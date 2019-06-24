import os
import socket
from pathlib import Path

import keyring
import paramiko


def absolute_path(raw_path):
    """
    Gets the string absolute path from a path object or string.

    :param raw_path: a string or ``pathlib.Path`` object
    """
    if not isinstance(raw_path, Path):
        raw_path = Path(raw_path)
    return str(raw_path.expanduser())


def default_sftp_path(this_path, default_path):
    """
    If ``this_path`` exists, return it as a path, else, return
    the ``pathlib.Path.name`` of the default path
    """
    return Path(this_path) if this_path else Path(Path(default_path).name)


def able_to_connect(host, port, timeout=1.5):
    """
    Returns true if it is possible to connect to the specified host
    and port, within the given timeout in seconds.
    """
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
    except Exception as e:
        return False
    return True


def get_pkey(key_path):
    """
    Helper for getting an RSA key
    """
    key_file = absolute_path(key_path)
    return paramiko.RSAKey.from_private_key_file(
        key_file, password=keyring.get_password(issho_ssh_pw_name(key_file), key_file)
    )


def issho_pw_name(pw_type, profile):
    """
    Helper for standardizing password names
    """
    return "issho_{}_{}".format(pw_type, profile)


def issho_ssh_pw_name(rsa_id):
    """
    Helper for standardizing ssh password names
    """
    return "issho_ssh_{}".format(
        "".join(ch for ch in absolute_path(rsa_id) if ch.isalnum())
    )


def get_user():
    return os.environ.get("USER")


def clean_spark_options(spark_options):
    new_spark_options = {}
    for k, v in spark_options.items():
        if not k.startswith("--"):
            k = "--{}".format(k)
        new_spark_options[k.replace("_", "-")] = v
    return new_spark_options


def add_arguments_to_cmd(cmd, *args):
    if not args:
        return cmd
    else:
        string_args = " ".join(map(str, args))
        return "{} {}".format(cmd, string_args)
