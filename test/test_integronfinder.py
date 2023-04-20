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


def test_integronfinder2():
    toolname = "integronfinder2"
    filename = "results.integrons"
    input = f"test/data/dummy/{toolname}/{filename}"
    summary_file = "results.summary"
    summary_path = f"test/data/dummy/{toolname}/{summary_file}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"
    metadata = {"analysis_software_version": "1.6.1",
                "summary_file_path":summary_path
                }
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = ABRomicsonization.parse(
        input, 
        metadata, 
        toolname
        )
    
    results_list = list(parsed_report.abromics_results["results"].keys())
    
    for result in results_list:
        assert parsed_report.abromics_results["results"][result]["content"] == load_json[0]["results"][result]["content"]
        
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
            
            
            