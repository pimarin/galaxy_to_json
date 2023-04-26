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


def test_bakta_alone():
    toolname = "bakta"
    metadata = {
                "summary_result_path":"",
                "gff_file_path":"",
                "nucleotide_annotation_path":"",
                "amino_acid_annotation_path":""
                }
    filename = "bakta.json"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_only_output.json"
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = abromics_galaxy_json_extractor.parse(
        input, 
        metadata, 
        toolname
        )
    
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]
            
def test_bakta_full():
    toolname = "bakta"
    metadata = {
                "analysis_software_version": "1.7.0",
                "reference_database_version":"4.0",
                "summary_result_path":"test/data/dummy/bakta/bakta_summary.txt",
                "gff_file_path":"test/data/dummy/bakta/bakta_annotation.gff3",
                "nucleotide_annotation_path":"test/data/dummy/bakta/bakta_nucleotide.fasta",
                "amino_acid_annotation_path":"test/data/dummy/bakta/bakta_aminoacid.faa"}
    filename = "bakta.json"
    input = f"test/data/dummy/{toolname}/{filename}"
    output_report = f"test/data/raw_outputs/{toolname}/{toolname}_all_output.json"
        
    with open(output_report, "r") as input_file:
        load_json = json.loads(input_file.read())
        
    parsed_report = abromics_galaxy_json_extractor.parse(
        input, 
        metadata, 
        toolname
        )
    assert parsed_report.abromics_results["analysis_software_name"] == toolname
    assert parsed_report.abromics_results["analysis_software_version"] == "1.7.0"
    assert parsed_report.abromics_results["reference_database_version"] == "4.0"
    assert parsed_report.abromics_results["results"][toolname]["content"] == load_json[0]["results"][toolname]["content"]
            
            