import pytest

from wdmapper import run, __version__


def test_help_as_default(capsys):
    with pytest.raises(SystemExit):
        run()
    out, err = capsys.readouterr()
    assert out.startswith('usage: ')


def test_help_as_command(capsys):
    with pytest.raises(SystemExit):
        run('help')
    out, err = capsys.readouterr()
    assert out.startswith('usage: ')


def test_unknown_command(capsys):
    with pytest.raises(SystemExit):
        run('x', 'P1', 'P2')
    out, err = capsys.readouterr()
    assert err.startswith('command must be one of ')
