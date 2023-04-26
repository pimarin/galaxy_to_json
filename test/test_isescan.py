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


def test_isescan():
    toolname = "isescan"
    directory = "test/data/dummy/isescan"
    metadata = {"analysis_software_version": "1.7.2.3",
                "orf_fna_file": f"{directory}/orf.fna",
                "orf_faa_file": f"{directory}/orf.faa",
                "is_fna_file": f"{directory}/is.fna"}
    
    filename = "results.tsv"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"
    
    with open(output_report, "r") as output:
        load_json = json.loads(output.read())
        
    parsed_report = abromics_galaxy_json_extractor.parse(
        input, 
        metadata, 
        toolname
        )
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    results_list = list(parsed_report.abromics_results["results"].keys())
    for result in results_list:
        assert parsed_report.abromics_results["results"][result]["content"] == load_json[0]["results"][result]["content"]