import os
import pandas as pd
import numpy as np
import joblib  
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Iniciando a criação do modelo Random Forest...")

#Carregar a base e limpar
df = pd.read_csv("data/base_finalizada.csv", index_col="date")
df.columns = df.columns.str.replace(';', '').str.strip()
df = df.replace(r';+', '', regex=True)
df = df.replace(r'\s+', '', regex=True)
df = df.apply(pd.to_numeric, errors='coerce')
df.fillna(0.0, inplace=True)

df['Usage_kWh_60min_atras'] = df['Usage_kWh'].shift(4)
df.dropna(inplace=True)

y = df['Usage_kWh']
colunas_vazadas = [
    'Lagging_Current_Reactive.Power_kVarh', 
    'Leading_Current_Reactive_Power_kVarh', 
    'Lagging_Current_Power_Factor', 
    'Leading_Current_Power_Factor'
]
colunas_vazadas_presentes = [col for col in colunas_vazadas if col in df.columns]
X = df.drop(columns=['Usage_kWh'] + colunas_vazadas_presentes)

#Divisão
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, shuffle=False)

#Treinamento
print("Treinando o Random Forest...")
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
modelo_rf.fit(X_train, y_train)

#Cria a pasta 'models' se ela não existir
os.makedirs("models", exist_ok=True)

#Salva o modelo treinado e os dados de teste em arquivos locais
joblib.dump(modelo_rf, "models/modelo_rf.pkl")
joblib.dump((X_test, y_test), "models/dados_teste.pkl")

print("\nSucesso! Modelo e dados salvos na pasta 'models'.")