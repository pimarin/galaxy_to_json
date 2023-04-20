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


def test_recentrifuge():
    toolname = "recentrifuge"
    input_dir = "test/data/dummy/recentrifuge"
    metadata = {
        "rcf_stat_file_path":f"{input_dir}/rcf_stat.tsv",
        "rcf_html_path":f"{input_dir}/rcf_report.html",
    }
    filename = "rcf_data.tsv"
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