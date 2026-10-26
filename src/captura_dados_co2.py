import requests
import pandas as pd
from datetime import datetime, timedelta
import time

#Configurações da API
TOKEN = "em_2MMgPyf9mvt544NXsfcTQbkQKHH6HCSR"
ZONE = "KR" 
GRANULARITY = "15_minutes"

headers = {
    "auth-token": TOKEN
}

#Configurar o período
start_date = datetime(2018, 1, 1)
end_date = datetime(2018, 12, 31)

#Lista vazia que vai guardar todos os dados coletados
all_data = []

#Data que vai ser atualizada a cada passo do loop
current_start = start_date

print("Iniciando a coleta de dados da API...")

#Loop de 3 em 3 dias (limite da API para 15_minutes)
while current_start < end_date:
    #Calcula a data de fim do bloco atual (+ 3 dias)
    current_end = current_start + timedelta(days=3)
    
    #Se o fim do bloco ultrapassar o final do ano, ajusta para o fim do ano
    if current_end > end_date:
        current_end = end_date
        
    #Formata as datas para o padrão que a API exige (ISO 8601)
    str_start = current_start.strftime("%Y-%m-%dT00:00:00.000Z")
    str_end = current_end.strftime("%Y-%m-%dT00:00:00.000Z")
    
    #Monta a URL
    url = f"https://api.electricitymaps.com/v4/carbon-intensity/past-range?zone={ZONE}&start={str_start}&end={str_end}&temporalGranularity={GRANULARITY}"
    
    #Faz a requisição
    print(f"Baixando período: {str_start[:10]} a {str_end[:10]}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        json_data = response.json()
        
        #Pega a lista de medições
        if 'data' in json_data:
            all_data.extend(json_data['data'])
            
    else:
        print(f"Erro na requisição: {response.status_code}")
        print(response.text)
        break 
        
    #Atualiza o current_start para o próximo ciclo
    current_start = current_end
    
    #Pausa de 1.5 segundos para não sobrecarregar a API e evitar bloqueio
    time.sleep(1.5)

#Converter tudo para DataFrame e salvar em CSV
if all_data:
    df_carbono = pd.DataFrame(all_data)
    
    #Salva o arquivo CSV no seu computador
    df_carbono.to_csv("data/intensidade_carbono_2018_15min.csv", index=False)
    
    print("\nSucesso! Arquivo 'intensidade_carbono_2018_15min.csv' gerado.")
    print(f"Total de linhas coletadas: {len(df_carbono)}")
else:
    print("Nenhum dado foi coletado. Verifique os erros acima.")