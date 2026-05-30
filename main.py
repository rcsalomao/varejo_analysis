import pandas as pd
import numpy as np
import os
from subprocess import run
from shutil import which
from collections import Counter


ESTADO_CIVIL_MAP = {
    1: "CASADO",
    2: "DIVORCIADO",
    3: "SEPARADO",
    4: "SOLTEIRO",
    5: "VIUVO",
}


def print_nulos_por_col(df):
    print("Nulos por coluna:")
    nulos = df.isnull().sum()
    pct = (nulos / len(df) * 100).round(1)
    for col in df.columns:
        if nulos[col] > 0:
            print(f"  {col}: {nulos[col]} ({pct[col]}%)")
    print()


def get_dataframes(filename):
    # Carregando os dados
    print(">>> Leitura de Dados")
    df = pd.read_csv(filename, sep=";", encoding="utf-8-sig")
    print("-> Leitura de dados completada com sucesso")

    def relatorio_qualidade(df, nome):
        print(f"\n{'=' * 50}")
        print(f"RELATÓRIO: {nome}".center(50))
        print(f"{'=' * 50}")
        print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
        print()
        print_nulos_por_col(df)
        n_duplicatas = df.duplicated().sum()
        print(f"Duplicatas: {n_duplicatas} ({n_duplicatas / len(df) * 100:.2f}%)")
        print()
        print("Tipos das colunas:")
        print(df.dtypes)

    relatorio_qualidade(df, "Base Varejo")
    print()
    return df


# Verificar a existência do dataset e descompactá-lo caso necessário
dataset_csv = os.path.isfile("./data/input/Base Varejo.csv")
dataset_zip = os.path.isfile("./data/input/Base Varejo.csv.zip")
if not dataset_csv:
    if not dataset_zip:
        print("ERRO: Arquivo do dataset não encontrado!")
        print(
            "Por favor, mover 'Base Varejo.csv.zip' ou 'Base Varejo.csv' para './data/input/'"
        )
        exit(1)
    if not which("unzip"):
        print("ERRO: Comando 'unzip' não encontrado!")
        print(
            "Por favor, instale 'unzip' ou utilize um sistema operacional de verdade c:"
        )
        print(
            "Caso não seja possível, faça a extração manual do arquivo 'Base Varejo.csv.zip' para a pasta './data/input/'"
        )
        exit(1)
    run(
        'unzip -qq "./data/input/Base Varejo.csv.zip" -d "./data/input/"',
        shell=True,
        check=True,
    )


# Ingestão dos dados e criação de relatório
df = get_dataframes("./data/input/Base Varejo.csv")


# Percebe-se que pelo relatório de ingestão
# o dataset possui colunas completamente vazias.
# No caso, seriam as colunas de índice 10, 11, 12 e 13.
# Deve-se proceder então para a remoção destas mesmas colunas:
df.drop(columns=df.columns[[10, 11, 12, 13]], inplace=True)


