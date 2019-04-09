import toml
import paramiko
from pathlib import Path
from issho.helpers import absolute_path

ISSHO_CONF_FILE = Path.home().joinpath('.issho').joinpath('conf.toml')


def _make_issho_conf_dir():
    if not ISSHO_CONF_FILE.exists():
        ISSHO_CONF_FILE.parent.mkdir()
        ISSHO_CONF_FILE.touch()
    return


def read_issho_conf(profile):
    _make_issho_conf_dir()
    conf = toml.load(ISSHO_CONF_FILE)
    if profile not in conf:
        raise ValueError
    return conf[profile]


def write_issho_conf(new_conf_dict):
    """
    Updates the issho config file
    """
    _make_issho_conf_dir()
    old_issho_conf = toml.load(ISSHO_CONF_FILE)
    new_conf = {**old_issho_conf, **new_conf_dict}
    toml.dump(new_conf, open(str(ISSHO_CONF_FILE), 'w'))
    return


def read_ssh_profile(ssh_config_path, profile):
    """
    Helper method for getting data from .ssh/config
    """
    ssh_config_file = absolute_path(ssh_config_path)
    conf = paramiko.SSHConfig()
    conf.parse(open(ssh_config_file))
    return conf.lookup(profile)
