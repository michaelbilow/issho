import toml
import paramiko
from pathlib import Path
from issho.helpers import absolute_path

ISSHO_DIR = Path.home().joinpath(".issho")
ISSHO_CONF_FILE = ISSHO_DIR.joinpath("conf.toml")
ISSHO_ENV_FILE = ISSHO_DIR.joinpath("envs.toml")


def _make_issho_conf_dir():
    if not ISSHO_DIR.exists():
        ISSHO_DIR.mkdir()
    if not ISSHO_CONF_FILE.exists():
        ISSHO_CONF_FILE.touch()
    if not ISSHO_ENV_FILE.exists():
        ISSHO_ENV_FILE.touch()
    return


def read_issho_conf(profile, filename=ISSHO_CONF_FILE):
    """
    Writes issho variables out to a ``.toml`` file.

    :param profile: The name of the profile to read
    :param filename: The output filename
    :return: a dict of data stored with that profile in the configuration file
    """
    _make_issho_conf_dir()
    conf = toml.load(filename)
    if profile not in conf:
        raise ValueError
    return conf[profile]


def read_issho_env(profile):
    """
    Reads issho environment variables to a dict
    :param profile: the name of the issho environment to draw from
    :return: a dict of data with that profile stored in the environment file
    """
    return read_issho_conf(profile, filename=ISSHO_ENV_FILE)


def write_issho_conf(new_conf_dict, filename=ISSHO_CONF_FILE):
    """
    Updates the issho config file
    :param new_conf_dict: the new configuration to add
    :param filename: the location of the old configuration file
    """
    _make_issho_conf_dir()
    old_issho_conf = toml.load(filename)
    new_conf = {**old_issho_conf, **new_conf_dict}
    toml.dump(new_conf, open(str(filename), "w"))
    return


def write_issho_env(new_env_dict):
    """
    Save a new issho environment
    :param new_env_dict: the new set of environment paramters to add
    """
    write_issho_conf(new_env_dict, filename=ISSHO_ENV_FILE)


def read_ssh_profile(ssh_config_path, profile):
    """
    Helper method for getting data from .ssh/config
    """
    ssh_config_file = absolute_path(ssh_config_path)
    conf = paramiko.SSHConfig()
    conf.parse(open(ssh_config_file))
    return conf.lookup(profile)
