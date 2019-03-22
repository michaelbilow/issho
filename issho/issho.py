# -*- coding: utf-8 -*-

"""Main module."""

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
                 host='dev',
                 kinit=True):
        self.key_path = key_path
        self.ssh_config_path = ssh_config_path
        self.host = host
        self.remote_conf = read_issho_conf(host)
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
        key_file = absolute_path(self.key_path)
        return paramiko.RSAKey.from_private_key_file(
            key_file, password=keyring.get_password('SSH', key_file))

    def _get_issho_ssh_config(self):
        ssh_config_file = absolute_path(self.ssh_config_path)
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
        paths = self._sftp_paths(localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.get(remotepath=paths['remotepath'], localpath=paths['localpath'])
        return

    def put(self, localpath, remotepath=None):
        paths = self._sftp_paths(localpath=localpath, remotepath=remotepath)
        with self._ssh.open_sftp() as sftp:
            sftp.put(localpath=paths['localpath'], remotepath=paths['remotepath'], callback=self._sftp_progress)
        return

    def kinit(self):
        kinit_pw = keyring.get_password('{}_kinit'.format(self.host), self.user)
        if kinit_pw:
            self.exec('echo {} | kinit'.format(kinit_pw))
        else:
            raise OSError("Add your kinit password to your keyring")
        return

    def hive(self, query):
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

