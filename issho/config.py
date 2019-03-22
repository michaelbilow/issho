import toml
from pathlib import Path

ISSHO_CONF_FILE = Path('~/.issho/conf.toml').resolve()


def _make_issho_conf_dir():
    if not ISSHO_CONF_FILE.exists():
        ISSHO_CONF_FILE.parent.mkdir()
        ISSHO_CONF_FILE.touch()
    return


def read_issho_conf(host):
    _make_issho_conf_dir()
    conf = toml.load(ISSHO_CONF_FILE)
    if host not in conf:
        raise ValueError
    return conf[host]


def write_issho_conf(new_conf_dict):
    _make_issho_conf_dir()
    old_issho_conf = toml.load(ISSHO_CONF_FILE)
    new_conf = {**old_issho_conf, **new_conf_dict}
    toml.dump(new_conf, ISSHO_CONF_FILE)
    return
