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


def test_bracken_alone():
    toolname = "bracken"
    metadata = {
        "analysis_software_version": "2.8",
        "reference_database_version": "PlusPF_16",
        }
    filename = "bracken_report.tsv"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_alone_output.json"
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = ABRomicsonization.parse(
        input, 
        metadata, 
        toolname
        )
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]

def test_bracken_full():
    toolname = "bracken"
    metadata = {
        "analysis_software_version": "2.8",
        "reference_database_version": "PlusPF_16",
        "kraken_report_path":"test/data/dummy/bracken/bracken_kraken_report.tsv"
        }
    filename = "bracken_report.tsv"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_full_output.json"
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = ABRomicsonization.parse(
        input, 
        metadata, 
        toolname
        )
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]
    assert parsed_report.abromics_results["results"]["kraken2_estimated"]["content"] == load_json[0]["results"]["kraken2_estimated"]["content"]