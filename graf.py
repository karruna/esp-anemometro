import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Suas credenciais do Firebase
API_KEY = "AIzaSyCxiLEH4iDh2ttozEZaUzJziYT4Os9Mdcg"
DATABASE_URL = "https://anemometro-710c6-default-rtdb.firebaseio.com/"

# Obter timestamp atual e calcular o intervalo das últimas 24 horas
now = datetime.now()
start_time = now - timedelta(hours=24*1)
start_timestamp = int(start_time.timestamp())

# Referência ao nó de aquisição
path = "acquisition/ESP1.json"
url = f"{DATABASE_URL}{path}"

# Obter dados do Firebase
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Erro ao acessar Firebase: {response.status_code}")
    exit()

# Filtrar dados das últimas 24 horas
filtered_data = {
    ts: values
    for ts, values in data.items()
    if int(ts) >= start_timestamp
}

# Listas para os gráficos
timestamps = []
vmin_values = []
vmed_values = []
vmax_values = []
wind_directions = []  # Nova lista para armazenar direções do vento

# Preparar os dados para os gráficos
for ts, values in sorted(filtered_data.items(), key=lambda x: int(x[0])):
    timestamp = datetime.fromtimestamp(int(ts))
    vmin = values.get('vmin', 0)
    vmed = values.get('vmed', 0)
    vmax = values.get('vmax', 0)
    wind_direction = values.get('dir', None)  # Extrair direção do vento

    # Filtrar valores acima de 200
    if vmax <= 200 and vmin < 70:
        timestamps.append(timestamp.strftime('%d/%m/%y  %H:%M'))  # Apenas horas e minutos
        vmin_values.append(vmin)
        vmed_values.append(vmed)
        vmax_values.append(vmax)
        wind_directions.append(wind_direction)

# print(wind_directions)
# Gerar gráfico de Vmin
fig1 = plt.figure(figsize=(14, 7))
plt.plot(timestamps, vmin_values, label="Vmin", color="blue", marker='.')
plt.xlabel('Horas')
plt.ylabel('Vmin')
plt.title('Gráfico de Vmin (Últimas 24 horas)')
plt.xticks(rotation=45, fontsize=8, ticks=range(0, len(timestamps), max(1, len(timestamps) // 10)))
plt.tight_layout()
plt.grid()
fig1.show()

# Gerar gráfico de Vmed
fig2 = plt.figure(figsize=(14, 7))
plt.plot(timestamps, vmed_values, label="Vmed", color="orange", marker='.')
plt.xlabel('Horas')
plt.ylabel('Vmed')
plt.title('Gráfico de Vmed (Últimas 24 horas)')
plt.xticks(rotation=45, fontsize=8, ticks=range(0, len(timestamps), max(1, len(timestamps) // 10)))
plt.tight_layout()
plt.grid()
fig2.show()

# Gerar gráfico de Vmax
fig3 = plt.figure(figsize=(14, 7))
plt.plot(timestamps, vmax_values, label="Vmax", color="green", marker='.')
plt.xlabel('Horas')
plt.ylabel('Vmax')
plt.title('Gráfico de Vmax (Últimas 24 horas)')
plt.xticks(rotation=45, fontsize=8, ticks=range(0, len(timestamps), max(1, len(timestamps) // 10)))
plt.tight_layout()
plt.grid()
fig3.show()

# Gerar o gráfico
fig4 = plt.figure(figsize=(14, 7))
plt.plot(timestamps, vmin_values, label="Vmin", marker='.')
plt.plot(timestamps, vmed_values, label="Vmed", marker='.')
plt.plot(timestamps, vmax_values, label="Vmax", marker='.')
plt.xlabel('Horas')
plt.ylabel('Valores')
plt.title('Gráfico de Vmin, Vmed e Vmax (Últimas 24 horas)')
plt.xticks(rotation=45, fontsize=8, ticks=range(0, len(timestamps), max(1, len(timestamps) // 10)))
plt.legend()  # Adicionar a legenda
plt.tight_layout()
plt.grid()
fig4.show()

# Agrupar os dados por direção e contar a frequência
wind_df = pd.DataFrame({'direction': wind_directions})
wind_counts = wind_df['direction'].value_counts()

# Ordenar as direções para garantir uma visualização consistente
order = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
wind_counts = wind_counts.reindex(order)

# Criar o gráfico polar
fig5 = plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)

# Plotar os dados
angles = np.linspace(0, 2*np.pi, len(wind_counts), endpoint=False)
ax.plot(angles, wind_counts, 'o-', linewidth=2)

# Configurar os rótulos
ax.set_thetagrids(angles * 180/np.pi, labels=order)
ax.set_title('Frequência de Direções do Vento')

# Mostrar o gráfico
fig5.show()

# Manter os gráficos abertos
plt.ioff()
plt.show()