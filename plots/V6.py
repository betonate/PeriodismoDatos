import pandas as pd
import matplotlib.pyplot as plt

# Cargar archivos
jordan_path = r"C:\Users\revec\.cache\kagglehub\datasets\edgarhuichen\nba-players-career-game-log\versions\2\jordan_career.csv"
lebron_path = r"C:\Users\revec\.cache\kagglehub\datasets\edgarhuichen\nba-players-career-game-log\versions\2\lebron_career.csv"

df_jordan = pd.read_csv(jordan_path)
df_lebron = pd.read_csv(lebron_path)

# Convertir fechas
df_jordan['date'] = pd.to_datetime(df_jordan['date'])
df_jordan['year'] = df_jordan['date'].dt.year

df_lebron['date'] = pd.to_datetime(df_lebron['date'])
df_lebron['year'] = df_lebron['date'].dt.year

# Filtrar temporadas
jordan_86_87 = df_jordan[
    ((df_jordan['year'] == 1986) & (df_jordan['date'].dt.month >= 10)) |
    ((df_jordan['year'] == 1987) & (df_jordan['date'].dt.month <= 6))
]

lebron_05_06 = df_lebron[
    ((df_lebron['year'] == 2005) & (df_lebron['date'].dt.month >= 10)) |
    ((df_lebron['year'] == 2006) & (df_lebron['date'].dt.month <= 6))
]

# 🔁 Conversión de minutos
def convertir_minutos(s):
    try:
        minutos, segundos = map(int, s.split(":"))
        return minutos + segundos / 60
    except:
        return None

jordan_86_87['mp'] = jordan_86_87['mp'].apply(convertir_minutos)
lebron_05_06['mp'] = lebron_05_06['mp'].apply(convertir_minutos)

# Estadísticas alternativas
def resumen_estadisticas_alt(df):
    return {
        'Minutos': df['mp'].mean(),
        'FG%': df['fgp'].mean(),
        '3P%': df['threep'].mean(),
        'FT%': df['ftp'].mean(),
        'Pérdidas': df['tov'].mean()
    }

jordan_stats = resumen_estadisticas_alt(jordan_86_87)
lebron_stats = resumen_estadisticas_alt(lebron_05_06)

# Dataset de burbujas
datos = []
for stat, value in jordan_stats.items():
    datos.append({'Estadística': stat, 'Jugador': 'Jordan (86-87)', 'Valor': value})
for stat, value in lebron_stats.items():
    datos.append({'Estadística': stat, 'Jugador': 'LeBron (05-06)', 'Valor': value})

df_burbujas = pd.DataFrame(datos)

# Posiciones en X
estadisticas = ['Minutos', 'FG%', '3P%', 'FT%', 'Pérdidas']
x_map = {stat: i for i, stat in enumerate(estadisticas)}
df_burbujas['x'] = df_burbujas['Estadística'].map(x_map)

# Colores por jugador
colores = {'Jordan (86-87)': '#E03A3E', 'LeBron (05-06)': '#552583'}
df_burbujas['color'] = df_burbujas['Jugador'].map(colores)


def escalar_tamano(valores, min_size=300, max_size=1200):
    min_val, max_val = min(valores), max(valores)
    if max_val == min_val:
        return [min_size for _ in valores]
    return [min_size + (v - min_val) / (max_val - min_val) * (max_size - min_size) for v in valores]

df_burbujas['tamano'] = escalar_tamano(df_burbujas['Valor'])

# Graficar burbujas
plt.figure(figsize=(10, 6))
for jugador in df_burbujas['Jugador'].unique():
    sub_df = df_burbujas[df_burbujas['Jugador'] == jugador]
    plt.scatter(sub_df['x'], sub_df['Valor'],
                s=sub_df['tamano'], alpha=0.6, c=sub_df['color'],
                label=jugador, edgecolors='k', linewidths=1)

# Estética
plt.xticks(ticks=range(len(estadisticas)), labels=estadisticas)
plt.ylabel("Promedio por partido (%) o valor")
plt.title("Estadísticas Avanzadas (Escaladas)\nJordan (1986-87) vs LeBron (2005-06)", fontsize=14)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()
