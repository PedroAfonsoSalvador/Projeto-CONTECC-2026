import pandas as pd
import holidays

print("Iniciando o processamento dos dados...")

#Carregar as três bases.
df_industria = pd.read_csv("data/Steel_industry_data.csv")
df_carbono = pd.read_csv("data/intensidade_carbono_2018_15min.csv")
df_clima = pd.read_csv("data/clima_2018_coreia.csv")

#Processar a base de Carbono.
df_carbono = df_carbono[['datetime', 'carbonIntensity']]
df_carbono['datetime'] = pd.to_datetime(df_carbono['datetime']).dt.tz_localize(None)

#Processar a base de Clima (Criar coluna datetime a partir de Ano, Mês, Dia e Hora).
df_clima = df_clima.rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'})
df_clima['datetime_clima'] = pd.to_datetime(df_clima[['year', 'month', 'day', 'hour']])
#Descarta colunas separadas de tempo 
df_clima = df_clima.drop(columns=['year', 'month', 'day', 'hour'])

#Ajustar a base da indústria
df_industria['date'] = pd.to_datetime(df_industria['date'], dayfirst=True)

#MERGE 1: Indústria + Carbono
df_final = pd.merge_asof(
    df_industria.sort_values('date'),
    df_carbono.sort_values('datetime'),
    left_on='date',
    right_on='datetime',
    direction='nearest'
)

#MERGE 2: Base Atual + Clima 
df_final = pd.merge_asof(
    df_final.sort_values('date'),
    df_clima.sort_values('datetime_clima'),
    left_on='date',
    right_on='datetime_clima',
    direction='backward'
)


#Adicionar Feriados da Coreia do Sul (2018)
feriados_kr = holidays.KR(years=2018)

#Pega todas as datas dos feriados e transforma em uma lista de strings ('2018-01-01', etc)
lista_datas_feriados = [str(data) for data in feriados_kr.keys()]

#Converte a coluna de data do Pandas para string e verifica se está na lista
df_final['Is_Holiday'] = df_final['date'].dt.strftime('%Y-%m-%d').isin(lista_datas_feriados).astype(int)

print(f"\nTotal de medições em feriados: {df_final['Is_Holiday'].sum()}")


#Remover colunas de data extras
df_final = df_final.drop(columns=['datetime', 'datetime_clima'])

#Calcular a emissão real
df_final['Real_CO2_kg'] = (df_final['Usage_kWh'] * df_final['carbonIntensity']) / 1000


#Lista com a coluna de CO2 antiga e todas as colunas elétricas que não serão usadas no modelo
colunas_para_remover = [
    'CO2(tCO2)',
    'Lagging_Current_Reactive.Power_kVarh',
    'Leading_Current_Reactive_Power_kVarh',
    'Lagging_Current_Power_Factor',
    'Leading_Current_Power_Factor'
]

df_final = df_final.drop(columns=colunas_para_remover, errors='ignore')


#Salva a base definitiva
df_final.to_csv("data/base_finalizada.csv", index=False)

print("\nBase final criada com sucesso! Clima, Feriados integrados e colunas não utilizadas foram removidas.")
print(df_final.head())