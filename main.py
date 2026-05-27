import pandas as pd
import numpy as np

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


df = get_dataframes("./data/Base Varejo.csv")


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


# Substituição de valores string "NULL", "N/A" e "" pelo valor 'None':
df.replace({v: None for v in ["NULL", "N/A", "", "#N/D"]}, inplace=True)
print("Após a substituição de valores string nulos")
print_nulos_por_col(df)


# Padronização do nome dos produtos, com a remoção de espaços extras e capitalização
df["PR_NOME"] = df["PR_NOME"].str.strip().str.upper()


# Conversão do tipo dos valores no campo 'DATA' para datetime
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
print("Após a conversão dos valores no campo 'DATA'")
print("Tipos das colunas:")
print(df.dtypes)
print_nulos_por_col(df)


# Substituição dos valores inteiros do campo 'CL_EC' para correspondente
# em string, segundo o mapeamento dado em 'ESTADO_CIVIL_MAP'
df["CL_EC"] = df["CL_EC"].map(lambda x: ESTADO_CIVIL_MAP[x])


# Estatísticas para os valores de 'CL_FHL'
print("Estatísticas descritivas para o de número de filhos dos clientes:")
print(df["CL_FHL"].describe())
print(f"moda: {df['CL_FHL'].mode().values[0]}\n")


# Exploração de padrões por agrupamento
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
