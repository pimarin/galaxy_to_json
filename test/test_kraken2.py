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


def test_kraken2():
    toolname = "kraken2"
    metadata = {
        "analysis_software_version": "2.1.2",
        "reference_database_version": "PlusPF_16",
        "seq_classification_file_path":"test/data/dummy/kraken2/taxonomy_result.tsv",
        "classification_hid":"historic ID for read classification file from Galaxy"}
    filename = "taxonomy_report.tsv"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = ABRomicsonization.parse(
        input, 
        metadata, 
        toolname
        )
    
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]
    assert parsed_report.abromics_results["results"]["seq_classification"]["content"] == load_json[0]["results"]["seq_classification"]["content"]