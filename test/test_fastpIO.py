import pytest
import json
from contextlib import contextmanager
import abromics_galaxy_json_extractor


@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)


def test_fastp():
    toolname = "fastp"
    metadata = {"analysis_software_version": "0.23.2"}
    filename = "fastp_report.json"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"

    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())

    parsed_report = abromics_galaxy_json_extractor.parse(
        input,
        metadata,
        toolname)

    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert (
        parsed_report.abromics_results["results"][toolname]["content"]
        == load_json[0]["results"][toolname]["content"]
    )
