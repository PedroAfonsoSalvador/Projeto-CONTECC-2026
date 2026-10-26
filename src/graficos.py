import os
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Carregando recursos e gerando todos os gráficos...")

#Garantir que a pasta 'imagens' exista
os.makedirs("imagens", exist_ok=True)
caminho_csv = Path(__file__).resolve().parent.parent / "data" / "base_finalizada.csv"

# ==========================================
# GRÁFICO 1: Tabela de Métricas
# ==========================================
modelo_rf = joblib.load("models/modelo_rf.pkl")
X_test, y_test = joblib.load("models/dados_teste.pkl")

previsoes = modelo_rf.predict(X_test)
r2 = r2_score(y_test, previsoes)
mae = mean_absolute_error(y_test, previsoes)
rmse = np.sqrt(mean_squared_error(y_test, previsoes))

dados_tabela = [
    ["Coeficiente de Determinação (R²)", f"{(r2 * 100):.2f}%"],
    ["Erro Médio Absoluto (MAE)", f"{(mae * 100):.2f}%"],
    ["Raiz do Erro Quadrático Médio (RMSE)", f"{(rmse * 100):.2f}%"]
]

fig, ax = plt.subplots(figsize=(10, 3))
ax.axis('tight')
ax.axis('off')
tabela = ax.table(cellText=dados_tabela, colLabels=["Métrica", "Valor"], loc='center', cellLoc='left')
tabela.auto_set_font_size(False)
tabela.set_fontsize(12)
tabela.scale(1.2, 2.0)
plt.savefig("imagens/resultados_metricas.png", bbox_inches='tight', pad_inches=0.5, dpi=300)
plt.close()
print(" -> Gráfico 1 gerado: resultados_metricas.png")


# ==========================================
# GRÁFICO 2: Distribuição por Tipo de Carga
# ==========================================
df_cargas = pd.read_csv(caminho_csv)
df_cargas.columns = df_cargas.columns.str.replace(';', '').str.strip()

cargas_count = df_cargas['Load_Type'].value_counts().sort_index()
total = len(df_cargas)

labels = ['Carga Leve\n(Light Load)', 'Carga Média\n(Medium Load)', 'Carga Máxima\n(Maximum Load)']
counts = [cargas_count.iloc[0], cargas_count.iloc[1], cargas_count.iloc[2]]
cores = ['#2b5c8f', '#e67e22', '#d9534f']

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

bars = ax.bar(labels, counts, color=cores, width=0.55, edgecolor='black', alpha=0.85)

for bar, count in zip(bars, counts):
    height = bar.get_height()
    pct = (count / total) * 100
    ax.annotate(f'{count:,}\n({pct:.1f}%)'.replace(',', '.'),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_xlabel('Regime de Operação da Fábrica (Load Type)', fontsize=13, fontweight='bold', labelpad=10)
ax.set_ylabel('Número de Registros', fontsize=13, fontweight='bold', labelpad=10)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
ax.set_ylim(0, 23000)
plt.tight_layout()

plt.savefig("imagens/grafico_distribuicao_cargas.png", dpi=300)
plt.close()
print(" -> Gráfico 2 gerado: grafico_distribuicao_cargas.png")


# ==========================================
# GRÁFICO 3: Dispersão (Reais vs Previstos)
# ==========================================
plt.figure(figsize=(8, 8))
plt.scatter(y_test, previsoes, alpha=0.4, color='#2980b9', edgecolors='none', s=25, label='Previsões vs Reais')

min_val = min(y_test.min(), previsoes.min())
max_val = max(y_test.max(), previsoes.max())
plt.plot([min_val, max_val], [min_val, max_val], color='#e74c3c', linestyle='--', linewidth=2, label='Previsão Perfeita (y = x)')

plt.title('Gráfico de Dispersão: Valores Reais vs. Previstos (Random Forest)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Valores Reais de Consumo (Usage_kWh)', fontsize=12)
plt.ylabel('Valores Previstos pelo Modelo (Usage_kWh)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)

plt.text(0.05, 0.92, f'R² = {r2*100:.2f}%', transform=plt.gca().transAxes,
         fontsize=12, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', edgecolor='#bdc3c7'))

plt.legend(loc='lower right', fontsize=11)
plt.tight_layout()

plt.savefig("imagens/grafico_dispersao.png", dpi=300)
plt.close()
print(" -> Gráfico 3 gerado: grafico_dispersao.png")

print("\nConcluído! Todos os gráficos foram gerados com sucesso na pasta 'imagens'.")