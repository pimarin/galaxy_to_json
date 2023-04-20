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


def test_plasmidfinder():
    toolname = "plasmidfinder"
    metadata = {"analysis_software_version": "1.0",
                     "software_database_version": "1.0",
                     "genome_hit_file_path": f"test/data/dummy/{toolname}/genome_hit.fasta",
                     "plasmid_sequence_file_path": f"test/data/dummy/{toolname}/plasmid_hit.fasta"}
    filename = "plasmidfinder_result.json"
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
    results_list = list(parsed_report.abromics_results["results"].keys())
    for result in results_list:
        assert parsed_report.abromics_results["results"][result]["content"] == load_json[0]["results"][result]["content"]