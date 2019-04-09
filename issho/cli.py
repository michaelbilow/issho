from prompt_toolkit import prompt
import keyring
from issho.config import write_issho_conf, read_issho_conf, read_ssh_profile
from issho.helpers import issho_pw_name, issho_ssh_pw_name, absolute_path
import os
import fire


class IsshoCLI:
    """
    CLI for Issho; right now only used for configuration
    """

    def config(self, profile, ssh_profile='', ssh_config='~/.ssh/config',
               rsa_id='~/.ssh/id_rsa'):
        """
        Configures a single issho profile. Saves non-private variables
        to ``~/.issho/conf.toml`` and passwords to the local keyring.

        :param profile: name of the profile to configure

        :param ssh_profile: The name of the associated ssh config profile;
            defaults to the profile name if not supplied.

        :param ssh_config: the path to the ssh_config to be used for this profile

        :param rsa_id: the path to the id_rsa file to be used for this profile
        """

        local_user = os.environ.get('USER')
        ssh_profile = profile if not ssh_profile else profile
        rsa_id = absolute_path(rsa_id)

        ssh_conf = read_ssh_profile(ssh_config, ssh_profile)
        if not all(x in ssh_conf for x in ('hostname', 'user')):
            raise KeyError()

        if not keyring.get_password(issho_ssh_pw_name(rsa_id), rsa_id):
            _set_up_ssh_password(rsa_id=rsa_id)

        _set_up_password(pw_type='kinit',
                         profile=profile,
                         pw_user=local_user)

        hive_opts = prompt('Hive Options: ')
        hive_jdbc = prompt('Hive JDBC connection string: ')
        spark_shell_conf = prompt('Spark Shell Configuration String: ')

        new_conf = {
            'HIVE_OPTS': hive_opts,
            'HIVE_JDBC': hive_jdbc,
            'SPARK_CONF': spark_shell_conf,
            'SSH_CONFIG_PATH': ssh_config,
            'RSA_ID_PATH': rsa_id
        }
        write_issho_conf({profile: new_conf})

    def update_variable(self, profile, variable, value):
        """
        Updates or add a single profile variable.
        """
        old_conf = read_issho_conf(profile)
        old_conf[variable] = value
        write_issho_conf({profile: old_conf})


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
    return


def _set_up_ssh_password(rsa_id):
    """
    Adds the ssh password to the local keyring.
    """
    pw = _get_pw(pw_type='ssh')
    pw_name = issho_ssh_pw_name(rsa_id=rsa_id)
    keyring.set_password(pw_name, rsa_id, pw)
    return


def main():
    """
    Inititates the CLI using python-fire
    """
    fire.Fire(IsshoCLI)


if __name__ == "__main__":
    main()
