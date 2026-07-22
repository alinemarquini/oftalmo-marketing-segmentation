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
# Ver os 20 valores mais frequentes (mesmo os que parecem texto normal)
print(df['Equipamento_Laser'].value_counts(dropna=False).head(20))

# Analisando os fabricantes mais recorrentes, vamos padronizar utilizando os nomes que mais aparecem: Zeiss, Alcon e J&J Vision.
equip = df['Equipamento_Laser'].str.lower().fillna('')

df['Fabricante_Laser'] = 'Outros/Desconhecido' #Valor padrão

df.loc[equip.str.contains('alcon|wavelight|ex500|lensx'), 'Fabricante_Laser'] = 'Alcon'
df.loc[equip.str.contains('zeiss|mel|visumax'), 'Fabricante_Laser'] = 'Zeiss'
df.loc[equip.str.contains('j&j|johnson|star|catalys'), 'Fabricante_Laser'] = 'J&J Vision'
df['Equipamento_Laser'] = df['Equipamento_Laser'].fillna('Desconhecido')
df['Equipamento_Laser'] = df['Equipamento_Laser'].replace(['-', 'N/A', 'n/a', 'na', '0', ''], 'Desconhecido')

# 3. Verificando o resultado das duas colunas lado a lado
print("Mapeamento de Equipamento vs Fabricante:")
print(df[['Equipamento_Laser', 'Fabricante_Laser']].head(10))
print("Distribuição de Market Share por Fabricante:")
print(df['Fabricante_Laser'].value_counts())

#Agora, analisando a coluna Faturamento_Consumiveis_Anual
df['Faturamento_Consumiveis_Anual'] = (
    df['Faturamento_Consumiveis_Anual']
    .astype(str)
    .str.strip()
    .str.replace('R$', '', regex=False)
    .str.replace('.', '',regex=False)
    .str.replace(',', '.', regex=False)
)
df['Faturamento_Consumiveis_Anual'] = pd.to_numeric(df['Faturamento_Consumiveis_Anual'], errors='coerce')

#Preenchendo eventuais nulos com a mediana
mediana_faturamento = df['Faturamento_Consumiveis_Anual'].median()
df['Faturamento_Consumiveis_Anual'] = df['Faturamento_Consumiveis_Anual'].fillna(mediana_faturamento)

print('Resumo dos consumíveis:')
print(df['Faturamento_Consumiveis_Anual'].describe())

# Por fim, as datas das últimas visitas
# Parseamento inteligente para datas com mistura de ISO e formato brasileiro
df['Ultima_Visita_Representante'] = pd.to_datetime(
    df['Ultima_Visita_Representante'], 
    format='mixed',      # Aceita ISO e BR na mesma coluna!
    dayfirst=True,       # Garante que 04/05 seja lido como 4 de Maio nas datas BR
    errors='coerce'      # Transforma eventuais textos inválidos em NaT (Not a Time)
)

# Conferindo a integridade temporal resultante
print("Tipo final da coluna:", df['Ultima_Visita_Representante'].dtype)
print("Visita mais antiga registrada:", df['Ultima_Visita_Representante'].min())
print("Visita mais recente registrada:", df['Ultima_Visita_Representante'].max())
print("Quantidade de datas inválidas/nulas:", df['Ultima_Visita_Representante'].isnull().sum())

#Ajustando a análise de datas para que seja possível clusterizar  (transforma datas para dias decorrido até data x, que será determinada por 31/12/2026)
data_referencia = pd.to_datetime('2026-12-31')
df['Dias_Sem_Visita'] = (data_referencia - df['Ultima_Visita_Representante']).dt.days
 # Para as clínicas sem registro, usaremos novamente a mediana
mediana_dias = df['Dias_Sem_Visita'].median()
df['Dias_Sem_Visita'] = df['Dias_Sem_Visita'].fillna(mediana_dias)
df['Dias_Sem_Visita'] = df['Dias_Sem_Visita'].astype(int)

print('Resumo de recência do relacionamento comercial (em dias):')
print(df['Dias_Sem_Visita'].describe())

# Salvando o dataset tratado e pronto para análise/modelagem
df.to_csv('oftalmo_clinicas_tratado.csv', index=False)
print("Arquivo 'oftalmo_clinicas_tratado.csv' gerado com sucesso!")