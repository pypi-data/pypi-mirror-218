from github import Github
from diz.commands.setup import SetupCommand


class InstallCommand:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_pkg(self):
        github = Github()
        repo = github.get_repo("mjason/diz_repo")
        file_path = f"{self.name}.yml"
        return repo.get_contents(file_path).download_url

    def run(self):
        setup_cmd = SetupCommand(self.get_pkg(), self.path)
        setup_cmd.run()
