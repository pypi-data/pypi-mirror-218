from diz.utils import shell


def test_current():
    assert shell.current() == ('zsh', '/bin/zsh')