import os
import pandas as pd

# Definindo a função comparador_cabecalhos_csv
def comparador_cabecalhos_csv(diretorio, cabecalho_correto, delimitador, encoding):
    """
    Esta função processa arquivos CSV em um diretório especificado, verifica se o cabeçalho de cada arquivo corresponde ao cabeçalho correto fornecido e gera um relatório de comparação.

    Parâmetros:
    diretorio (str): O caminho para o diretório que contém os arquivos CSV.
    cabecalho_correto (str): Uma string delimitada por ponto e vírgula do cabeçalho correto.
    delimitador (str): O delimitador usado nos arquivos CSV.
    encoding (str): A codificação usada nos arquivos CSV.

    Retorna:
    None. A função salva um arquivo CSV com o relatório de comparação no diretório especificado.
    """
    # Inicializando um DataFrame para comparação
    df_comparacao = pd.DataFrame(columns=["Arquivo", "Status", "Colunas faltantes", "Colunas em excesso-nomes diferentes"])
    
    # Iterando sobre todos os arquivos no diretório especificado
    for arquivo in os.listdir(diretorio):
        # Verificando se o arquivo é um arquivo .csv
        if arquivo.endswith(".csv"):
            # Construindo o caminho completo para o arquivo
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            # Lendo o arquivo .csv para um DataFrame
            df = pd.read_csv(caminho_arquivo, delimiter=delimitador, encoding=encoding)
            
            # Convertendo todos os nomes das colunas para maiúsculas
            df.columns = [col.upper() for col in df.columns]
            
            # Identificando as colunas faltantes e em excesso
            colunas_faltantes = set(cabecalho_correto.split(";")) - set(df.columns)
            colunas_em_excesso = set(df.columns) - set(cabecalho_correto.split(";"))
            
            # Determinando o status do arquivo
            status = "correto" if not colunas_faltantes and not colunas_em_excesso else "incorreto"
            
            # Convertendo os conjuntos de colunas para listas
            colunas_faltantes_lista = list(colunas_faltantes)
            
            # Adicionando os resultados ao DataFrame de comparação
            df_comparacao = pd.concat([df_comparacao, pd.DataFrame({
                "Arquivo": [arquivo],
                "Status": [status],
                "Colunas faltantes": [" | ".join(colunas_faltantes_lista)],
                "Colunas em excesso-nomes diferentes": [" | ".join(colunas_em_excesso)]
            })], ignore_index=True)
    
    # Salvando o DataFrame de comparação como um arquivo .csv
    df_comparacao.to_csv(os.path.join(diretorio, 'resultado_comparacao_cabecalhos_escolas.csv'), sep=";", index=False)

# Uso da função:
cabecalho_correto = "DRE;CODESC;TIPOESC;NOMESC;NOMESCOF;CEU;DIRETORIA;SUBPREF;ENDERECO;NUMERO;BAIRRO;CEP;TEL1;TEL2;FAX;SITUACAO;CODDIST;DISTRITO;SETOR;CODINEP;CODCIE;EH;FX_ETARIA;DT_CRIACAO;ATO_CRIACAO;DOM_CRIACAO;DT_INI_FUNC;DT_INI_CONV;DT_AUTORIZA;DT_EXTINCAO;NOME_ANT;REDE;LATITUDE;LONGITUDE;DATABASE"
comparador_cabecalhos_csv('datasets_originais\\escolas', cabecalho_correto, ";", 'latin-1')