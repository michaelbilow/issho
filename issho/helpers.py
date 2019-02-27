from pathlib import Path
import socket


def absolute_path(raw_path):
    if not isinstance(raw_path, Path):
        raw_path = Path(raw_path)
    return str(raw_path.expanduser())


def default_sftp_path(this_path, that_path):
    return Path(this_path) if this_path else Path(Path(that_path).name)


def able_to_connect(host, port, timeout=1.5):
    try:
        sock = socket.socket()
        sock.settimeout(timeout)
        sock.connect((host, port))
    except Exception as e:
        return False
    return True
