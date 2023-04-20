#!/usr/bin/env python
import json
import pandas as pd
from Bio import SeqIO
from ABRomicsonization.Interfaces import AbromicsResultIterator


required_metadata = {
    "plasmid_hid": "Historic ID for plasmidfinder file from galaxy",
    "analysis_software_version": "plasmidfinder version",
    "software_database_version": "plasmidfinder DB version",
    "genome_hit_file_path": (
        "fasta file with hits in genome, doesn't work for multiple input"
    ),
    "genome_hit_hid": "Historic ID for genome hit file from galaxy",
    "plasmid_sequence_file_path": (
        "fasta file with plasmid sequences, doesn't work for multiple input"
    ),
    "plasmid_hit_hid": "Historic ID for plasmid sequence hit file from galaxy",
}


class PlasmidFinderIterator(AbromicsResultIterator):
    """Plasmidfinder tool parser
    Filter results from Plasmidfinder json result
    Could also parse file for:
    Plasmid sequence hit file
    Genome sequence hit
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "plasmidfinder"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Parse plasmidfinder file"""
        # - analyse de l'input de base
        json_object = json.loads(self.stream.read())
        json_object = json_object[list(json_object.keys())[0]].pop("results")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json_object
        # - analyse de genome hit
        if self.metadata["genome_hit_file_path"]:
            self.__check_input_files__(
                self.abromics_results["genome_hit_file_path"]
            )
            extracted_infos = self.__get_fasta_infos__()
            self.abromics_results["results"]["genome_hit"] = {
                "name": "genome_hit",
                "file_path": self.abromics_results.pop("genome_hit_file_path"),
                "hid": self.abromics_results.pop("genome_hit_hid"),
                "content": extracted_infos,
            }

        # - analyse de plasmid hit
        if self.metadata["plasmid_sequence_file_path"]:
            self.__check_input_files__(
                self.metadata["plasmid_sequence_file_path"]
            )
            extracted_infos = self.__get_fasta_infos__()
            self.abromics_results["results"]["plasmid_sequence"] = {
                "name": "plasmid_hit",
                "file_path": self.abromics_results.pop(
                    "plasmid_sequence_file_path"
                ),
                "hid": self.abromics_results.pop("plasmid_hit_hid"),
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
        for seqname in fasta_sequences:
            sequence_infos = pd.DataFrame(seqname.description.split(" "))
            sequence_infos[[0, 1]] = sequence_infos[0].str.split(
                pat=":", n=1, expand=True
            )
            sequence_infos[[0, 1]] = sequence_infos[0].str.split(
                pat="=", n=1, expand=True
            )
            sequence_infos = sequence_infos.iloc[0:4, 0:2]
            sequence_infos = dict(zip(sequence_infos[0], sequence_infos[1]))
            sequence_name = list(sequence_infos.keys())[0]
            sequence_infos.pop(sequence_name)
            parsed_fasta_sequence[sequence_name] = {
                "sequence_informations": sequence_infos,
                "nucleotide_sequence": seqname.seq.__str__(),
            }
        return parsed_fasta_sequence
