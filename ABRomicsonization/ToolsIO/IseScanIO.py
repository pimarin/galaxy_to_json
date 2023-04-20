#!/usr/bin/env python
import json
import re
import pandas as pd
from Bio import SeqIO
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "isescan_hid": "Historic ID for isescan file from galaxy",
    "analysis_software_version": "isescan version",
    "orf_fna_file": "fasta file with nucleotide orf sequences",
    "orf_fna_hid": "Historic ID for orf fasta file from galaxy",
    "orf_faa_file": "fasta file with amino acide orf sequences",
    "orf_faa_hid": "Historic ID for orf amino acid file from galaxy",
    "is_fna_file": "fasta file with nucleotide IS sequences",
    "is_fna_hid": "Historic ID for IS file from galaxy",
}


class IseScanIterator(AbromicsResultIterator):
    """IseScan tool parser
    Filter results from tabular file
    Could also parse:
    IS fna file
    orf faa file
    orf fna file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "isescan"
        self.metadata = metadata
        super().__init__(source, self.metadata)

        self.parse()

    def parse(self):
        """Extract information from IseScan tabular file
        and optionnal files
        """
        isescan_df = pd.read_table(self.stream, header=1)
        isescan_df = isescan_df.to_json(orient="records")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(isescan_df)

        if self.metadata["orf_fna_file"]:
            self.__check_input_files__(self.abromics_results["orf_fna_file"])
            extracted_infos = self.__get_fasta_infos__()
            self.abromics_results["results"]["orf_fna_file"] = {
                "name": "orf_fna",
                "file_path": self.abromics_results["orf_fna_file"],
                "hid": self.abromics_results.pop("orf_fna_hid"),
                "content": {extracted_infos},
            }
        if self.metadata["orf_faa_file"]:
            self.__check_input_files__(self.abromics_results["orf_faa_file"])
            extracted_infos = self.__get_fasta_infos__()
            self.abromics_results["results"]["orf_faa_file"] = {
                "name": "orf_fna",
                "file_path": self.abromics_results.pop("orf_faa_file"),
                "hid": self.abromics_results.pop("orf_faa_hid"),
                "content": extracted_infos,
            }
        if self.metadata["is_fna_file"]:
            self.__check_input_files__(self.abromics_results["is_fna_file"])
            extracted_infos = self.__get_fasta_infos__()
            self.abromics_results["results"]["is_fna_file"] = {
                "name": "is_fna",
                "file_path": self.abromics_results.pop("is_fna_file"),
                "hid": self.abromics_results.pop("is_fna_hid"),
                "content": extracted_infos,
            }

    def __get_fasta_infos__(self):
        """Extract fasta informations
        Extract name, sequences, positions
        and IS information
        Returns:
            dict: sequence informations
        """
        fasta_sequences = SeqIO.parse(self.stream, format="fasta")
        parsed_fasta_sequence = {}
        sequence_infos_names = [
            "contig",
            "start",
            "end",
            "strand",
            "family",
            "cluster",
        ]
        for seqname in fasta_sequences:
            sequence_infos = re.split(r"[ _]", seqname.description)
            parsed_fasta_sequence[sequence_infos[0]] = {
                "sequence_informations": dict(
                    zip(sequence_infos_names, sequence_infos)
                ),
                "sequence": seqname.seq.__str__(),
            }
        return parsed_fasta_sequence
