import platform
import os


def get_current_shell():
    shell = os.environ.get('SHELL', '')
    if shell.endswith('bash'):
        return 'bash'
    elif shell.endswith('zsh'):
        return 'zsh'
    elif shell.endswith('fish'):
        return 'fish'
    elif 'csh' in shell or 'tcsh' in shell:
        return 'csh'
    else:
        raise ValueError("Unsupported shell")


def get_activate_command(venv_path):
    system = platform.system()
    shell = get_current_shell()

    if system == 'Windows':
        if shell == 'cmd.exe':
            return f'call {venv_path}\\Scripts\\activate.bat'
        elif shell == 'PowerShell':
            return f'& {venv_path}\\Scripts\\Activate.ps1'
        else:
            raise ValueError(f"Unsupported shell: {shell}")
    elif system in ('Linux', 'Darwin'):
        if shell in ('bash', 'zsh'):
            return f'source {venv_path}/bin/activate'
        elif shell == 'fish':
            return f'source {venv_path}/bin/activate.fish'
        elif shell in ('csh', 'tcsh'):
            return f'source {venv_path}/bin/activate.csh'
        else:
            raise ValueError(f"Unsupported shell: {shell}")
    else:
        raise ValueError(f"Unsupported system: {system}")