# Foram identificadas aprox. 11,63% de linhas duplicadas no dataset.
# Procede-se, portanto, para a remoção das mesmas:
df.drop_duplicates(keep="first", inplace=True)
print("Após remoção dos dados duplicados:")
print(f"  Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
print()


# Substituição de valores string "NULL", "N/A", "" e "#N/D" pelo valor 'None':
df.replace({v: None for v in ["NULL", "N/A", "", "#N/D"]}, inplace=True)
print("Após a substituição de valores string nulos")
print_nulos_por_col(df)
# O total de nulos presente no dataset é de 0.4% nas colunas de categoria e nome do produto
# Entendo que este valor não seja significativo e, portanto,
# é plenamente possível fazer uso destes campos


# Padronização do nome dos produtos, com a remoção de espaços extras e capitalização
df["PR_NOME"] = df["PR_NOME"].str.strip().str.upper()


# Conversão do tipo dos valores no campo 'DATA' para datetime
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
print("Após a conversão dos valores no campo 'DATA'")
print("Tipos das colunas:")
print(df.dtypes)
print_nulos_por_col(df)


# Substituição dos valores inteiros do campo 'CL_EC' para correspondente
# em string, segundo o mapeamento dado em 'ESTADO_CIVIL_MAP' para melhor compreensão
df["CL_EC"] = df["CL_EC"].map(lambda x: ESTADO_CIVIL_MAP[x])


# Estatísticas para os valores de 'CL_FHL'
print("Estatísticas descritivas para o de número de filhos dos clientes:")
print(df["CL_FHL"].describe())
print(f"moda: {df['CL_FHL'].mode().values[0]}\n")


print(">>> Exploração de padrões por agrupamento:")

print("Valores proporcionais de produtos comprados por gênero:")
print(df.groupby(by="CL_GENERO")["PR_CAT"].value_counts(normalize=True) * 100)
# É possível perceber que, proporcionalmente, o perfil de compra
# em função do gênero do cliente se mantém inalterado.

print("Distinção de gênero dos clientes com a respectiva quantidade de filhos:")
print(df.groupby(by="CL_FHL")["CL_GENERO"].value_counts(normalize=True) * 100)
# Percebe-se neste caso que, de forma geral (casos de 0, 1, 2 e 3 filhos),
# as clientes do sexo feminino são mais predominantes.
# Entretanto há uma inversão significativa para o caso específico de um casal
# com 4 filhos, cujo há uma presença mais exarcebada de clientes masculinos.
# Poderia-se presumir que nestes casos é a esposa a responsável por cuidar
# das crianças enquanto o esposo realiza as compras.
print()


print(">>> Insights alcançados:")

print("Proporção de compras por gênero:")
print(df["CL_GENERO"].value_counts(normalize=True) * 100)
# Percebe-se que há uma maior presença de clientes
# do gênero feminino neste dataset.

print("Número de vendas por categoria:")
print(df["PR_CAT"].value_counts(normalize=True) * 100)
# Por meio desta tabela, pode-se notar que os
# produtos da categoria de ALIMENTOS são os
# mais vendidos, contribuindo com mais de 52% das
# vendas. Já os produtos da categoria ACESSORIOS são
# os produtos que a menor representação com menos de
# 2% de representação.

print("Número total de vendas por ano e diferença percentual:")
df_2019 = df.loc[df["DATA"].dt.year == 2019, :]
df_2020 = df.loc[df["DATA"].dt.year == 2020, :]
n_vendas_2019 = (
    df_2019["DATA"]
    .dt.month.value_counts(sort=False, normalize=False)
    .to_frame()
    .sort_values(by="DATA")
)
n_vendas_2020 = (
    df_2020["DATA"]
    .dt.month.value_counts(sort=False, normalize=False)
    .to_frame()
    .sort_values(by="DATA")
)
print(f"Total de vendas em 2019: {n_vendas_2019['count'].sum()}")
print(f"Total de vendas em 2020: {n_vendas_2020['count'].sum()}")
print(
    f"Diferença percentual: {((n_vendas_2020.sum() - n_vendas_2019.sum()) / n_vendas_2019.sum() * 100).values[0]}"
)
# Nota-se que houve um aumento de quase 10% no volume de vendas
# entre os anos de 2019 e 2020.

print("Número de vendas por mês durante os dois anos:")
print("  Ano de 2019:")
print("  Quantidade de vendas por mês:")
print(n_vendas_2019["count"])
print(n_vendas_2019.describe())
dias_unicos = df_2019["DATA"].unique()
dias_por_mes = pd.DataFrame.from_dict(
    Counter([d.month for d in dias_unicos]), orient="index", columns=["quantidade"]
)
print("  Quantidade de vendas por mês normalizada pela quantidade de dias:")
vendas_por_dia_mes = n_vendas_2019["count"] / dias_por_mes["quantidade"]
print(vendas_por_dia_mes)
print("  Ano de 2020:")
print("  Quantidade de vendas por mês:")
print(n_vendas_2020["count"])
print(n_vendas_2020.describe())
dias_unicos = df_2020["DATA"].unique()
dias_por_mes = pd.DataFrame.from_dict(
    Counter([d.month for d in dias_unicos]), orient="index", columns=["quantidade"]
)
print("  Quantidade de vendas por mês normalizada pela quantidade de dias:")
vendas_por_dia_mes = n_vendas_2020["count"] / dias_por_mes["quantidade"]
print(vendas_por_dia_mes)
# Do ano de 2019 para 2020, o número de vendas médio aumentou quase 10%
# com a redução do respectivo desvio padrão em 35%, demonstrando que
# a amplitude dos valores mensais se tornou menor enquanto os valores
# mensais resultaram maiores.
# Ao se analisar as vendas mensais normalizadas pelo número de dias,
# percebe-se que não há a presença de um claro padrão a longo dos
# anos e entre os anos.

# print(
#     df["PR_CAT"].unique()
# )  # ['BEBIDAS' 'HIGIENE' 'ALIMENTOS' 'LIMPEZA' 'ACESSORIOS' 'PET' None]
print("Número de vendas por categoria de produtos:")
print("Produtos de HIGIENE:")
print(df.query("PR_CAT == 'HIGIENE'")["PR_NOME"].value_counts(normalize=True) * 100)
print("Produtos de ALIMENTOS:")
print(df.query("PR_CAT == 'ALIMENTOS'")["PR_NOME"].value_counts(normalize=True) * 100)
print("Produtos de LIMPEZA:")
print(df.query("PR_CAT == 'LIMPEZA'")["PR_NOME"].value_counts(normalize=True) * 100)
print("Produtos para PET:")
print(df.query("PR_CAT == 'PET'")["PR_NOME"].value_counts(normalize=True) * 100)
