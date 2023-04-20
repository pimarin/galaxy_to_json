import pytest
from unittest.mock import patch
from contextlib import contextmanager
from ABRomicsonization.abromics import main

@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)
    
def test_abromics_main(capsys):
    with patch("sys.argv", ["main", "abricate", "--help"]):
        main()
        captured = capsys.readouterr()
        assert captured.out == "Hello Jürgen\n"

