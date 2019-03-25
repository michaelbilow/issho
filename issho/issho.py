# -*- coding: utf-8 -*-

"""
Implementation for the ``Issho`` class, which implements
a connection and some simple commands over ``ssh``, using
``keyring`` to manage secrets locally.
"""

import paramiko
import keyring
from sshtunnel import SSHTunnelForwarder
from issho.helpers import absolute_path, default_sftp_path
from issho.config import read_issho_conf
import sys
import time
from shutil import copyfile


class Issho:

    def __init__(self,
                 key_path='~/.ssh/id_rsa',
                 ssh_config_path="~/.ssh/config",
                 profile='dev',
                 kinit=True):
        self.key_path = key_path
        self.ssh_config_path = ssh_config_path
        self.profile = profile
        self.remote_conf = read_issho_conf(profile)
        self.ssh_conf = self._get_issho_ssh_config()
        self.hostname = self.ssh_conf['hostname']
        self.port = int(self.ssh_conf['port'])
        self.user = self.ssh_conf['user']
        self._ssh = self._connect()
        if kinit:
            self.kinit()
        self._remote_home_dir = self.get_output('echo $HOME').strip()
        return

    def _get_pkey(self):
        """
        Helper for getting an RSA key
        """
        key_file = absolute_path(self.key_path)
        return paramiko.RSAKey.from_private_key_file(
            key_file, password=keyring.get_password('SSH', key_file))

    def _get_issho_ssh_config(self):
        """
        Helper method for getting data from .ssh/config
        """
        ssh_config_file = absolute_path(self.ssh_config_path)
        conf = paramiko.SSHConfig()
        conf.parse(open(ssh_config_file))
        issho_conf = conf.lookup(self.profile)
        return issho_conf

    def local_forward(self, remote_host, remote_port, local_host='0.0.0.0', local_port=44556):
        """
        Forwards a port from a remote through this Issho object.
        Useful for connecting to remote hosts that can only be accessed
        from inside a VPC of which your devbox is part.
        """
        tunnel = SSHTunnelForwarder(
            (self.hostname, self.port),
            ssh_username=self.user,
            ssh_pkey=self._get_pkey(),
            remote_bind_address=(remote_host, remote_port),
            local_bind_address=(local_host, local_port))
        tunnel.start()
        return tunnel

    def _connect(self):
        """
        Uses paramiko to connect to the remote specified
        :return:
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname,
                    username=self.user,
                    port=self.port,
                    pkey=self._get_pkey())
        return ssh

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
            cmd = 'cmd=$"{}"; nohup bash -c "$cmd" &'.format(cmd.replace('"', r'\"'))
        if debug:
            print(cmd)
        stdin, stdout, stderr = self._ssh.exec_command(cmd)

        captured_output = ''
        for line in stdout:
            if capture_output:
                captured_output += line
            else:
                print(line, end='')

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
            sftp.get(remotepath=paths['remotepath'], localpath=paths['localpath'])
        return

    def put(self, localpath, remotepath=None):
        """
        Puts the file at the local path to the remote.

        :param localpath: The local path of the file to put to the remote

        :param remotepath: Defaults to the name of the local path
        """
        paths = self._sftp_paths(localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.put(localpath=paths['localpath'], remotepath=paths['remotepath'], callback=self._sftp_progress)
        return

    def kinit(self):
        """
        Runs kerberos init
        """
        kinit_pw = keyring.get_password('{}_kinit'.format(self.profile), self.user)
        if kinit_pw:
            self.exec('echo {} | kinit'.format(kinit_pw))
        else:
            raise OSError("Add your kinit password to your keyring")
        return

    def hive(self, query):
        """
        Runs a hive query using the parameters
        set in .issho/config.toml

        :param query: a string query, or the name of a query file
            name to run.
        """
        tmp_filename = '/tmp/issho_{}.sql'.format(time.time())
        if query.endswith('sql', 'hql'):
            copyfile(query, tmp_filename)
        else:
            with open(tmp_filename, 'w') as f:
                f.write(query)
        self.put(tmp_filename, tmp_filename)

        self.exec('beeline {opts} -u  "{jdbc}" -f {fn}'.format(
            opts=self.remote_conf['HIVE_OPTS'],
            jdbc=self.remote_conf['HIVE_JDBC'],
            fn=tmp_filename))

    def _sftp_paths(self, localpath, remotepath):
        localpath = default_sftp_path(localpath, remotepath)
        remotepath = default_sftp_path(remotepath, localpath)
        return {'localpath': str(localpath.expanduser()),
                'remotepath': str(remotepath).replace('~', self._remote_home_dir)}

    @staticmethod
    def _sftp_progress(transferred, remaining):
        print('{:.1f} MB transferred, {:.1f} MB remaining'.format(transferred/2**20, remaining/2**20))

