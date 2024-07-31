#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <config_file>"
    exit 1
fi

# Assign arguments to variables
INPUT_FILE=$1
CONFIG_FILE=$2

# Load config variables
source "$CONFIG_FILE"

# Run the main processing script with the config variables
python3 id_processor.py "$INPUT_FILE" "$REFERENCE_ID_FILE"

# Define output filenames based on input filename
OUTPUT_FILE="${INPUT_FILE}_output"
MERGED_FILE="${INPUT_FILE}_merged"

# Concatenate reference SNP file and output file
cat "$REFERENCE_SNP_FILE" "$OUTPUT_FILE" > "$MERGED_FILE"

# Create qcf90 script file
QCF90_SCRIPT="qcf90_script.txt"
cat <<EOL > "$QCF90_SCRIPT"
--snpfile $MERGED_FILE
--pedfile $PEDFILE
--mapfile $MAPFILE
--exclude-chr $EXCLUDE_CHR
--crm $CRM
--cra $CRA
--maf $MAF
--hwep $HWEP
--save-clean $SAVE_CLEAN
EOL

# Run qcf90 with the generated script
qcf90 --script "$QCF90_SCRIPT"
