import subprocess
import requests
from diz.utils import validators
import os
import tempfile


def run_command_in_venv(command, venv_path):
    activate_script = f"{venv_path}/bin/activate"
    cmd = f"source {activate_script} && {command}"
    subprocess.run(cmd, shell=True)


def install(dep, venv_path):
    if validators.is_valid_url(dep):
        install_from_url(dep, venv_path)
    else:
        run_command_in_venv(f"pip install {dep}", venv_path)


def install_from_url(url, ven_path):
    with tempfile.TemporaryDirectory() as (tmp_dir):
        tmp_file = os.path.join(tmp_dir, 'requirements.txt')
        with open(tmp_file, 'w') as (f):
            f.write(requests.get(url).text)
        run_command_in_venv(f"pip install -r {tmp_file}", ven_path)