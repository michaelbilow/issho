from prompt_toolkit import prompt
import keyring
from issho.config import write_issho_conf, read_issho_conf, \
    read_ssh_profile, write_issho_env, read_issho_env
from issho.helpers import issho_pw_name, issho_ssh_pw_name, \
    absolute_path, get_user
from collections import OrderedDict
from issho.issho import Issho
import fire
import re

OPENSSH_PASSWORD_ERROR = '''
Paramiko v2.4.0 does not allow OpenSSH RSA key format (common on new Macs);
see: https://github.com/paramiko/paramiko/issues/1313#issuecomment-492448807
Create your ssh key using:
$ ssh-keygen -t rsa -b 4096 -C "email@email.com" -m PEM
'''

ENV_PROMPTS = OrderedDict((
    ('HIVE_OPTS', 'Hive Options: '),
    ('HIVE_JDBC', 'Hive JDBC connection string: '),
    ('SPARK_CONF', 'Spark Shell Configuration String: ')
))


class IsshoCLI:
    """
    CLI for Issho; right now only used for configuration
    """

    def config(self, profile, env=None, ssh_profile='', ssh_config='~/.ssh/config',
               rsa_id='~/.ssh/id_rsa'):
        """
        Configures a single issho profile. Saves non-private variables
        to ``~/.issho/conf.toml`` and passwords to the local keyring.

        :param profile: name of the profile to configure

        :param env: Optional environment variable profile to draw from.

        :param ssh_profile: The name of the associated ssh config profile;
            defaults to the profile name if not supplied.

        :param ssh_config: the path to the ssh_config to be used for this profile

        :param rsa_id: the path to the id_rsa file to be used for this profile
        """

        local_user = get_user()
        ssh_profile = profile if not ssh_profile else profile
        rsa_id = absolute_path(rsa_id)
        ssh_config = absolute_path(ssh_config)
        env = read_issho_env(env) if env else {}
        print(env)

        ssh_conf = read_ssh_profile(ssh_config, ssh_profile)
        if not all(x in ssh_conf for x in ('hostname', 'user')):
            raise KeyError()

        if not keyring.get_password(issho_ssh_pw_name(rsa_id), rsa_id):
            _set_up_ssh_password(rsa_id=rsa_id)

        kinit_was_setup = _set_up_password(pw_type='kinit',
                                           profile=profile,
                                           pw_user=local_user)

        new_conf = {
            'SSH_CONFIG_PATH': ssh_config,
            'RSA_ID_PATH': rsa_id,
            **_get_env_vars(env)
        }
        write_issho_conf({profile: new_conf})
        self.test_connection(profile, kinit=kinit_was_setup)

    @staticmethod
    def env(name):
        """
        Saves a set of variables to ~/.issho/envs.toml
        :param name: name of the environment to set up or update
        """
        env_conf = {name: _get_env_vars({})}
        write_issho_env(env_conf)
        return env_conf

    @staticmethod
    def update_variable(profile, variable, value):
        """
        Updates or add a single profile variable.
        """
        old_conf = read_issho_conf(profile)
        old_conf[variable] = value
        write_issho_conf({profile: old_conf})

    @staticmethod
    def test_connection(profile, kinit=True):
        try:
            test_issho = Issho(profile, kinit)
        except Exception as e:
            return 'Test Connection failed with error: {}'.format(str(e))
        return 'Test Connection Successful!'


def _get_env_vars(env):
    return {var_name: env.get(var_name) if var_name in env else prompt(prompt_str)
            for var_name, prompt_str in ENV_PROMPTS.items()}


def _get_pw(pw_type):
    """
    Gets a password using the prompt toolkit
    """
    while True:
        pw = prompt("Enter the {} password: ".format(pw_type), is_password=True)
        if not pw:
            break
        pw2 = prompt('Enter the {} password again: '.format(pw_type), is_password=True)
        if pw != pw2:
            print('The passwords do not match; try again')
        else:
            return pw


def _set_up_password(pw_type, profile, pw_user):
    """
    Gets an issho password for this profile and
    saves it to the local keyring.
    """
    pw = _get_pw(pw_type=pw_type)
    pw_name = issho_pw_name(pw_type=pw_type, profile=profile)
    keyring.set_password(pw_name, pw_user, pw)
    return True if pw else False


def _set_up_ssh_password(rsa_id):
    """
    Adds the ssh password to the local keyring.
    """
    _check_not_openssh_pkey(rsa_id)
    pw = _get_pw(pw_type='ssh')
    pw_name = issho_ssh_pw_name(rsa_id=rsa_id)
    keyring.set_password(pw_name, rsa_id, pw)
    return True if pw else False


def _check_not_openssh_pkey(rsa_id):
    with open(rsa_id) as f:
        if re.search('OPENSSH', f.readline()):
            raise ValueError(OPENSSH_PASSWORD_ERROR)


def main():
    """
    Inititates the CLI using python-fire
    """
    fire.Fire(IsshoCLI)


if __name__ == "__main__":
    main()
