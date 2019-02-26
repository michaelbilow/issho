from pathlib import Path
import socket
import os


def absolute_path(raw_path):
    if not isinstance(raw_path, Path):
        raw_path = Path(raw_path)
    return str(raw_path.expanduser())


def default_sftp_path(input_path):
    return os.path.split(input_path)[1]


def able_to_connect(host, port):
    try:
        sock = socket.socket()
        sock.settimeout(3)
        sock.connect((host, port))
    except Exception as e:
        return False
    return True
