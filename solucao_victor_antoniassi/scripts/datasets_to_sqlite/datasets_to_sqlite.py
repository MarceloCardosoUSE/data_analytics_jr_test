import os
import pandas as pd
from unidecode import unidecode

def remove_caracteres_especiais(diretorio_entrada, diretorio_saida, delimitador='\t', encoding='latin-1'):
    """
    Remove caracteres especiais e acentos dos valores das colunas de todos os arquivos CSV e TSV em um diretório,
    e salva os dados novamente em arquivos TSV.

    Args:
        diretorio_entrada (str): Caminho para o diretório com os arquivos CSV e TSV.
        diretorio_saida (str): Caminho para o diretório onde os arquivos TSV serão salvos.
        delimitador (str, opcional): Delimitador usado nos arquivos. Padrão é '\t'.
        encoding (str, opcional): Codificação usada nos arquivos. Padrão é 'latin-1'.

    Returns:
        None
    """
    # Itera sobre os arquivos no diretório de entrada
    for arquivo in os.listdir(diretorio_entrada):
        # Processa apenas arquivos CSV e TSV
        if arquivo.endswith('.csv') or arquivo.endswith('.tsv'):
            # Obtém o caminho completo do arquivo
            caminho_arquivo = os.path.join(diretorio_entrada, arquivo)
            # Lê o arquivo em um DataFrame
            df = pd.read_csv(caminho_arquivo, delimiter=delimitador, encoding=encoding)
            # Remove acentos de cada valor de string no DataFrame
            df = df.apply(lambda x: x.map(lambda y: unidecode(y) if isinstance(y, str) else y))
            # Define o nome do arquivo de saída
            nome_arquivo_tsv = os.path.join(diretorio_saida, arquivo.rsplit('.', 1)[0] + '.tsv')
            # Salva o DataFrame no arquivo de saída
            df.to_csv(nome_arquivo_tsv, sep='\t', index=False, encoding=encoding)


remove_caracteres_especiais('datasets_tratados\\escolas\\tratados_google_sheets', 'datasets_tratados\\escolas\\tratados_python')