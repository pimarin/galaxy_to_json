import pandas as pd
from Bio import SeqIO
"""
Details to staramr input files
"""

class BlastHitColnames:
    def __init__(self):
        self.blast_colnames = ["seq_name",
                               "contig",
                               "contig_start",
                               "contig_end",
                               "database_gene_start",
                               "database_gene_end",
                               "hsp/length",
                               "pid",
                               "plength"
                               ]


class ResfinderFilter(BlastHitColnames):
    def __init__(self):
        super().__init__()
        __staramr_version__ = "0.9.1"
        self.resfinder_colnames = ["Isolate",
                              "ID",
                              "Gene",
                              "Predicted Phenotype",
                              "%Identity",
                              "%Overlap",
                              "HSP Length/Total Length",
                              "Contig",
                              "Start",
                              "End",
                              "Accession",
                              "Sequence"
                                   ]
    def read_blast_hit(self, fasta_file, start_col_num=4, end_col_num=6):
        blast_hit = SeqIO.parse(fasta_file, format="fasta")
        sequence_name_list = [seq_name.description.strip() for seq_name in blast_hit]
        sequence_dataframe = pd.DataFrame(sequence_name_list)
        sequence_dataframe = sequence_dataframe.iloc[:, 0].str.split(",", expand=True)
        sequence_dataframe.columns = self.blast_colnames
        self.filter_other_columns(sequence_dataframe)
        self.filter_sequence_name(sequence_dataframe)

    def read_resfinder_data(self, resfinder_dataframe):
        resfinder_dataframe


    def filter_sequence_name(self, dataframe):
        dataframe["accession"] = dataframe.iloc[:,0].str.split(" ").str[0].str.split("_", expand= True)[2]
        dataframe["seq_name"] = dataframe.iloc[:,0].str.split(" ").str[0].str.split("_", expand= True)[0]

    def filter_other_columns(self, dataframe):
        data_dimension = range(1, dataframe.shape[1])
        [self.keep_data_info(dataframe, column_index=dim) for dim in data_dimension]

    def keep_data_info(self, dataframe, column_index: int, strip_char=": "):
        dataframe.iloc[:, column_index] = dataframe.iloc[:, column_index].str.split(strip_char).str[1]

class MlstFilter:

    def __init__(self):
        self.mlst_colnames = [
                                "Isolate",
                                "ID",
                                "Scheme",
                                "Sequence Type",
                                "Locus",
                             ]

        def read_mlst_file(self):
            mlst_dataframe = pd.read_table(mlst, delimiter="\t")

            colname_differences = set(mlst_dataframe) ^ set(mlst_colnames)

class PlasmidfinderFilter(BlastHitColnames):
    def __init__(self):
        super().__init__()
        self.plasmidfinder_colnames = [
                                        "Isolate",
                                        "ID",
                                        "Scheme",
                                        "Sequence Type",
                                        "Locus",
                                      ]




resfinder ="/home/pierre/PycharmProjects/galaxy_to_json/tests/e_faecalis/resfinder.tsv"
fasta_file ="/home/pierre/PycharmProjects/galaxy_to_json/tests/e_faecalis/hits/resfinder_10_Enterococcus_faecalis.fa"