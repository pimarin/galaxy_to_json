<p align="center">
  <img src=images/ABRomics_logo.svg />
</p>


# ABRomicsonization

This repository contains abromic converter tool, to parse some tool results to a json readable file format.
It was initially developped to be used on [galaxy](https://galaxyproject.org/) and some option are only available in Galaxy (e.g. extract the historic ID from a galaxy analysis)
All the metadata related to tools are optionals.
It can analyse some differents kinds of tools (14 + 1 generic tool for tabular files as of 2023-04-20).
It can produce both a single file to each tool or a summarized file in json format for all report provided

# Installation
## Requirement
- python = 3.9
- pandas = 1.4.3
- biopython = 1.81


The tool could be download using conda:
```
mamba create --name abromicsonization --channel bioconda abromicsonization
```
You can also download from gith repository:
```
git clone mon lien github
pip install abromicsonization
```
## Galaxy version
This tool is also available for [galaxy](https://galaxyproject.org/) using the [toolshed](https://toolshed.g2.bx.psu.edu/repository?repository_id=7793bb09fbee1504&changeset_revision=08bc877b2c5b)

# Usage
```
usage: abromics <tool> <options>

Convert ABRomics workflow results tool output(s) to abromics specificationformat

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Tools with abromics reports:
  {abricate,plasmidfinder,shovill,staramr,fastp,quast,refseqmasher,bandage,bakta,integronfinder2,isescan,kraken2,bracken,recentrifuge,tabular_file,tooltest,summarize}
    abricate            abromics abricate's output report i.e., OUTPUT.tsv
    plasmidfinder       abromics plasmidfinder's output report i.e., plasmidfinder.tsv
    shovill             abromics shovill's output report i.e., contig.fasta
    staramr             abromics staramr's output report i.e., resfinder.tsv
    fastp               abromics fastp's output report i.e., report.json
    quast               abromics quast's output report i.e., report.tsv
    refseqmasher        abromics refseqmasher's output report i.e., OUTPUT.tsv
    bandage             abromics bandage's output report i.e., OUTPUT.txt
    bakta               abromics bakta's output report i.e., OUTPUT.json
    integronfinder2     abromics integronfinder2's output report i.e., OUTPUT.integrons, OUTPUT.summary
    isescan             abromics isescan's output report i.e., OUTPUT.tsv
    kraken2             abromics kraken2's output report i.e., report.tsv
    bracken             abromics bracken's output report i.e., report.tsv
    recentrifuge        abromics recentrifuge's output report i.e., data.tsv
    tabular_file        abromics tabular_file's output report i.e., report.tsv
    tooltest            abromics tooltest's output report i.e., unitest
    summarize           Provide a list of paths to the reports you wish to summarize
```
To look at a specific tool e.g. abricate:
```
> abromics abricate --help
usage: abromics.py abricate <options>

Applies abromics specification to output(s) from abricate (OUTPUT.tsv)

positional arguments:
  report                Path to report(s)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output location
  --analysis_software_version ANALYSIS_SOFTWARE_VERSION
                        abricate version for abricate
  --reference_database_version REFERENCE_DATABASE_VERSION
                        DB version for abricate
  --abricate_hid ABRICATE_HID
                        historic ID for abricate file from galaxy for abricate
```

```
abromics abricate test/data/dummy/abricate/report.tsv --reference_database_version 3.2.5 --analysis_software_version 1.0.0
```

To parse multiple reports from the same tool at once just give a list of reports as the argument.
```
abromics abricate test/data/dummy/abricate/*.tsv --reference_database_version 3.2.5 --analysis_software_version 1.0.0
```
It will generate only one json file for all reports
You can also summarize all json from differents tools in one final json file
```
> abromics summarize --help
Concatenate and summarize AMR detection reports

positional arguments:
  abromics_reports      list of abromics reports

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path for summary
  -f FORCE, --force FORCE
                        Overwrite to the output file mandatory
```
```
abromics summarize test/data/dummy/summarize/*output.json -o test/data/raw_output/summarize/abromics_summary.json
```
# Special cases
abromicsonization take some different kind of tools to generate a parsed json.
There are several limitations related to the finale size of json file or type of parsed results
## Tools with more than one type of input files
Caution : when you can provied different kind of file to a tool (e.g. shovill option use the contig.fasta, but can also use the alignment bam and assembly graph file), you canno't submit in multiple file mode. Only provid one result file with related optional file.
### Bakta

Bakta tool generate a complete json file in output, but could be so big to a database integration and also redondant with other tool results.
The Bakta parser, uses some informations from the bakta json file, it could add summary of the analysis if provided in summary file from bakta (optional), but remove information related to nucleotide and amino acid sequences. It could add path of the sequences files instead (optional)

## bakta
```
abromics bakta --help

Applies abromics specification to output(s) from bakta (OUTPUT.json)

positional arguments:
  report                Path to report(s)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output location
  --bakta_hid BAKTA_HID
                        historic ID to bakta result file from galaxy for bakta
  --analysis_software_version ANALYSIS_SOFTWARE_VERSION
                        bakta version for bakta
  --reference_database_version REFERENCE_DATABASE_VERSION
                        DB version for bakta
  --summary_result_path SUMMARY_RESULT_PATH
                        summary file of the bakta analysis in txt format for bakta
  --summary_hid SUMMARY_HID
                        historic ID for summary file from galaxy for bakta
  --gff_file_path GFF_FILE_PATH
                        annotation file result in gff3 format for bakta
  --gff_hid GFF_HID     historic ID for gff file from galaxy for bakta
  --nucleotide_annotation_path NUCLEOTIDE_ANNOTATION_PATH
                        nuleotide file of the annotation for bakta
  --nucleotide_hid NUCLEOTIDE_HID
                        historic ID for nucleotide file from galaxy for bakta
  --amino_acid_annotation_path AMINO_ACID_ANNOTATION_PATH
                        amino acid file of the annotation for bakta
  --amino_hid AMINO_HID
                        historic ID for amino acide sequence file from galaxy for bakta

```

Please cite the ABRomics project when using the tool
# contact
You can contact the ABRomics team to [abromics@abromics.fr](mailto:abromics@abromics.fr)

# Parser Authorship Information

All reimplemented by @fmaguire in refactored code.

Original parser and mapping authors:
- AbricateIO.py: @dfornika 
- AmrFinderPlusIO.py: @dfornika @fmaguire
- AmrPlusPlusIO.py: @fmaguire
- AribaIO.py: @fmaguire
- CSStarIO.py: @fmaguire
- DeepArgIO.py: @fmaguire
- GrootIO.py: @fmaguire
- KmerResistanceIO.py: @fmaguire
- ResFamsIO.py: @fmaguire
- ResFinderIO.py: @raphenya @fmaguire
- PointFinderIO.py: @fmaguire
- RgiIO.py: @dfornika @raphenya @fmaguire
- SraxIO.py: @fmaguire
- Srst2IO.py: @fmaguire
- StarAmrIO.py: @fmaguire
- TBProfilerIO.py: @jodyphelan
- MykrobeIO.py: @pvanheus
