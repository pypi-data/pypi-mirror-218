import typer
import subprocess
from diz.commands.setup import SetupCommand
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def setup(path: Annotated[str, typer.Option(prompt="请输入安装目录")],
          pkg: Annotated[str, typer.Option(prompt="请输入配置文件的 URL 地址")]):
    SetupCommand(path=path, pkg=pkg).run()


@app.command()
def gpu_info():
    try:
        info = subprocess.check_output(['nvidia-smi'], universal_newlines=True)
        print(info)
    except FileNotFoundError:
        print('nvidia-smi command not found. Make sure NVIDIA drivers are installed.')
    except subprocess.CalledProcessError:
        print('Not connected to a GPU')


def main():
    app()


if __name__ == "__main__":
    main()
