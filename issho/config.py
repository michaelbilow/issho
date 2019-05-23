import toml
import paramiko
from pathlib import Path
from issho.helpers import absolute_path

ISSHO_DIR = Path.home().joinpath('.issho')
ISSHO_CONF_FILE = ISSHO_DIR.joinpath('conf.toml')
ISSHO_ENV_FILE = ISSHO_DIR.joinpath('envs.toml')


def _make_issho_conf_dir():
    if not ISSHO_DIR.exists():
        ISSHO_DIR.mkdir()
    if not ISSHO_CONF_FILE.exists():
        ISSHO_CONF_FILE.touch()
    if not ISSHO_ENV_FILE.exists():
        ISSHO_ENV_FILE.touch()
    return


def read_issho_conf(profile, filename=ISSHO_CONF_FILE):
    _make_issho_conf_dir()
    conf = toml.load(filename)
    if profile not in conf:
        raise ValueError
    return conf[profile]


def read_issho_env(profile):
    return read_issho_conf(profile, filename=ISSHO_ENV_FILE)


def write_issho_conf(new_conf_dict, filename=ISSHO_CONF_FILE):
    """
    Updates the issho config file
    """
    _make_issho_conf_dir()
    old_issho_conf = toml.load(filename)
    new_conf = {**old_issho_conf, **new_conf_dict}
    toml.dump(new_conf, open(str(filename), 'w'))
    return


def write_issho_env(new_env_dict):
    write_issho_conf(new_env_dict, filename=ISSHO_ENV_FILE)


def read_ssh_profile(ssh_config_path, profile):
    """
    Helper method for getting data from .ssh/config
    """
    ssh_config_file = absolute_path(ssh_config_path)
    conf = paramiko.SSHConfig()
    conf.parse(open(ssh_config_file))
    return conf.lookup(profile)
