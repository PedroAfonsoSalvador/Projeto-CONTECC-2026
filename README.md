# 🏭 Desenvolvimento de um Modelo de Aprendizado de Máquina para Avaliação e Otimização do Consumo Energético

Repositório oficial do projeto de pesquisa voltado à previsão de demanda de energia e eficiência energética no setor industrial siderúrgico utilizando **Aprendizado de Máquina (Machine Learning)**. O estudo integra dados operacionais, meteorológicos e de intensidade de carbono da rede elétrica.

---

## 📂 Estrutura do Repositório

O projeto está organizado da seguinte forma, separando código-fonte, dados, modelos treinados e saídas visuais:

```text
Projeto-CONTECC-2026/
│
├── data/                      # Bancos de dados brutos e tratados
│   ├── base_finalizada.csv
│   ├── clima_2018_coreia.csv
│   ├── intensidade_carbono_2018_15min.csv
│   └── Steel_industry_data.csv
│
├── imagens/                   # Gráficos e tabelas gerados pelo modelo
│   ├── grafico_dispersao.png
│   ├── grafico_distribuicao_cargas.png
│   └── resultados_metricas.png
│
├── models/                    # Modelos e partições de teste serializadas (.pkl)
│   ├── dados_teste.pkl
│   └── modelo_rf.pkl
│
├── src/                       # Scripts de processamento, treino e geração de gráficos
│   ├── captura_dados_co2.py
│   ├── graficos.py
│   ├── pre_processamento.py
│   ├── random_forest.py
│   └── unir_bases.py
│
├── Artigo CONTECC - Pedro Afonso Cavalcanti Salvador.pdf  # Artigo científico do projeto
├── requirements.txt           # Dependências do projeto
└── README.md                  # Documentação do repositório

```

---

## 🎯 Sobre o Projeto

O crescimento da demanda global por energia exige soluções inovadoras para otimizar o consumo industrial e mitigar a pegada de carbono. Este trabalho utiliza o algoritmo preditivo **Random Forest Regressor** para prever o consumo de energia (`Usage_kWh`) de uma indústria siderúrgica com **60 minutos de antecedência**, operando em intervalos de 15 minutos.

A pesquisa combina três fontes principais de dados:

1. **Dados Operacionais da Indústria:** Registros de consumo de uma siderúrgica (Coreia do Sul, 2018).


2. **Intensidade de Carbono da Rede:** Dados coletados via API do *Electricity Maps*.


3. **Parâmetros Meteorológicos:** Variáveis locais (temperatura, umidade, radiação solar) extraídas da plataforma *NASA POWER*.



---

## 📊 Resultados e Desempenho

O modelo alcançou alta precisão preditiva na captura dos padrões operacionais e não lineares da fábrica:

| Métrica | Símbolo / Sigla | Valor Alcançado |
| --- | --- | --- |
| **Coeficiente de Determinação** | $R^2$ | **78,00%**

 |
| **Erro Médio Absoluto** | $\text{MAE}$ | **5,01%**

 |
| **Raiz do Erro Quadrático Médio** | $\text{RMSE}$ | **9,36%**

 |

A análise de importância das variáveis (*Feature Importance*) revelou que a variável de atraso temporal de 60 minutos (`Usage_kWh_60min_atras`) possui o maior peso explicativo (54,79%), evidenciando a forte dependência temporal dos equipamentos de grande porte da siderurgia.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

O projeto foi desenvolvido em **Python**, fazendo uso das seguintes bibliotecas principais:

* **Pandas & NumPy:** Manipulação, cruzamento e estruturação de bases de dados.


* **Scikit-Learn:** Pré-processamento (`MinMaxScaler`), divisão de dados, treinamento do `RandomForestRegressor` e cálculo de métricas.


* **Joblib:** Serialização e salvamento do modelo treinado.


* **Matplotlib:** Visualização de dados e geração de gráficos institucionais.


* **Requests:** Comunicação com a API do Electricity Maps.


* **Holidays:** Mapeamento de feriados oficiais da Coreia do Sul para o ano de 2018.



---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos e Instalação

Clone o repositório e instale as dependências necessárias utilizando o arquivo `requirements.txt`:

```bash
git clone [https://github.com/seu-usuario/Projeto-CONTECC-2026.git](https://github.com/seu-usuario/Projeto-CONTECC-2026.git)
cd Projeto-CONTECC-2026

# Criar e ativar um ambiente virtual (recomendado)
python -m venv .venv
# No Windows (PowerShell):
.venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt

```

### 2. Executando o Pipeline de Dados e Machine Learning

Os scripts dentro da pasta `src/` devem ser executados na ordem lógica de engenharia de dados e modelagem:

1. **Coleta de dados de carbono (Opcional, já inclusa):**
```bash
python src/captura_dados_co2.py

```


2. **União das bases (Indústria + Carbono + Clima + Feriados):**
```bash
python src/unir_bases.py

```


3. **Pré-processamento e normalização:**
```bash
python src/pre_processamento.py

```


4. **Treinamento do modelo Random Forest:**
```bash
python src/random_forest.py

```


5. **Geração dos gráficos e tabelas de resultados:**
```bash
python src/graficos.py

```



As imagens geradas serão automaticamente armazenadas na pasta `imagens/`.

---

## 👥 Autor

* **Pedro Afonso Cavalcanti Salvador** — *Estudante de Engenharia da Computação (UPE)*

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e científicos no âmbito do Congresso Técnico Científico da Agronomia e Engenharias (**CONTECC**).