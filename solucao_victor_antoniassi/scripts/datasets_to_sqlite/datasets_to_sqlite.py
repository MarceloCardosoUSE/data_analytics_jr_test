import os
import pandas as pd
from unidecode import unidecode

def remove_special_characters(input_directory, output_directory, delimiter='\t', encoding='latin-1'):
    """
    Removes special characters and accents from the column values of all CSV and TSV files in a directory,
    and saves the data back into TSV files.

    Args:
        input_directory (str): Path to the directory with the CSV and TSV files.
        output_directory (str): Path to the directory where the TSV files will be saved.
        delimiter (str, optional): Delimiter used in the files. Default is '\t'.
        encoding (str, optional): Encoding used in the files. Default is 'latin-1'.

    Returns:
        None
    """
    # Iterates over the files in the input directory
    for file in os.listdir(input_directory):
        # Processes only CSV and TSV files
        if file.endswith('.csv') or file.endswith('.tsv'):
            # Gets the full path of the file
            file_path = os.path.join(input_directory, file)
            # Reads the file into a DataFrame
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
            # Removes accents from each string value in the DataFrame
            df = df.apply(lambda x: x.map(lambda y: unidecode(y) if isinstance(y, str) else y))
            # Defines the name of the output file
            tsv_file_name = os.path.join(output_directory, file.rsplit('.', 1)[0] + '.tsv')
            # Saves the DataFrame to the output file
            df.to_csv(tsv_file_name, sep='\t', index=False, encoding=encoding)
