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


import sqlite3


def load_tsv_to_sqlite(tsv_dir, db_name, table_name, primary_key):
    """
    Load TSV files from a directory into a SQLite database.
    
    Args:
        tsv_dir (str): The directory where the TSV files are located.
        db_name (str): The name of the SQLite database.
        table_name (str): The name of the table in the SQLite database where the data will be inserted.
        primary_key (str): The name of the column to be set as the primary key in the table.

    Returns:
        None
    """

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_name)

    # Create a cursor object
    cur = conn.cursor()

    # Create the table with the specified column as the primary key
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {primary_key} TEXT PRIMARY KEY
        )
    """)

    # Get all files in the specified directory
    files = os.listdir(tsv_dir)

    # Filter the list of files to include only TSV files
    tsv_files = [file for file in files if file.endswith('.tsv')]

    # Iterate over each TSV file
    for tsv_file in tsv_files:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(os.path.join(tsv_dir, tsv_file), sep='\t')

        # Write the DataFrame to the SQLite database
        df.to_sql(table_name, conn, if_exists='append', index=False)

    # Print the first 10 records of the table
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 10", conn)
    print(df)

    # Print the schema of the table
    cur.execute(f"PRAGMA table_info({table_name})")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # Close the connection to the SQLite database
    conn.close()
