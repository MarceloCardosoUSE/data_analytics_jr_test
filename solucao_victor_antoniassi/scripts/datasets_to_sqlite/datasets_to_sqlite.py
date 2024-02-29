import pandas as pd
from unidecode import unidecode

def remove_caracteres_especiais(arquivos_csv, delimitador=',', encoding='latin-1'):
    """
    Função para ler um ou mais arquivos CSV, remover caracteres especiais e acentos dos valores das colunas,
    e salvar os dados novamente em arquivos TSV.

    Parâmetros:
    arquivos_csv (list): Lista de arquivos CSV para processar.
    delimitador (str, opcional): Delimitador usado nos arquivos CSV. Padrão é ','.
    encoding (str, opcional): Codificação usada nos arquivos CSV. Padrão é 'latin-1'.

    Retorna:
    None
    """
    for arquivo_csv in arquivos_csv:
        df = pd.read_csv(arquivo_csv, delimiter=delimitador, encoding=encoding)  # Lê o arquivo CSV
        df = df.applymap(lambda x: unidecode(str(x)) if isinstance(x, str) else x)  # Remove acentos
        nome_arquivo_tsv = arquivo_csv.replace('.csv', '.tsv')  # Cria o nome do arquivo TSV
        df.to_csv(nome_arquivo_tsv, sep='\t', index=False, encoding=encoding)  # Salva como TSV