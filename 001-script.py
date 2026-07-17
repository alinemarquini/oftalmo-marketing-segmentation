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

filtro_duplicados_nome = df[df.duplicated(subset=['Nome_Normalizado'], keep=False)]
print(filtro_duplicados_nome[['ID_Clinica', 'Nome_Clinica', 'Regiao', 'Volume_Cirurgias_Mes']].head(6))