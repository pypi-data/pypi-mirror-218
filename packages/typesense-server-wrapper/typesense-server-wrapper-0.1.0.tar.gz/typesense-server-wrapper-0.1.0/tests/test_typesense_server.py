"""Test Python wrapper for Typesense Server"""
import os
import shutil
import time

import typesense_server


def test_title():
    assert typesense_server.__title__ == 'python-typesense-server-wrapper'


def test_run():
    shutil.rmtree('data', ignore_errors=True)
    os.mkdir('data')
    args = ['--api-key', 'abc', '--data-dir', 'data']
    with typesense_server.run(*args):
        time.sleep(10)
