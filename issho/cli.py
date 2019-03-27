from prompt_toolkit import prompt
import keyring
from issho.config import write_issho_conf, read_issho_conf, read_ssh_config
from issho.helpers import issho_pw_name, ssh_pw_name
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

        ssh_conf = read_ssh_config(ssh_config)
        if not all(x in ssh_conf.lookup(ssh_profile) for x in ('hostname', 'user')):
            raise KeyError()

        if not keyring.get_password(ssh_pw_name(rsa_id))

        while True:
            pw = prompt("Enter the profile's kinit password: ", is_password=True)
            if not pw:
                break
            pw2 = prompt('Enter the kinit password again: ', is_password=True)
            if pw != pw2:
                print('passwords do not match')
            else:
                keyring.set_password(issho_pw_name(pw_type='kinit', profile=profile),
                                     local_user, pw)
                break

        hive_opts = prompt('Hive Options: ')
        hive_jdbc = prompt('Hive JDBC connection string: ')
        spark_shell_conf = prompt('Spark Shell Configuration String: ')

        new_conf = {

            'HIVE_OPTS': hive_opts,
            'HIVE_JDBC': hive_jdbc,
            'SPARK_CONF': spark_shell_conf
        }
        write_issho_conf({profile: new_conf})

    def set_variable(self, profile, var_name):
        old_issho_config = read_issho_conf(profile)



def main():
    """
    Inititates the CLI using python-fire
    """
    fire.Fire(IsshoCLI)


if __name__ == "__main__":
    main()
