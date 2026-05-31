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
A execução do script resulta na exposição dos resultados e considerações do projeto no stdout do terminal, além do arquivo `./data/output/base_varejo_clean.csv` que representa o dataset processado e limpo em formato `csv`.
O script, quando possível, também gera o arquivo compactado em `zip`.

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

### Proporção de compras por gênero

Pretende-se avaliar se há uma diferença significativa no padrão de consumo entre os gêneros.
A seguinte tabela mostra os valores proporcionais:
```
CL_GENERO
F    52.141055
M    47.858945
Name: proportion, dtype: float64
```
Percebe-se que há uma presença significativamente maior (~ 9%) de clientes do gênero feminino neste dataset.
Este valor pode servir de base para políticas de marketing mais eficientes e direcionadas.

### Número de vendas por categoria

A seguir são mostrados os valores proporcionais de vendas por categoria:
```
PR_CAT
ALIMENTOS     52.613942
HIGIENE       18.857630
LIMPEZA       17.615537
BEBIDAS        5.240072
PET            3.910197
ACESSORIOS     1.762622
Name: proportion, dtype: float64
```
Por meio desta tabela, pode-se notar que os produtos da categoria de ALIMENTOS são os mais vendidos, contribuindo com mais de 52% das vendas.
Já os produtos da categoria ACESSORIOS são os produtos que possuem a menor representação, com menos de 2%.

### Número total de vendas por ano e diferença percentual
Adiante, procura-se entender qual a variação nos números de venda entre os anos de 2019 e 2020.
A tabela à seguir nos conta que houve um aumento de quase 10% no respectivo volume de vendas.
```
Total de vendas em 2019: 176103
Total de vendas em 2020: 192804
Diferença percentual: 9.483654452223982
```
### Número de vendas por mês durante os dois anos
As tabelas seguintes resumem os dados de vendas para o ano de 2019:
```
  Quantidade de vendas por mês:
DATA
1      6492
2     16153
3      9835
4     16255
5     28115
6     19484
7     10755
8     15918
9     16895
10     9127
11     6120
12    20954
Name: count, dtype: int64

  Estatísticas das vendas por mês:
              count
count     12.000000
mean   14675.250000
std     6495.187535
min     6120.000000
25%     9658.000000
50%    16035.500000
75%    17542.250000
max    28115.000000

  Quantidade de vendas por mês normalizada pela quantidade de dias:
1     1298.400000
2     2692.166667
3     1405.000000
4     2322.142857
5     2162.692308
6     2164.888889
7     2688.750000
8     1768.666667
9     2111.875000
10    1521.166667
11    1224.000000
12    2328.222222
dtype: float64
```

Já as próximas tabelas resumem os dados de vendas para o ano de 2020:
```
  Quantidade de vendas por mês:
DATA
1     20675
2     17173
3     17543
4     15695
5     14011
6     10907
7      8967
8     15935
9     18877
10    25275
11    15079
12    12667
Name: count, dtype: int64

  Estatísticas das vendas por mês:
              count
count     12.000000
mean   16067.000000
std     4382.543139
min     8967.000000
25%    13675.000000
50%    15815.000000
75%    17876.500000
max    25275.000000

  Quantidade de vendas por mês normalizada pela quantidade de dias:
1     2067.500000
2     1717.300000
3     2506.142857
4     2242.142857
5     2335.166667
6     2726.750000
7     1793.400000
8     2276.428571
9     2359.625000
10    2297.727273
11    2154.142857
12    1809.571429
dtype: float64
```
É possível perceber que do ano de 2019 para 2020, o número de vendas médio aumentou quase 10% com a redução do respectivo desvio padrão em 35%, demonstrando que a amplitude dos valores mensais se tornou menor enquanto os valores mensais resultaram maiores.
Ao se analisar as vendas mensais normalizadas pelo número de dias, percebe-se que não há a presença de um claro padrão a longo dos anos e/ou entre os anos.

### foo

Por fim, é de interesse também entender qual a distribuição de vendas dos produtos por suas respectivas categorias.
As seguintes tabelas demonstram quais são as vendas proporcionais dos diversos produtos encontrados no dataset, ordenados em forma decrescente.
```
Produtos de HIGIENE:
PR_NOME
ESCOVA DE DENTE     4.733410
GEL                 4.732684
MODELADOR           4.723969
PAPEL HIGIENICO     4.703635
CREME               4.691290
PRESERVATIVO        4.686206
FRALDA              4.667325
FIXADOR             4.657158
FIO DENTAL          4.656432
HASTES FLEXIVEIS    4.654253
SABONETE            4.652075
SHAMPOO             4.647718
HIDRATANTE          4.643360
CONDICIONADOR       4.642634
REPELENTE           4.623027
TALCO               4.623027
TINTURAS            4.604871
PASTA DE DENTE      4.597609
LENCO UMEDECIDO     4.583085
ENXAGUANTE BUCAL    4.574371
PROTETOR SOLAR      4.563478
ABSORVENTE          2.338383
Name: proportion, dtype: float64

Produtos de ALIMENTOS:
PR_NOME
PRESUNTO COZIDO               3.310541
SARDINHA                      1.720472
BANANA                        1.696525
PAPINHA INFANTIL              1.695745
CEBOLA                        1.692101
                                ...   
COXA E SOBRECOXA DE FRANGO    1.616358
ACHOCOLATADO                  0.844098
ABACAXI                       0.843057
ABACATE                       0.841235
ALHO                          0.831344
Name: proportion, Length: 61, dtype: float64

Produtos de LIMPEZA:
PR_NOME
CERA                  5.054730
LIMPADOR PERFUMADO    5.053952
DESENGORDURANTE       5.053175
REMOVEDOR             5.047733
DETERGENTE            5.040736
RODO                  5.011195
LIMPADOR MULTIUSO     5.008862
SABAO                 4.999534
INSETICIDA            4.996424
AMACIANTE             4.995646
BALDE                 4.994092
TIRA LIMO             4.993314
LUSTRA MOVEIS         4.990982
VASSOURA              4.987872
DESINFETANTE          4.966882
LIMPA VIDROS          4.963773
TIRA MANCHA           4.949779
ODORIZADOR            4.948224
SABAO EM PO           4.910131
AGUA SANITARIA        2.570123
ALCOOL                2.462840
Name: proportion, dtype: float64

Produtos para PET:
PR_NOME
RACAO SECA PARA CAES      22.533534
RACAO UMIDA PARA CAES     22.221833
RACAO SECA PARA GATOS     22.214829
RACAO UMIDA PARA GATOS    21.829580
ALIMENTO PARA PASSARO     11.200224
Name: proportion, dtype: float64
```
Desta maneira, pode-se ter uma melhor idéia sobre quais produtos possuem maiores e menores demandas nas suas respectivas categorias.
No caso dos produtos de higiene, é possível perceber que todos eles possuem valores muito próximos de vendas, com a única excessão do produto absorvente, que possui um valor significativamente menor.
Já para os produtos da categoria de alimentos, é possível separar os produtos em 3 grupos de acordo com seus números de vendas.
O produto mais consumido é o presunto cozido, enquanto os produtos com menor saída são o achocolatado, abacaxi, abacate e alho.
Para os produtos de limpeza, apenas a água sanitária e o álcool registraram valores de vendas significantemente menores do restante.
Por fim, para os produtos da categoria pet, apenas o alimento para pássaro possui valor muito inferior aos outros tipos de ração.

## Conclusão

