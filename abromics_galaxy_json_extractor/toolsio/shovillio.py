#!/usr/bin/env python

from Bio import SeqIO
import re
from abromics_galaxy_json_extractor.interfaces import (
    AbromicsResultIterator,
)

required_metadata = {
    "contigs_hid": "Historic ID to shovill contigs file from Galaxy",
    "analysis_software_version": "shovill version number",
    "contig_graph_path": "Assembly graph file",
    "contig_graph_hid": "Historic ID to assembly graph from Galaxy",
    "bam_file_path": "Binary Alignment file from shovill",
    "bam_hid": "Historic ID to alignment file from Galaxy",
}


class ShovillIterator(AbromicsResultIterator):
    """Shovill tool parser
    Filter results from contig fasta file
    Could also keep path for:
    Alignemnt file (bam format)
    Contig graph file (gfa format)
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "shovill"
        self.metadata = metadata
        super().__init__(source, metadata)

        self.parse()

    def parse(self):
        """Assembly shovill parser
        Read contig assembly file to extract informations and sequences
        Could also add path information for
        BAM file and GFA file
        """

        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = self.__get_fasta_infos__()
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("contigs_hid")

        if self.metadata["contig_graph_path"]:
            self._check_input_files(self.metadata["contig_graph_path"])
            self.abromics_results["results"]["contig_graph"] = {
                "name": "contig_graph",
                "file_path": self.abromics_results.pop("contig_graph_path"),
                "hid": self.abromics_results.pop("contig_graph_hid"),
                "content": "",
            }

        if self.metadata["bam_file_path"]:
            self._check_input_files(self.metadata["bam_file_path"])
            self.abromics_results["results"]["alignment"] = {
                "name": "alignment",
                "file_path": self.abromics_results.pop("bam_file_path"),
                "hid": self.abromics_results.pop("bam_hid"),
                "content": "",
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
            seq_results = {}
            seq_results["length"] = len(seqname.seq)
            seq_results["coverage"] = float(
                re.match(
                    r".*cov=([0-9.]*)",
                    seqname.description,
                ).group(1)
            )
            seq_results["sequence"] = seqname.seq.__str__()
            parsed_fasta_sequence[seqname.id] = seq_results
        return parsed_fasta_sequence
