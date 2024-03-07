

# Projeto de Preparação de Dados - Empresa de Uniformes e Materiais Escolares

Este projeto é baseado em um **cenário fictício** e foi desenvolvido com o objetivo de simular a etapa de preparação de dados, uma fase crucial e desafiadora no processo de análise de dados.

A preparação adequada dos dados é essencial para o desenvolvimento de análises de dados eficazes que podem auxiliar no planejamento de vendas e operações de uma empresa de comércio físico/virtual de uniformes e materiais escolares na cidade de São Paulo para o ano de 2023.

Os dados utilizados são referentes aos perfis de alunos e escolas da cidade de São Paulo dos anos de 2021 e 2022. A escolha desses anos se deu pelo fato de que os dados de 2023 dos educandos não continham o campo raça, um atributo que considero de grande relevância para a análise em um projeto real de preparação de dados em uma empresa com essa área de atuação.

Embora estejamos atualmente no ano de 2024, o cenário foi pensado para refletir as condições e desafios que uma empresa poderia enfrentar ao planejar suas operações para o ano seguinte, com base nos dados disponíveis dos anos anteriores.

## Conjunto de Dados

Os dados utilizados neste projeto são referentes aos anos de 2021 e 2022, extraídos de quatro arquivos .csv. Dois desses arquivos contêm perfis agregados de estudantes e os outros dois contêm informações sobre as escolas.

Cada registro nos dados dos educandos representa um número de alunos por escola, agrupados por série, turno, sexo, idade, necessidades educacionais especiais e raça/cor. Esses dados foram obtidos a partir do portal da Prefeitura de São Paulo, os dados dos perfis de educandos podem ser acessados [aqui](http://dados.prefeitura.sp.gov.br/dataset/perfil-dos-educandos-cor-raca-idade-sexo-necessidades-educacionais-especiais) e os das escolas [aqui](http://dados.prefeitura.sp.gov.br/dataset/cadastro-de-escolas-municipais-conveniadas-e-privadas).

## Etapas da Preparação de Dados

1. Análise inicial da qualidade dos dados e das estruturas dos arquivos .csv utilizando o Google Sheets.
2. Desenvolvimento de um [script](data_preparation/scripts/compare_delimited_file_headers) em Python para comparar os cabeçalhos dos arquivos (educandos e escolas) com cabeçalhos corretos baseados nos respectivos dicionários de dados.
3. Correção manual dos problemas identificados utilizando o Google Sheets (correção nos nomes dos campos, mudança de posições das colunas para posições corretas e exclusão de colunas totalmente vazias ou que não existem no dicionários de dados).
4. Desenvolvimento de um [script](data_preparation/scripts/datasets_to_sqlite) em Python que aplica algumas etapas de preparação/limpeza nos dados, necessário para os dados serem armazenados de forma correta no banco de dados SQLite.
5. Desenvolvimento de um [script](data_preparation/scripts/datasets_to_sqlite) em Python que cria o [banco de dados SQLite](sqlite_db) e que faz a ingestão de dados dos arquivos para as tabelas 'educandos' (dados dos perfis de alunos matriculados nos anos de 2021 e 2022), 'escolas' (dados sobre as escolas municipais referente aos anos de 2021 e 2022) e 'escolas_educandos' (tabela que faz a junção das tabelas 'escolas' e 'educandos').

## Resultados

Os dados foram preparados e salvos em um [banco de dados SQLite](sqlite_db), prontos para análises de dados.

## Sugestões de Análises

1. **Análise Demográfica**: Analisar a distribuição dos alunos com base em características demográficas, como raça, gênero e idade. Isso pode ajudar a empresa a entender melhor a diversidade de seus clientes potenciais e a desenvolver produtos que atendam às necessidades de diferentes grupos demográficos.

2. **Análise de Necessidades Educacionais Especiais**: Analisar a distribuição de alunos com necessidades educacionais especiais. Isso pode ajudar a empresa a desenvolver produtos específicos para esse segmento, o que pode ser uma consideração importante para muitos pais.

3. **Análise de Tendências**: Comparar os dados de 2021 e 2022 para identificar tendências. Isso pode ajudar a empresa a prever a demanda futura e a se preparar adequadamente para atender às necessidades dos pais.

4. **Análise de Cluster**: Agrupar escolas com base em características semelhantes (como localização e tamanho) e analisar as diferenças nas tendências de vendas entre os diferentes grupos. Isso pode ajudar a empresa a entender melhor as necessidades específicas de diferentes comunidades escolares.

5. **Análise de Segmentação de Mercado**: Identificar segmentos de mercado com base nas características dos alunos e das escolas. Isso pode ajudar a empresa a personalizar seus produtos e estratégias de marketing para diferentes segmentos, permitindo que ela atenda melhor às necessidades dos pais.
