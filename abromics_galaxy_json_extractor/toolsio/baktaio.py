#!/usr/bin/env python
import json
import pandas as pd
from abromics_galaxy_json_extractor.interfaces import (
    AbromicsResultIterator,
)

required_metadata = {
    "bakta_hid": "historic ID to bakta result file from galaxy",
    "analysis_software_version": "bakta version",
    "reference_database_version": "DB version",
    "summary_result_path": "summary file of the bakta analysis in txt format",
    "summary_hid": "historic ID for summary file from galaxy",
    "gff_file_path": "annotation file result in gff3 format",
    "gff_hid": "historic ID for gff file from galaxy",
    "nucleotide_annotation_path": "nuleotide file of the annotation",
    "nucleotide_hid": "historic ID for nucleotide file from galaxy",
    "amino_acid_annotation_path": "amino acid file of the annotation",
    "amino_hid": "historic ID for amino acide sequence file from galaxy",
}


class BaktaIterator(AbromicsResultIterator):
    """Bakta tool parser
    Filter results from bakta json output file
    Could also filter file for:
    summary file
    gff annotation file
    nucleotide sequence file
    amino acid sequence file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "bakta"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Extract information from bakta json file
        Add some optionnal informations if provided
        Add summary result with global result
        Add path for gff3 file
        Add path for nucleotide sequences
        Add path for amino acid sequences
        """
        # skip any manually specified fields for later
        with open(self.source, "r") as f:
            bakta_load = json.loads(f.read())
        bakta_load = json.loads(self.stream.read())
        bakta_load.pop("sequences")
        features_df = pd.DataFrame.from_records(bakta_load["features"])
        features_df = features_df.drop(["nt", "aa"], axis=1)
        features_json = features_df.to_json(orient="records")
        bakta_load["features"] = json.loads(features_json)

        if self.abromics_results["analysis_software_version"] == "":
            self.abromics_results["analysis_software_version"] = bakta_load[
                "version"
            ].pop("bakta")
        if self.abromics_results["reference_database_version"] == "":
            self.abromics_results["reference_database_version"] = bakta_load[
                "version"
            ].pop("db")
        bakta_load.pop("version")

        if self.metadata["summary_result_path"]:
            self._check_input_files(self.metadata["summary_result_path"])
            summary_df = pd.read_table(self.stream, header=7)
            summary_df = summary_df["Annotation:"].str.split(
                pat=":", n=1, expand=True
            )
            summary_df = summary_df.replace(" ", "")
            # Indexes
            start_row = 0
            end_row = summary_df[summary_df[0] == "Bakta"].index[0]
            start_col = 0
            end_col = 2
            summary_df = summary_df.iloc[
                start_row:end_row,
                start_col:end_col,
            ]
            sequence_dic = dict(zip(summary_df[0], summary_df[1]))
            bakta_load["summary"] = sequence_dic
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = bakta_load
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("bakta_hid")

        if self.metadata["gff_file_path"]:
            self._check_input_files(self.metadata["gff_file_path"])
            self.abromics_results["results"]["gff_file_path"] = {
                "name": "gff3",
                "file_path": self.abromics_results.pop("gff_file_path"),
                "hid": self.abromics_results.pop("gff_hid"),
                "content": {},
            }
        if self.metadata["nucleotide_annotation_path"]:
            self._check_input_files(
                self.metadata["nucleotide_annotation_path"]
            )
            self.abromics_results["results"]["nucleotide_annotation_path"] = {
                "name": "nucleotide",
                "file_path": self.abromics_results.pop(
                    "nucleotide_annotation_path"
                ),
                "hid": self.abromics_results.pop("nucleotide_hid"),
                "content": {},
            }
        if self.metadata["amino_acid_annotation_path"]:
            self._check_input_files(
                self.metadata["amino_acid_annotation_path"]
            )
            self.abromics_results["results"]["amino_acid_annotation_path"] = {
                "name": "amino_acid",
                "file_path": self.abromics_results.pop(
                    "amino_acid_annotation_path"
                ),
                "hid": self.abromics_results.pop("amino_hid"),
                "content": {},
            }
