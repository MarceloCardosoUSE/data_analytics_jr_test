import os
import pandas as pd
from unidecode import unidecode
import sqlite3


def remove_special_characters(input_directory, output_directory, delimiter='\t', encoding='latin-1'):
    """
    Remove special characters and accents from the column values of all CSV and TSV files in a directory,
    and save the data back into TSV files.

    Parameters:
        input_directory (str): Path to the directory with the CSV and TSV files.
        output_directory (str): Path to the directory where the TSV files will be saved.
        delimiter (str, optional): Delimiter used in the files. Default is '\t'.
        encoding (str, optional): Encoding used in the files. Default is 'latin-1'.

    Returns:
        None
    """
    # Iterate over the files in the input directory
    for file in os.listdir(input_directory):
        # Process only CSV and TSV files
        if file.endswith('.csv') or file.endswith('.tsv'):
            
            # Get the full path of the file
            file_path = os.path.join(input_directory, file)
            
            # Read the file into a DataFrame
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
            
            # Remove accents from each string value in the DataFrame
            df = df.apply(lambda x: x.map(lambda y: unidecode(y) if isinstance(y, str) else y))
            
            # Define the name of the output file
            tsv_file_name = os.path.join(output_directory, file.rsplit('.', 1)[0] + '.tsv')
            
            # Save the DataFrame to the output file
            df.to_csv(tsv_file_name, sep='\t', index=False, encoding=encoding)


def load_tsv_to_sqlite(tsv_dir, db_name, table_name, primary_key=None):
    """
    Load TSV files from a directory into a SQLite database.

    Parameters:
        tsv_dir (str): The directory where the TSV files are located.
        db_name (str): The name of the SQLite database.
        table_name (str): The name of the table in the SQLite database where
                          the data will be inserted.
        primary_key (str, optional): The name of the column to be set as the primary key
                           in the table. If not provided, an artificial primary
                           key called 'ID_EDUCANDOS' will be created.

    Returns:
        None
    """
    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_name)

    # Create a cursor object
    cur = conn.cursor()

    # If no primary_key is provided, create an artificial one called 'ID_EDUCANDOS'
    if primary_key is None:
        primary_key = 'ID_EDUCANDOS'

    # Get all files in the specified directory
    files = os.listdir(tsv_dir)

    # Filter the list of files to include only TSV files
    tsv_files = [file for file in files if file.endswith('.tsv')]

    # Iterate over each TSV file
    for tsv_file in tsv_files:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(os.path.join(tsv_dir, tsv_file), sep='\t')

        # If no primary_key was provided, create an artificial one
        if primary_key == 'ID_EDUCANDOS' and primary_key not in df.columns:
            df.insert(0, 'ID_EDUCANDOS', range(1, len(df) + 1))

        # Write the DataFrame to the SQLite database
        df.to_sql(table_name, conn, if_exists='replace', index=False)

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

# Usage of the function:
# load_tsv_to_sqlite('datasets_tratados\\educandos\\tratados_python', 'escolas_educandos_sqlite.db', 'educandos')


def create_escolas_educandos_table():
    """
    This function creates a new table named 'escolas_educandos' in a SQLite database.
    The new table is based on two existing tables: 'escolas' and 'educandos'.
    The function keeps only one column for each name, except for the columns called DATABASE, which are differentiated by aliases.
    The common key between the tables is CODESC.

    Returns:
    None
    """

    # Connect to the SQLite database 'escolas_educandos_sqlite.db'
    conn = sqlite3.connect('escolas_educandos_sqlite.db')

    # Create a cursor object to execute SQL commands
    cur = conn.cursor()

    # Get the column names of the 'escolas' table
    cur.execute("PRAGMA table_info(escolas)")
    columns_escolas = [column[1] for column in cur.fetchall()]

    # Get the column names of the 'educandos' table
    cur.execute("PRAGMA table_info(educandos)")
    columns_educandos = [column[1] for column in cur.fetchall()]

    # Find the common columns between the 'escolas' and 'educandos' tables, except 'DATABASE'
    common_columns = list(set(columns_escolas) & set(columns_educandos))
    if 'DATABASE' in common_columns: common_columns.remove('DATABASE')

    # Create the column list for the SQL query
    columns_sql = []

    # Add the columns of the 'escolas' table to the list, differentiate 'DATABASE' column
    for column in columns_escolas:
        if column == 'DATABASE':
            columns_sql.append(f"esc.{column} AS DATABASE_ESCOLAS")
        else:
            columns_sql.append(f"esc.{column}")

    # Add the columns of the 'educandos' table that are not in the `common_columns` list to the list, differentiate 'DATABASE' column
    for column in columns_educandos:
        if column not in common_columns:
            if column == 'DATABASE':
                columns_sql.append(f"educ.{column} AS DATABASE_EDUCANDOS")
            else:
                columns_sql.append(f"educ.{column}")

    # SQL command to create a new table 'escolas_educandos' based on the 'escolas' and 'educandos' tables
    sql_command = f"""
    CREATE TABLE escolas_educandos AS
    SELECT 
        {', '.join(columns_sql)}
    FROM escolas esc
    JOIN educandos educ
    ON esc.CODESC = educ.CODESC;
    """

    # Execute the SQL command
    cur.execute(sql_command)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Usage of the function:
# create_escolas_educandos_table()