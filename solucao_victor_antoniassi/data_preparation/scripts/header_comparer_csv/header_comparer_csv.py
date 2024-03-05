import os
import pandas as pd

# Defining the function compare_csv_headers
def compare_csv_headers(input_directory, output_directory, correct_header, delimiter=';', encoding='latin-1'):
    """
    This function processes CSV files in a specified directory, checks whether the header of each file matches the provided correct header, and generates a comparison report.

    Parameters:
    input_directory (str): The path to the directory containing the CSV files.
    output_directory (str): The path to the directory where the comparison report will be saved.
    correct_header (str): A semicolon-delimited string of the correct header.
    delimiter (str, optional): Delimiter used in the files. Default is ';'.
    encoding (str, optional): Encoding used in the files. Default is 'latin-1'.

    Returns:
    None. The function saves a CSV file with the comparison report in the specified directory.
    """
    # Initializing a DataFrame for comparison
    comparison_df = pd.DataFrame(columns=["File", "Status", "Missing Columns", "Excess Columns-Different Names"])
    
    # Iterating over all files in the specified directory
    for file in os.listdir(input_directory):
        # Checking if the file is a .csv file
        if file.endswith(".csv"):
            # Building the full path to the file
            file_path = os.path.join(input_directory, file)
            
            # Reading the .csv file into a DataFrame
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)
            
            # Converting all column names to uppercase
            df.columns = [col.upper() for col in df.columns]
            
            # Identifying the missing and excess columns
            missing_columns = set(correct_header.split(";")) - set(df.columns)
            excess_columns = set(df.columns) - set(correct_header.split(";"))
            
            # Determining the status of the file
            status = "correct" if not missing_columns and not excess_columns else "incorrect"
            
            # Converting the sets of columns to lists
            missing_columns_list = list(missing_columns)
            
            # Adding the results to the comparison DataFrame
            comparison_df = pd.concat([comparison_df, pd.DataFrame({
                "File": [file],
                "Status": [status],
                "Missing Columns": [" | ".join(missing_columns_list)],
                "Excess Columns-Different Names": [" | ".join(excess_columns)]
            })], ignore_index=True)
    
    # Saving the comparison DataFrame as a .csv file
    comparison_df.to_csv(os.path.join(output_directory, 'comparison_result_school_headers.csv'), sep=";", index=False)


# Usage of the function:
correct_header = "DRE;CODESC;TIPOESC;NOMESC;NOMESCOF;CEU;DIRETORIA;SUBPREF;ENDERECO;NUMERO;BAIRRO;CEP;TEL1;TEL2;FAX;SITUACAO;CODDIST;DISTRITO;SETOR;CODINEP;CODCIE;EH;FX_ETARIA;DT_CRIACAO;ATO_CRIACAO;DOM_CRIACAO;DT_INI_FUNC;DT_INI_CONV;DT_AUTORIZA;DT_EXTINCAO;NOME_ANT;REDE;LATITUDE;LONGITUDE;DATABASE"
compare_csv_headers('datasets_originais\\escolas', 'datasets_originais\\escolas', correct_header)