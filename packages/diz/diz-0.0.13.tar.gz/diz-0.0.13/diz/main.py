import typer
import subprocess
from diz.commands.setup import SetupCommand
from diz.commands.install import InstallCommand
from typing_extensions import Annotated
from diz.commands.shell import Tmux
from enum import Enum
import os


app = typer.Typer()


@app.command()
def setup(path: Annotated[str, typer.Option(prompt="请输入安装目录")],
          pkg: Annotated[str, typer.Option(prompt="请输入配置文件的 URL 地址")]):
    SetupCommand(path=path, pkg=pkg).run()


@app.command()
def install(name: str,
            path: Annotated[str, typer.Option(prompt="请输入安装目录")]):
    InstallCommand(path=path, name=name).run()


@app.command()
def gpu_info():
    try:
        info = subprocess.check_output(['nvidia-smi'], universal_newlines=True)
        print(info)
    except FileNotFoundError:
        print('nvidia-smi command not found. Make sure NVIDIA drivers are installed.')
    except subprocess.CalledProcessError:
        print('Not connected to a GPU')


class Mode(str, Enum):
    attach = 'i'
    detach = 'o'
    kill = 'k'


@app.command()
def shell(index: int = 0, mode: Mode = Mode.attach, auto_venv: bool = False):
    """
    使用 tmux 来实现后台服务管理，方便在服务端进行调试

    index: 需要进入第几个后台，默认为 0

    mode: 模式，i 为进入，o 为退出，kill 为删除
    """
    tmux = Tmux(index, auto_venv)
    if mode == Mode.attach:
        tmux.attach()
    elif mode == Mode.detach:
        tmux.detach()
    elif mode == Mode.kill:
        tmux.kill()


@app.command()
def venv():
    """
    激活虚拟环境
    """
    cmd = venv.get_activate_command('./venv')
    subprocess.run(cmd, shell=True, executable=os.environ.get("SHELL", ''))


def main():
    app()


if __name__ == "__main__":
    main()
