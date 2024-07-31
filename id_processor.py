# id_processor.py

import pandas as pd
import random
import string
import sys

class IDProcessor:
    def __init__(self, input_file, reference_file):
        self.input_file = input_file
        self.output_file = input_file + '_output'
        self.rejected_file = input_file + '_rejected'
        self.mapping_file = input_file + '_mapping'
        self.reference_file = reference_file
        self.existing_ids, self.valid_id_length = self.load_reference_ids_and_length()
        self.id_mapping = {}

    def load_reference_ids_and_length(self):
        try:
            ref_df = pd.read_csv(self.reference_file, sep=r'\s+', header=None, dtype=str)
            ref_ids = set(ref_df[0].str.strip().tolist())
            valid_id_length = len(ref_df.iloc[0, 0].strip()) if not ref_df.empty else 0
            if valid_id_length == 0:
                print(f"Reference file {self.reference_file} is empty.")
                sys.exit(1)
            return ref_ids, valid_id_length
        except FileNotFoundError:
            print(f"Reference file {self.reference_file} not found.")
            sys.exit(1)

    def process_file(self):
        # Read the file with pandas, using regex to handle various delimiters
        df = pd.read_csv(self.input_file, sep=r'\s+', engine='python', header=None, dtype=str)
        df[0] = df[0].str.strip()  # Remove leading/trailing whitespace

        valid_rows = []
        rejected_rows = []

        for index, row in df.iterrows():
            original_id = row[0]
            content = row[1:].tolist()

            if self.is_valid(original_id):
                new_id = original_id
            else:
                new_id = self.generate_valid_id()
                self.id_mapping[new_id] = original_id
                rejected_rows.append([original_id] + content)

            self.existing_ids.add(new_id)
            valid_rows.append([new_id] + content)

        # Convert lists to DataFrames
        valid_df = pd.DataFrame(valid_rows)
        rejected_df = pd.DataFrame(rejected_rows)
        mapping_df = pd.DataFrame(list(self.id_mapping.items()), columns=['New ID', 'Original ID'])

        # Write DataFrames to files with proper encoding
        valid_df.to_csv(self.output_file, sep=' ', index=False, header=False, encoding='utf-8')
        rejected_df.to_csv(self.rejected_file, sep=' ', index=False, header=False, encoding='utf-8')
        mapping_df.to_csv(self.mapping_file, sep=' ', index=False, encoding='utf-8')

    def is_valid(self, id_value):
        return id_value.isdigit() and len(id_value) == self.valid_id_length and id_value not in self.existing_ids

    def generate_valid_id(self):
        while True:
            new_id = ''.join(random.choices(string.digits, k=self.valid_id_length))
            if new_id not in self.existing_ids:
                return new_id

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python id_processor.py <input_file> <reference_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    reference_file = sys.argv[2]

    processor = IDProcessor(input_file, reference_file)
    processor.process_file()
