# -*- coding: utf-8 -*-

"""Main module."""

import paramiko
import keyring
from sshtunnel import SSHTunnelForwarder
from devbox.helpers import absolute_path, able_to_connect
import sys

class Devbox:

    def __init__(self,
                 key_path='~/.ssh/id_rsa',
                 config_path="~/.ssh/config",
                 host='dev',
                 kinit_service='kinit',
                 kinit=True):
        self.key_path = key_path
        self.config_path = config_path
        self.host = host
        self.conf = self.get_devbox_ssh_config()
        self.hostname = self.conf['hostname']
        self.port = int(self.conf['port'])
        self.user = self.conf['user']
        self.kinit_service = kinit_service
        self.connect(kinit=kinit)
        return

    def _get_pkey(self):
        key_file = absolute_path(self.key_path)
        return paramiko.RSAKey.from_private_key_file(
            key_file, password=keyring.get_password('SSH', key_file))

    def get_devbox_ssh_config(self):
        ssh_config_file = absolute_path(self.config_path)
        conf = paramiko.SSHConfig()
        conf.parse(open(ssh_config_file))
        devbox_conf = conf.lookup(self.host)
        return devbox_conf

    def local_forward(self, remote_host, remote_port, local_host='0.0.0.0', local_port=44556):
        tunnel = SSHTunnelForwarder(
            (self.hostname, self.port),
            ssh_username=self.user,
            ssh_pkey=self._get_pkey(),
            remote_bind_address=(remote_host, remote_port),
            local_bind_address=(local_host, local_port))
        tunnel.start()
        return tunnel

    def connect(self, kinit=True):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname,
                    username=self.user,
                    port=self.port,
                    pkey=self._get_pkey(),)
        self.ssh = ssh
        if kinit:
            self.kinit()
        return

    def exec(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        for line in stdout:
            print(line, end='')
        for line in stderr:
            sys.stderr.write(line)
        return

    def get(self, remote_path, local_path):
        with self.ssh.open_sftp() as sftp:
            sftp.get(remote_path=remote_path, local_path=local_path)
        return

    def put(self, local_path, remote_path):
        with self.ssh.open_sftp() as sftp:
            sftp.put(local_path=local_path, remote_path=remote_path)
        return

    def kinit(self):
        if keyring.get_password(self.kinit_service, self.user):
            self.exec('echo {} | kinit'.format(keyring.get_password(self.kinit_service, self.user)))
        else:
            raise OSError("Add your kinit password to your keyring via\n"
                          "python -m keyring set kinit {}".format(self.user))
        return
