from pathlib import Path
import socket
import paramiko
import keyring

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
    key_profile = ''.join(ch for ch in key_path if ch.isalnum())
    return paramiko.RSAKey.from_private_key_file(
        key_file, password=keyring.get_password(
            issho_pw_name(pw_type='SSH', profile=key_profile), key_file))


def issho_pw_name(pw_type, profile):
    return 'issho_{}_{}'.format(pw_type, profile)

def ssh_pw_name(rsa_id):
    return 'issho_'
