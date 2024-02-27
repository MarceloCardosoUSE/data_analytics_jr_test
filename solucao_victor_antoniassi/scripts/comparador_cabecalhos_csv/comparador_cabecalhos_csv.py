import os
import pandas as pd

def carregar_csv(caminho_arquivo):
    """
    Carrega um arquivo CSV e retorna um DataFrame do Pandas.

    Args:
        caminho_arquivo (str): O caminho para o arquivo CSV.

    Returns:
        pandas.DataFrame: O DataFrame contendo os dados do arquivo CSV.
    """
    return pd.read_csv(caminho_arquivo, delimiter=";", encoding='latin-1')

def comparar_cabecalhos(df):
    """
    Compara as colunas de um DataFrame com um cabeçalho correto predefinido.

    Args:
        df (pandas.DataFrame): O DataFrame a ser comparado.

    Returns:
        tuple: Uma tupla contendo:
            - str: "correto" se as colunas estiverem corretas, "incorreto" caso contrário.
            - set: Conjunto de colunas faltantes.
            - set: Conjunto de colunas em excessonomes diferentes.
    """
    cabecalho_correto = "DRE;CODESC;TIPOESC;NOMESC;NOMESCOF;CEU;DIRETORIA;SUBPREF;ENDERECO;NUMERO;BAIRRO;CEP;TEL1;TEL2;FAX;SITUACAO;CODDIST;DISTRITO;SETOR;CODINEP;CODCIE;EH;FX_ETARIA;DT_CRIACAO;ATO_CRIACAO;DOM_CRIACAO;DT_INI_CONV;DT_AUTORIZA;DT_EXTINCAO;NOME_ANT;LATITUDE;LONGITUDE;DATABASE"
    # Converter nomes das colunas para maiúsculas
    df.columns = [col.upper() for col in df.columns]
    
    colunas_faltantes = set(cabecalho_correto.split(";")) - set(df.columns)
    colunas_em_excesso = set(df.columns) - set(cabecalho_correto.split(";"))
    
    if not colunas_faltantes and not colunas_em_excesso:
        return "correto", colunas_faltantes, colunas_em_excesso
    else:
        return "incorreto", colunas_faltantes, colunas_em_excesso

def main():
    """
    Função principal que compara cabeçalhos de arquivos CSV em um diretório.

    Cria um DataFrame com os resultados das comparações.

    Salva os resultados em um arquivo CSV chamado 'resultado_comparacao_cabecalhos.csv'.
    """
    diretorio = 'datasets_tratados/escolas'
    df_comparacao = pd.DataFrame(columns=["Arquivo", "Status", "Colunas faltantes", "Colunas em excesso-nomes diferentes"])

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".csv"):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            df = carregar_csv(caminho_arquivo)
            status, colunas_faltantes, colunas_em_excesso = comparar_cabecalhos(df)

            # Converta o conjunto colunas_faltantes para uma lista
            colunas_faltantes_lista = list(colunas_faltantes)

            df_comparacao = pd.concat([df_comparacao, pd.DataFrame({
                "Arquivo": [arquivo],
                "Status": [status],
                "Colunas faltantes": [" | ".join(colunas_faltantes_lista)],
                "Colunas em excesso-nomes diferentes": [" | ".join(colunas_em_excesso)]
            })], ignore_index=True)

    df_comparacao.to_csv('datasets_tratados/escolas/.csv', sep=";", index=False)

if __name__ == "__main__":
    main()