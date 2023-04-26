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


def test_shovillio():
    toolname="shovill"
    input_directory = "test/data/dummy/shovill"
    metadata = {
    "analysis_software_version":"1.1.0",
    "contig_graph_path":f"{input_directory}/contigs.gfa",
    "bam_file_path":f"{input_directory}/alignment.bam"
    }
    shovill_filename = "contigs.fa"
    shovill_input = f"{input_directory}/{shovill_filename}"
    shovill_output_report = f"test/data/raw_outputs/{toolname}/{toolname}_output.json"
    
    with open(shovill_output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = abromics_galaxy_json_extractor.parse(
        shovill_input, 
        metadata, 
        toolname
        )
       
    assert parsed_report.abromics_results["analysis_software_version"] == "1.1.0"
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    results_list = list(parsed_report.abromics_results["results"].keys())
    for result in results_list:
        assert parsed_report.abromics_results["results"][result]["content"] == load_json[0]["results"][result]["content"]