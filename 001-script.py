import pandas as pd
import numpy as np

# Carregar o dataset bruto
df = pd.read_csv('clinicas_oftalmo_raw.csv')

# Visualizar as primeiras linhas e informações gerais da estrutura do dataframe
print(df.info())
print(df.head())

# Iniciando a análise dos dados da tabela. Primeiro, identificar se há marcadores em duplicidade.
filtro_duplicados = df[df.duplicated(subset=['ID_Clinica'])]
print(filtro_duplicados)

# Alguns IDs são iguais, porém representam Nomes de Clínicas diferentes. Por outro lado, em alguns casos, o mesmo nome apresenta-se escrito de maneira diferente.
# Vamos criar uma coluna temporária normalizada
df['Nome_Normalizado'] = df['Nome_Clinica'].str.strip().str.lower()
print(df[['Nome_Clinica', 'Nome_Normalizado']].head(10))

#Agora, uma chave combinando o nome normalizado e a região
df['Chave_Unica_Clinica'] = df['Nome_Normalizado'] + '_' + df['Regiao'].fillna('Sem_Regiao').str.lower().str.strip()

#Depois, o dataframe final filtrando duplicatas reais por essa chave composta
df_final = df.drop_duplicates(subset=['Chave_Unica_Clinica'], keep='first')

print("Quantidade de clínicas únicas identificadas no mercado B2B:")
print(df_final.shape)

# Eliminando a coluna redundante e salvando no DataFrame final limpo
df_final = df_final.drop(columns=['Nome_Normalizado'])

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print(df_final.head())

#Temos alguns estados escritos em letras minúsculas, vamos padronizá-los
df['Regiao'] = df['Regiao'].str.strip().str.upper()
print("Siglas de estados padronizadas:")
print(df['Regiao'].unique())

#Analisando a coluna de Volume de cirurgias por mês, é possível encontrar alguns valores faltantes (nan)
print('Quantidade de valores nulos:', df['Volume_Cirurgias_Mes'].isnull().sum())

# Além disso, encontram-se valores do tipo float, porém, é mais interessante um número do tipo inteiro para esta análise
df['Volume_Cirurgias_Mes'].describe 
print('Média de cirurgias por mês', df['Volume_Cirurgias_Mes'].mean().astype(int))

# Para contornar o problemas de dados faltantes, vamos nos utilizar da mediana para evitar possíveis vieses que a média poreia nos trazer, caso existam outliers no banco de dados
mediana_volume = df['Volume_Cirurgias_Mes'].median()
df['Volume_Cirurgias_Mes'] = df['Volume_Cirurgias_Mes'].fillna(mediana_volume).astype(int)
print('Nulos restantes:',df['Volume_Cirurgias_Mes'].isnull().sum())

# Vamos passar para linha de lentes premium vendidas
print(df['Lentes_Premium_Pct'].head(10))
df['Lentes_Premium_Pct'].describe

#Aqui, temos os dados como objeto e queremos que seja do tipo float. Primeiro, padronizamos a coluna e, depois, trocamos o tipo da string
df['Lentes_Premium_Pct'] = (
    df['Lentes_Premium_Pct']
    .astype(str)
    .str.replace('%', '', regex=False)
    .str.replace(',', '.', regex=False)
    .str.strip()
)
df['Lentes_Premium_Pct'] = pd.to_numeric(df['Lentes_Premium_Pct'], errors='coerce')
print(df['Lentes_Premium_Pct'].describe())
print('Quantidade de valores nulos:', df['Lentes_Premium_Pct'].isnull().sum())

#Assim como no caso do volume de cirurgias, a mediana também é o mais indicado nesta coluna para evitar viés de qualquer outlier
mediana_lentes = df['Lentes_Premium_Pct'].median()
df['Lentes_Premium_Pct'] = df['Lentes_Premium_Pct'].fillna(mediana_lentes)

print('Nulos restantes:',df['Lentes_Premium_Pct'].isnull().sum())

#Avaliando a coluna Equipamento_Laser
df['Equipamento_Laser'].describe
print(df['Equipamento_Laser'].unique())

# Foi possível notar missing values mascarados

# 2. Definindo o nome/caminho do arquivo de saída
nome_arquivo = 'meu_arquivo.csv'

# 3. Exportando o DataFrame para CSV
df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig', sep=';')

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")