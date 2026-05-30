# varejo_analysis
Neste repositório consta a análise de dados do dataset de varejo, como projeto avaliativo do curso de análise de dados do SCTEC.

# Objetivo
Trata-se da análise e considerações à cerca das questões presentes no documento de instrução `./briefing/Análise de Dados com Python [T2] - M1S07 - Mini-Projeto Avaliativo .pdf`.

A primeira parte corresponde às rotinas de ingestão, tratamento e limpeza dos dados brutos resultando num dataset limpo e ideal para as posteriores análises.

Na sequência, as questões propostas pelo documento de instrução são respondidas e discutidas. Os Insights são melhor detalhados em seção específica posteriormente.

Por fim, realiza-se a escrita dos dados limpos por meio de rotinas específicas.

# Requisitos
Este repositório faz uso das seguintes bibliotecas:

- pandas
- matplotlib

Por favor, instale-as previamente.

## Uso
O ponto de entrada do algoritmo para análise é o arquivo `./main.py`.
Basta, portanto, executar o respectivo arquivo pelo interpretador à partir da pasta raiz do projeto.

# Resultados
A execução do script resulta na exposição dos resultados e considerações do projeto no stdout do terminal, além do arquivo `./data/output/base_varejo_clean.csv` que representa o dataset processado e limpo em formato `csv`. O script, quando possível, também gera o arquivo compactado em `zip`.

Adicionalmente, o script `./main.py` também contém comentários e conclusões à cerca dos processos de limpeza e deduções.

## Ingestão dos dados
A ingestão dos dados brutos é realizada pela função `get_dataframes` por meio do método `pandas.read_csv(...)` da biblioteca `pandas`.
Adicionalmente é gerado um relatório inicial sobre o estado do mesmo, descrevendo a quantidade de dados duplicados, nulos e tipos das colunas encontradas.

O output resultante da ingestão dos dados é descrito à seguir:

```
>>> Leitura de Dados
-> Leitura de dados completada com sucesso

==================================================
              RELATÓRIO: Base Varejo              
==================================================
Linhas: 830000 | Colunas: 14

Nulos por coluna:
  Unnamed: 10: 830000 (100.0%)
  Unnamed: 11: 830000 (100.0%)
  Unnamed: 12: 830000 (100.0%)
  Unnamed: 13: 830000 (100.0%)

Duplicatas: 96553 (11.63%)

Tipos das colunas:
DATA            object
CO_ID            int64
CL_ID            int64
CL_GENERO       object
CL_EC            int64
CL_FHL           int64
CL_SEG          object
PR_ID            int64
PR_CAT          object
PR_NOME         object
Unnamed: 10    float64
Unnamed: 11    float64
Unnamed: 12    float64
Unnamed: 13    float64
dtype: object
```

## Limpeza dos dados

A limpeza dos dados brutos é realizada pela função `process_limpeza_df` logo após a ingestão dos mesmos.

Num primeiro momento foi identificada a presença de 4 colunas completamente nulas (de ids 10, 11, 12, 13) que foram propriadamente removidas do dataframe.

Na sequência foi realizada a remoção dos dados duplicados, já que anteriormente foi detectado a presença dos mesmos na proporção de 11,63% do total.
Entende-se que esta proporção é suficientemente pequena para se realizar a remoção completa.
O resultado no terminal é de:
```
-> Após remoção dos dados duplicados
  Linhas: 733447 | Colunas: 10
```

Realiza-se também a substituição de possíveis valores nulos do tipo string ("NULL", "N/A", "", "#N/D"), resultando no output à seguir.
```
-> Após a substituição de valores string nulos
Nulos por coluna:
  PR_CAT: 3228 (0.4%)
  PR_NOME: 3228 (0.4%)
```
O total de nulos presente no dataset é de 0.4% nas colunas de categoria e nome do produto.
Entendo que este valor não seja significativo e, portanto, é plenamente possível fazer uso destes campos.

Adicionalmente também é feita a padronização dos nomes dos produtos por meio do seguinte código:
```python
df["PR_NOME"] = df["PR_NOME"].str.strip().str.upper()
```

Também se faz necessário realizar a conversão das informações contidas na coluna 'DATA' para o tipo apropriado `datetime`.
Os valores que resultam em erros de conversão são implícitamente convertidos para `None`.
Segue o output resultante:
```
-> Após a conversão dos valores no campo 'DATA'
Tipos das colunas:
DATA         datetime64[ns]
CO_ID                 int64
CL_ID                 int64
CL_GENERO            object
CL_EC                 int64
CL_FHL                int64
CL_SEG               object
PR_ID                 int64
PR_CAT               object
PR_NOME              object
dtype: object
Nulos por coluna:
  PR_CAT: 3228 (0.4%)
  PR_NOME: 3228 (0.4%)
```

Por fim, realiza-se também a padronização dos valores do campo `CL_EC`, convertendo o número inteiro na sua categoria de fato em texto.
```python
df["CL_EC"] = df["CL_EC"].map(lambda x: ESTADO_CIVIL_MAP[x])
```
Em que `ESTADO_CIVIL_MAP` é um mapeamento do inteiro para a sua respectiva categoria string.

## Estatísticas descritivas
As estatísticas descritivas são realizadas na função `estat_descr`.
À seguir são apresentadas as estatísticas descritivas para os dados referentes ao número de filhos dos clientes do dataset:
```
>>> Estatísticas descritivas para o de número de filhos dos clientes:
count    733447.000000
mean          1.146049
std           1.416917
min           0.000000
25%           0.000000
50%           0.000000
75%           2.000000
max           4.000000
Name: CL_FHL, dtype: float64
moda: 0
```

## Análise por agrupamentos
As análises por agrupamentos são realizadas pela função `explor_agrup`.
Primeiramente verifica-se alguma disparidade de comportamento entre gêneros:
```
-> Valores proporcionais de produtos comprados por gênero
CL_GENERO  PR_CAT    
F          ALIMENTOS     52.601941
           HIGIENE       18.837512
           LIMPEZA       17.683691
           BEBIDAS        5.191012
           PET            3.889582
           ACESSORIOS     1.796262
M          ALIMENTOS     52.627016
           HIGIENE       18.879548
           LIMPEZA       17.541289
           BEBIDAS        5.293518
           PET            3.932655
           ACESSORIOS     1.725973
Name: proportion, dtype: float64
```
Percebe-se que de forma geral não há uma diferença nas proporções de consumo entre os gêneros.
Ambos são muito similares.

Adicionalmente também é realizada a análise da proporção de clientes com a respectiva quantidade de filhos:
```
-> Distinção de gênero dos clientes com a respectiva quantidade de filhos
CL_FHL  CL_GENERO
0       F            52.995953
        M            47.004047
1       F            55.341516
        M            44.658484
2       F            50.386543
        M            49.613457
3       F            55.408140
        M            44.591860
4       M            58.508467
        F            41.491533
Name: proportion, dtype: float64
```
Percebe-se neste caso que, de forma geral (casos de 0, 1, 2 e 3 filhos), as clientes do gênero feminino são mais predominantes.
Entretanto há uma inversão significativa para o caso específico de clientes com 4 filhos, cujo há uma presença mais exarcebada de pessoas do gênero masculino.

## Insights

### foo
### foo
### foo
### foo
### foo

## Conclusão

