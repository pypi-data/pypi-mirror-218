import libtmux
from diz.utils import dir
from diz.utils import venv


class Tmux:
    def __init__(self, index=0, auto_venv=True):
        self.server = libtmux.Server()
        self.session = self.find_or_create_session(index, auto_venv)

    def find_or_create_session(self, index=0, auto_venv=True):
        session_name = f"diz_{index}"
        sessions = self.server.sessions.filter(session_name=session_name)
        if not sessions:
            session = self.server.new_session(session_name=session_name)
            if not dir.is_empty('./venv/bin/activate') and auto_venv:
                cmd = venv.get_activate_command('./venv')
                self.run_cmd(cmd)
        else:
            session = sessions[0]
        return session

    def attach(self):
        self.session.attach_session()

    def run_cmd(self, command):
        window = self.session.attached_window
        pane = window.attached_pane
        pane.send_keys(command, enter=True)

    def detach(self):
        self.run_cmd("tmux detach")

    def kill(self):
        self.session.kill_session()
