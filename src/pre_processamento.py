import pandas as pd
from sklearn.preprocessing import MinMaxScaler

print("Iniciando o pré-processamento para Machine Learning...")

#Carregar a base final
df = pd.read_csv("data/base_finalizada.csv")

#Remove a coluna de CO2 real para evitar o Data Leakage.
if 'Real_CO2_kg' in df.columns:
    df = df.drop(columns=['Real_CO2_kg'])


#ETAPA 1: Transformar Textos em Números
print("Aplicando Encoding nas variáveis categóricas...")

#Mapeamento Binário (WeekStatus)
df['WeekStatus'] = df['WeekStatus'].map({'Weekday': 1, 'Weekend': 0})

#Mapeamento Ordinal (Load_Type)
ordem_carga = {'Light_Load': 0, 'Medium_Load': 1, 'Maximum_Load': 2}
df['Load_Type'] = df['Load_Type'].map(ordem_carga)

#One-Hot Encoding (Day_of_week)
df = pd.get_dummies(df, columns=['Day_of_week'])

#Converte as novas colunas booleanas geradas pelo get_dummies em 0 e 1
colunas_bool = df.select_dtypes(include=['bool']).columns
df[colunas_bool] = df[colunas_bool].astype(int)


#ETAPA 2: Lidar com a coluna Date
print("Extraindo sazonalidade e ajustando o índice de tempo...")

df['date'] = pd.to_datetime(df['date'])

#Extrai Mês e Hora como variáveis de sazonalidade
df['Month'] = df['date'].dt.month
df['Hour'] = df['date'].dt.hour

#Transforma a data no índice (index) do dataframe
df = df.set_index('date')

#ETAPA 3: Normalização (Scaling)
print("Normalizando variáveis contínuas...")

colunas_desejadas = [
    'Usage_kWh', 'NSM', 'carbonIntensity', 
    'T2M', 'RH2M', 'ALLSKY_SFC_SW_DWN', 'PRECTOTCORR'
]

colunas_para_escalonar = [col for col in colunas_desejadas if col in df.columns]

colunas_faltantes = set(colunas_desejadas) - set(colunas_para_escalonar)
if colunas_faltantes:
    print(f"Aviso: As seguintes colunas não foram encontradas e serão ignoradas: {colunas_faltantes}")

scaler = MinMaxScaler()

#Aplica a transformação apenas nas colunas que o Python confirmou que existem
if colunas_para_escalonar:
    df[colunas_para_escalonar] = scaler.fit_transform(df[colunas_para_escalonar])


df.to_csv("data/base_finalizada.csv")

print("\nPré-processamento concluído com sucesso!")
print(df.head())