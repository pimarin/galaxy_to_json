import pytest
import json
from contextlib import contextmanager
import ABRomicsonization

@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)


def test_bandage():
    toolname = "bandage"
    metadata = {"analysis_software_version": "1.0"}
    filename = "bandage_info.txt"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"

    
    with open(output_report, "r") as output:
        load_json = json.loads(output.read())
        
    parsed_report = ABRomicsonization.parse(
        input, 
        metadata, 
        toolname
        )
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]