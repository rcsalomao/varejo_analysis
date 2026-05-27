import pandas as pd
import numpy as np


def print_nulos_por_col(df):
    print("Nulos por coluna:")
    nulos = df.isnull().sum()
    pct = (nulos / len(df) * 100).round(1)
    for col in df.columns:
        if nulos[col] > 0:
            print(f"  {col}: {nulos[col]} ({pct[col]}%)")


def get_dataframes(filename):
    # Carregando os dados
    print(">>> Leitura de Dados")
    df = pd.read_csv(filename, sep=";")
    print("-> Leitura de dados completada com sucesso")

    def relatorio_qualidade(df, nome):
        print(f"\n{'=' * 50}")
        print(f"RELATÓRIO: {nome}".center(50))
        print(f"{'=' * 50}")
        print(f"Linhas: {df.shape[0]} | Colunas: {df.shape[1]}")
        print()
        print_nulos_por_col(df)
        n_duplicatas = df.duplicated().sum()
        print()
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


# Substituição de valores string "NULL", "N/A" e "" pelo valor 'None':
df.replace({v: None for v in ["NULL", "N/A", ""]}, inplace=True)
print("\nApós a substituição de valores string nulos")
print_nulos_por_col(df)
