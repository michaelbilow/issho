# -*- coding: utf-8 -*-

"""
Implementation for the ``Issho`` class, which implements
a connection and some simple commands over ``ssh``, using
``keyring`` to manage secrets locally.
"""

import paramiko
import keyring
from sshtunnel import SSHTunnelForwarder
from issho.helpers import default_sftp_path, get_pkey, issho_pw_name, get_user
from issho.config import read_issho_conf, read_ssh_profile
import sys
import time
from shutil import copyfile
import humanize


class Issho:
    def __init__(self, profile="dev", kinit=True):
        self.local_user = get_user()
        self.profile = profile
        self.issho_conf = read_issho_conf(profile)
        self.ssh_conf = read_ssh_profile(self.issho_conf["SSH_CONFIG_PATH"], profile)
        self.hostname = self.ssh_conf.get("hostname", None)
        self.user = self.ssh_conf.get("user", None)
        self.port = self.ssh_conf.get("port", 22)
        self._ssh = self._connect()
        if kinit:
            self.kinit()
        self._remote_home_dir = self.get_output("echo $HOME").strip()
        return

    def local_forward(
        self, remote_host, remote_port, local_host="0.0.0.0", local_port=44556
    ):
        """
        Forwards a port from a remote through this Issho object.
        Useful for connecting to remote hosts that can only be accessed
        from inside a VPC of which your devbox is part.
        """
        tunnel = SSHTunnelForwarder(
            (self.hostname, self.port),
            ssh_username=self.user,
            ssh_pkey=get_pkey(self.issho_conf["ID_RSA"]),
            remote_bind_address=(remote_host, remote_port),
            local_bind_address=(local_host, local_port),
        )
        tunnel.start()
        return tunnel

    def exec(self, cmd, bg=False, debug=False, capture_output=False):
        """
        Execute a command in bash over the SSH connection.

        Note, this command does not use an interactive terminal;
        it instead uses a *non-interactive login* shell.
        This means (specifically) that your aliased commands will not work
        and only variables exported in your remote ``.bashrc`` will be available.

        :param cmd: The bash command to be run remotely

        :param bg: True = run in the background

        :param debug: True = print some debugging output

        :param capture_output: True = return stdout as a string

        :return:
        """
        if bg:
            cmd = 'cmd=$"{}"; nohup bash -c "$cmd" &'.format(cmd.replace('"', r"\""))
        if debug:
            print(cmd)
        stdin, stdout, stderr = self._ssh.exec_command(cmd)

        captured_output = ""
        for line in stdout:
            if capture_output:
                captured_output += line
            else:
                print(line, end="")

        for line in stderr:
            sys.stderr.write(line)
        return captured_output

    def exec_bg(self, cmd, **kwargs):
        """
        Syntactic sugar for ``exec(bg=True)``
        """
        return self.exec(cmd, bg=True, **kwargs)

    def get_output(self, cmd, **kwargs):
        """
        Syntactic sugar for ``exec(capture_output=True)``
        """
        return self.exec(cmd, capture_output=True, **kwargs)

    def get(self, remotepath, localpath=None):
        """
        Gets the file at the remote path and puts it locally.

        :param remotepath: The path on the remote from which to get.

        :param localpath: Defaults to the name of the remote path
        """
        paths = self._sftp_paths(localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.get(
                remotepath=paths["remotepath"],
                localpath=paths["localpath"],
                callback=self._sftp_progress,
            )
        return

    def put(self, localpath, remotepath=None):
        """
        Puts the file at the local path to the remote.

        :param localpath: The local path of the file to put to the remote

        :param remotepath: Defaults to the name of the local path
        """
        paths = self._sftp_paths(localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.put(
                localpath=paths["localpath"],
                remotepath=paths["remotepath"],
                callback=self._sftp_progress,
            )
        return

    def kinit(self):
        """
        Runs kerberos init
        """
        kinit_pw = self._get_password("kinit")
        if kinit_pw:
            self.exec("echo {} | kinit".format(kinit_pw))
        else:
            raise OSError(
                "Add your kinit password with `issho config <profile>` "
                "or by editing `~/.issho/config.toml`"
            )
        return

    def hive(self, query, output_filename=None, remove_blank_top_line=True):
        """
        Runs a hive query using the parameters
        set in .issho/config.toml

        :param query: a string query, or the name of a query file
            name to run.
        :param output_filename: the (local) file to output the results
            of the hive query to. Adding this option will also
            keep a copy of the results in /tmp
        :param remove_blank_top_line: Hive usually has a blank top line
            when data is output, this parameter removes it.
        """
        query = str(query)
        tmp_filename = "/tmp/issho_{}.sql".format(time.time())
        if query.endswith("sql") or query.endswith("hql"):
            copyfile(query, tmp_filename)
        else:
            with open(tmp_filename, "w") as f:
                f.write(query)
        self.put(tmp_filename, tmp_filename)

        tmp_output_filename = "{}.output".format(tmp_filename)

        hive_cmd = 'beeline {opts} -u  "{jdbc}" -f {fn} {remove_first_line} {redirect_to_tmp_fn}'.format(
            opts=self.issho_conf["HIVE_OPTS"],
            jdbc=self.issho_conf["HIVE_JDBC"],
            fn=tmp_filename,
            remove_first_line="| sed 1d" if remove_blank_top_line else "",
            redirect_to_tmp_fn="> {}".format(tmp_output_filename)
            if output_filename
            else "",
        )

        self.exec(hive_cmd)

        if output_filename:
            self.get(tmp_output_filename, output_filename)

    def _connect(self):
        """
        Uses paramiko to connect to the remote specified
        :return:
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.hostname,
            username=self.user,
            port=self.port,
            pkey=get_pkey(self.issho_conf["RSA_ID_PATH"]),
        )
        return ssh

    def _sftp_paths(self, localpath, remotepath):
        localpath = default_sftp_path(localpath, remotepath)
        remotepath = default_sftp_path(remotepath, localpath)
        return {
            "localpath": str(localpath.expanduser()),
            "remotepath": str(remotepath).replace("~", self._remote_home_dir),
        }

    @staticmethod
    def _sftp_progress(transferred, to_transfer):
        print(
            "{} transferred out of a total of {}".format(
                humanize.naturalsize(transferred), humanize.naturalsize(to_transfer)
            )
        )

    def _get_password(self, pw_type):
        return keyring.get_password(
            issho_pw_name(pw_type=pw_type, profile=self.profile), self.local_user
        )
