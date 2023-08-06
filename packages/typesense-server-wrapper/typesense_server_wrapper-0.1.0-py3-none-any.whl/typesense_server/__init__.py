"""Typesense Server
"""

import contextlib
import pathlib
import subprocess


def get_path():
    """Get Typesense Server path."""
    init_path = pathlib.Path(__file__)
    bin_path = init_path.parent / 'typesense-server'
    return bin_path.resolve()


@contextlib.contextmanager
def run(*typesense_server_args, **proc_args):
    """Run Typesense Server

    :param list typesense_server_args: list of arguments for Typesense Server
    :param dict proc_args: dict of subprocess.Popen arguments
    """
    bin_path = str(get_path())
    proc = subprocess.Popen([bin_path, *typesense_server_args], **proc_args)
    with proc:
        yield proc
        proc.terminate()


__title__ = 'python-typesense-server-wrapper'
__version__ = '0.1.0'
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = '2023, Grant Jenks'
