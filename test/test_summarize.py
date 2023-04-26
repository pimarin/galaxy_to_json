import pytest
import json
from contextlib import contextmanager
import glob
import os
import abromics_galaxy_json_extractor

@contextmanager
def not_raises(exception, msg):
    try:
        yield
    except exception:
        raise pytest.fail(msg)
    
toolname="summarize"
input_directory="test/data/dummy"
output_directory="test/data/raw_outputs"
input_files = glob.glob(pathname=f"{input_directory}/{toolname}/*_output.json")
output_report = f"{output_directory}/{toolname}"
output_report_test_path = f"{output_report}/abromics_summary_test.json"
output_report_path = f"{output_report}/abromics_summary.json"
            
def items_extraction(data_list, use_key="analysis_software_name", use_value="results"):
    extracted_items = {}
    for elmts in data_list:
        for result in elmts:
            extracted_items[result[use_key]] = result[use_value]
    return extracted_items

def test_summarize():

    with open(output_report_path, "r") as input_file:
        load_json = json.loads(input_file.read())
    parsed_report = abromics_galaxy_json_extractor.summarize.ReportSummary(
        report_list=input_files,
        output_location=output_report_test_path
        )
    parsed_report.export_summary()
    extracted_from_summary = items_extraction(parsed_report.summary_json_list)
    extracted_from_json = items_extraction(load_json)
    os.remove(output_report_test_path)
    assert extracted_from_summary.items() == extracted_from_json.items()

def test_output_path_summarize():
    parsed_report = abromics_galaxy_json_extractor.summarize.ReportSummary(
        report_list=input_files,
        output_location=output_report)
    
    path_not_exist = f"{output_report}/no_file.json"
    parsed_report._output_location = path_not_exist
    out_fh = parsed_report._check_output_path()
    assert out_fh.mode == "w"
    try:
        parsed_report._check_output_path()
    except ValueError:
        assert os.path.exists(parsed_report._output_location)        
    finally:
        parsed_report._overwrite = True
        out_fh = parsed_report._check_output_path()
        assert out_fh.mode == "a"
    os.remove(out_fh.name)
    path_is_dir = output_report
    parsed_report._output_location = path_is_dir
    try:
        parsed_report._check_output_path()
    except FileExistsError:
        assert os.path.exists(parsed_report._output_location)
    finally:
        parsed_report._default_location = output_report_test_path
        out_fh = parsed_report._check_output_path()
        assert os.path.exists(out_fh .name)
        os.remove(out_fh.name)

def test_check_input_file():
    empty_file = f"{input_directory}/{toolname}/empty_file.json"
    parsed_report = abromics_galaxy_json_extractor.summarize.ReportSummary(
        report_list=empty_file)
    assert parsed_report._check_input_files(empty_file) == 0
    assert os.stat(parsed_report._report_list).st_size == 0
    no_file_exist = f"{input_directory}/{toolname}/no_file.json"
    try:
        parsed_report._check_input_files(no_file_exist)
    except FileNotFoundError:
        assert os.path.exists(no_file_exist) == False
    
    
