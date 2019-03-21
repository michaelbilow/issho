from prompt_toolkit import prompt
import keyring
from issho.config import read_issho_conf, write_issho_conf

def main():
    profile = prompt('What is the name of this profile in your ssh config? ')
    while True:
        pw = prompt('Enter the kinit password: ', is_password=True)
        if not pw:
            break
        pw2 = prompt('Enter the kinit password again: ', is_password=True)
        if pw != pw2:
            print('passwords do not match')
        else:
            keyring.set_password('{}_kinit'.format(profile), os.environ.get('USER'), pw)
            break

    hive_opts = prompt('Hive Options: ')
    jdbc_conn = prompt('JDBC connection string: ')




if __name__ == "__main__":
    main()
