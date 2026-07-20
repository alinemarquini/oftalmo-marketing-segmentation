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