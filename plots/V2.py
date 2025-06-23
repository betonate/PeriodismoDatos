import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivo CSV (asegúrate de tenerlo en la misma carpeta)
df = pd.read_csv("responses_form_binario.csv")

# Identificar columnas de país e impacto
cols_pais = [col for col in df.columns if col.startswith("País_")]
cols_impacto = [
    'Impacto_Poco importante',
    'Impacto_Medianamente importante',
    'Impacto_Muy importante',
    'Impacto_Fundamental'
]

# Obtener país más votado por cada persona
df['Pais'] = df[cols_pais].idxmax(axis=1).str.replace("País_", "")

# Mapear escala de impacto (1 a 5)
impacto_map = {
    'Impacto_Poco importante': 2,
    'Impacto_Medianamente importante': 3,
    'Impacto_Muy importante': 4,
    'Impacto_Fundamental': 5
}
df['Impacto'] = 0
for col, val in impacto_map.items():
    df['Impacto'] += df[col] * val

# Crear el gráfico Violin
plt.figure(figsize=(10, 6))
sns.violinplot(data=df, x="Impacto", y="Pais", palette="pastel", inner="quartile")
plt.title("Distribución del impacto percibido por país")
plt.xlabel("Impacto percibido (escala 1 a 5)")
plt.ylabel("País mencionado")
plt.tight_layout()
plt.show()
