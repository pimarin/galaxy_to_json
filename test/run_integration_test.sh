#!/bin/bash
set -e


abromics abricate test/data/dummy/abricate/report.tsv --output abricate_output.json
abromics fastp test/data/dummy/fastp/fastp_report.json --output abricate_output.json
