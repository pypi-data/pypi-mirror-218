import os.path
import git
import diz.utils.dir
from diz.utils import pip
from diz.utils import download, yaml
from toolz import pipe


class SetupCommand:
    def __init__(self, pkg: str, path: str):
        self.pkg = pkg
        self.path = path
        self.config = yaml.load_yaml(self.pkg)
        self.install_path = self.path

    def create_dir(self, path, print_path=True):
        target_path = pipe(
            path,
            lambda p: os.path.join(self.install_path, p),
            os.path.expanduser,
        )
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        if print_path:
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
        if diz.utils.dir.is_empty(self.create_dir("code", False)):
            git.Repo.clone_from(self.config['code_repo'], self.create_dir("code", False))
            print("下载完成！")
        else:
            print("已经下载过了，无需下载。")

    def download_model_from_huggingface(self):
        if diz.utils.dir.is_empty(self.create_dir("model", False)):
            download.save_huggingface_model(self.config['huggingface'], self.create_dir("model", False))
            print("下载完成！")
        else:
            print("已经下载过了，无需下载。")

    def create_venv(self):
        if diz.utils.dir.is_empty(self.create_dir("venv", False)):
            os.system(f"cd {self.path} && python -m venv venv")
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
