import pytest
import json
from contextlib import contextmanager
from abromics_galaxy_json_extractor.interfaces import AbromicsResultIterator

@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)


def test_check_input():
    AbromicsResultIterator.__abstractmethods__ = set()
    