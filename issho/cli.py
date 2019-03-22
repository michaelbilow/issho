from prompt_toolkit import prompt
import keyring
from issho.config import write_issho_conf
import os
import fire


class IsshoCLI:
    """
    CLI for Issho; right now only used for configuration
    """

    def config(self, profile):
        """
        Configures a single issho profile.

        :param profile: name of the profile to configure; should
        match the name in the ssh config.
        """

        while True:
            pw = prompt("Enter the profile's kinit password: ", is_password=True)
            if not pw:
                break
            pw2 = prompt('Enter the kinit password again: ', is_password=True)
            if pw != pw2:
                print('passwords do not match')
            else:
                keyring.set_password('{}_kinit'.format(profile), os.environ.get('USER'), pw)
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


def main():
    """
    Inititates the CLI using python-fire
    """
    fire.Fire(IsshoCLI)


if __name__ == "__main__":
    main()
