import pytest
import unittest
from contextlib import contextmanager
import ABRomicsonization

@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)

class TestParserOptions(unittest.TestCase):

    def test_parser_error_isinstance(self):
        toolname = int(1234)
        metadata = {}
        filename = "input_file.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"

        try:
            parsed_report = ABRomicsonization.parse(
                input,
                metadata,
                toolname
                )
        except TypeError:
            assert not isinstance(toolname, str)

    def test_parser_error_metadata(self):
        toolname = "None"
        metadata = None
        filename = "input_file.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"

        try:
            parsed_report = ABRomicsonization.parse(
                input,
                metadata,
                toolname
                )
        except TypeError:
            assert not isinstance(metadata, dict)

    def test_parser_error_notool(self):
        toolname=""
        metadata = {}
        filename = "input_file.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"

        try:
            parsed_report = ABRomicsonization.parse(
                input,
                metadata,
                tool=toolname
                )
        except ValueError:
            self.assertEqual(toolname, '')

    def test_parser_error_lowertool(self):
        toolname = "MYTOOL"
        metadata = {}
        filename = "input_file.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"

        try:
            parsed_report = ABRomicsonization.parse(
                input,
                metadata,
                toolname
                )
        except ValueError:
            assert not toolname.islower()

    def test_parser_error_requiredmetadata(self):
        toolname = "anothertool"
        metadata = {
                    "analysis_software_version": "1.0",
                    "reference_database_version":"1.0"
                    }
        filename = "report.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"
        try:
            ABRomicsonization.parse(
                input,
                metadata,
                toolname
                )
        except ValueError:
            assert toolname not in ABRomicsonization._RequiredToolMetadata.keys()

    def test_parser_error_unknowtool(self):
        toolname = "tooltest"
        metadata = {
                    "analysis_software_version": "1.0",
                    "reference_database_version":"1.0"
                    }
        filename = "report.tsv"
        input = f"test/data/dummy/{toolname}/{filename}"

        try:
            parsed_report = ABRomicsonization.parse(
                input,
                metadata,
                toolname
                )
        except ValueError:
            assert toolname not in ABRomicsonization._FormatToIterator.keys()


if __name__ == '__main__':
    unittest.main()
