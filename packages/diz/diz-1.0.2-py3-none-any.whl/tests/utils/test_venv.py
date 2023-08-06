from diz.utils import venv


def test_get_activate_command():
    assert venv.get_activate_command('venv') == 'source venv/bin/activate'
