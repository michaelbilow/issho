import toml

ISSHO_CONF_FILE = Path('~/.issho/conf.toml').resolve()
from pathlib import Path


def _make_issho_conf_dir():
    if not ISSHO_CONF_FILE.exists():
        ISSHO_CONF_FILE.parent.mkdir()
    return


def read_issho_conf():
    _make_issho_conf_dir()
    return toml.load(ISSHO_CONF_FILE)


def write_issho_conf(new_conf_dict):
    old_issho_conf = toml.load(ISSHO_CONF_FILE)
    new_conf = {**old_issho_conf, **new_conf_dict}
    toml.dump(new_conf, ISSHO_CONF_FILE)
    return
