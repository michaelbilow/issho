# -*- coding: utf-8 -*-

"""Main module."""

import paramiko
import keyring
from sshtunnel import SSHTunnelForwarder
from issho.helpers import absolute_path, default_sftp_path
import sys


class Issho:

    def __init__(self,
                 key_path='~/.ssh/id_rsa',
                 config_path="~/.ssh/config",
                 host='dev',
                 kinit_service='kinit',
                 kinit=True):
        self.key_path = key_path
        self.config_path = config_path
        self.host = host
        self.conf = self._get_issho_ssh_config()
        self.hostname = self.conf['hostname']
        self.port = int(self.conf['port'])
        self.user = self.conf['user']
        self.kinit_service = kinit_service
        self._ssh = self._connect()
        if kinit:
            self.kinit()
        self._remote_home_dir = self.get_output('echo $HOME').strip()
        return

    def _get_pkey(self):
        key_file = absolute_path(self.key_path)
        return paramiko.RSAKey.from_private_key_file(
            key_file, password=keyring.get_password('SSH', key_file))

    def _get_issho_ssh_config(self):
        ssh_config_file = absolute_path(self.config_path)
        conf = paramiko.SSHConfig()
        conf.parse(open(ssh_config_file))
        issho_conf = conf.lookup(self.host)
        return issho_conf

    def local_forward(self, remote_host, remote_port, local_host='0.0.0.0', local_port=44556):
        tunnel = SSHTunnelForwarder(
            (self.hostname, self.port),
            ssh_username=self.user,
            ssh_pkey=self._get_pkey(),
            remote_bind_address=(remote_host, remote_port),
            local_bind_address=(local_host, local_port))
        tunnel.start()
        return tunnel

    def _connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname,
                    username=self.user,
                    port=self.port,
                    pkey=self._get_pkey())
        return ssh

    def exec(self, cmd, bg=False, debug=False, capture_output=False):
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
        return self.exec(cmd, bg=True, **kwargs)

    def get_output(self, cmd, **kwargs):
        return self.exec(cmd, capture_output=True, **kwargs)

    def get(self, remotepath, localpath=None):
        localpath, remotepath = self._sftp_paths(
            localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.get(remotepath=remotepath, localpath=localpath)
        return

    def put(self, localpath, remotepath=None):
        localpath, remotepath = self._sftp_paths(
            localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.put(localpath=localpath, remotepath=remotepath)
        return

    def kinit(self):
        if keyring.get_password(self.kinit_service, self.user):
            self.exec('echo {} | kinit'.format(keyring.get_password(self.kinit_service, self.user)))
        else:
            raise OSError("Add your kinit password to your keyring via\n"
                          "python -m keyring set kinit {}".format(self.user))
        return

    def _sftp_paths(self, localpath, remotepath):
        localpath = default_sftp_path(localpath, remotepath)
        remotepath = default_sftp_path(remotepath, localpath)
        return str(localpath.expanduser()), \
               str(remotepath).replace('~', self._remote_home_dir)
