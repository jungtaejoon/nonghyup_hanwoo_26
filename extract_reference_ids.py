# extract_reference_ids.py

import pandas as pd
import sys


def extract_reference_ids(reference_input_file, reference_output_file):
    try:
        ref_df = pd.read_csv(reference_input_file, sep=r'\s+', header=None, dtype=str)
        ref_df[0] = ref_df[0].str.strip()  # Remove leading/trailing whitespace
        ref_df[[0]].to_csv(reference_output_file, sep='\t', index=False, header=False, encoding='utf-8')
        print(f"Extracted {len(ref_df)} reference IDs to {reference_output_file}")
    except FileNotFoundError:
        print(f"File {reference_input_file} not found.")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python extract_reference_ids.py <reference_input_file> <reference_output_file>")
        sys.exit(1)

    reference_input_file = sys.argv[1]
    reference_output_file = sys.argv[2]

    extract_reference_ids(reference_input_file, reference_output_file)