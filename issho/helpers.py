from pathlib import Path
import socket


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
