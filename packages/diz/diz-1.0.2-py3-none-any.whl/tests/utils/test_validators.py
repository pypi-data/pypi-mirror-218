from diz.utils import validators


def test_is_valid_url():
    assert validators.is_valid_url('https://github.com') is True