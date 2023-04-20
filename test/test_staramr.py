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


def test_staramr():
    toolname = "staramr"
    input_directory = "test/data/dummy/staramr"
    metadata = {
    "analysis_software_version": "0.9.1",
    "mlst_file_path":f"{input_directory}/mlst.tsv",
    "mlst_hid":"1234",
    "plasmidfinder_file_path":f"{input_directory}/plasmidfinder.tsv",
    "plasmid_hid":"Historic ID provided by Galaxy for plasmid file",
    "pointfinder_file_path":f"{input_directory}/pointfinder.tsv",
    "pointfinder_hid":"Historic ID provided by Galaxy for pointfinder file",
    "setting_file_path":f"{input_directory}/settings.txt"
    }
    filename = "resfinder.tsv"
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
    results_list = list(parsed_report.abromics_results["results"].keys())
    for result in results_list:
        assert parsed_report.abromics_results["results"][result]["content"] == load_json[0]["results"][result]["content"]