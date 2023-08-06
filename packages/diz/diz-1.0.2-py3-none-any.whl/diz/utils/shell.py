import os
import subprocess


def current():
    """
    Get current shell name and path
    :return: shell name, shell path
    """
    shell = os.environ.get('SHELL', '')
    return shell.split('/')[-1], shell


def run(cmd):
    _, path = current()
    subprocess.call(cmd, shell=True, executable=path)