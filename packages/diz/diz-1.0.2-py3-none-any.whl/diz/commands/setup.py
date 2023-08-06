import os.path
import git
import diz.utils.dir
from diz.utils import download, yaml, shell, pip
from toolz import pipe


class SetupCommand:
    def __init__(self, pkg: str, path: str):
        self.pkg = pkg
        self.path = path
        self.config = yaml.load_yaml(self.pkg)
        self.install_path = self.path

    def find_and_create_dir(self, path):
        target_path = self.get_dir(path)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        return target_path

    def create_dir(self, path):
        target_path = self.find_and_create_dir(path)
        print(f"创建目录：{target_path}")
        return target_path

    def get_dir(self, path):
        target_path = pipe(
            path,
            lambda p: os.path.join(self.install_path, p),
            os.path.expanduser,
        )
        return target_path

    def clone_code(self):
        code_path = self.find_and_create_dir("code")
        if diz.utils.dir.is_empty(code_path):
            git.Repo.clone_from(self.config['code_repo'], code_path)
            print("下载完成！")
        else:
            print("已经下载过了，无需下载。")

    def download_model_from_huggingface(self):
        model_path = self.find_and_create_dir("model")
        if diz.utils.dir.is_empty(model_path):
            download.save_huggingface_model(self.config['huggingface'], model_path)
            print("下载完成！")
        else:
            print("已经下载过了，无需下载。")

    def create_venv(self):
        venv_path = self.get_dir("venv")
        if not diz.utils.dir.is_empty(venv_path):
            shell.run(f"cd {self.path} && python -m venv venv")
            print("创建虚拟环境完成！")

    def install_deps(self):
        venv_path = self.get_dir("venv")
        for dep in self.config['deps']:
            pip.install(dep, venv_path)
        pip.install("diz", venv_path)

    def run(self):
        self.create_dir("code")
        self.create_dir("model")
        self.clone_code()
        self.download_model_from_huggingface()
        self.create_venv()
        self.install_deps()
