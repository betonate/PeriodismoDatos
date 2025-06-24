import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar archivos
jordan_df = pd.read_csv("jordan_career.csv")
lebron_df = pd.read_csv("lebron_career.csv")

# Asegurar tipo datetime
jordan_df['date'] = pd.to_datetime(jordan_df['date'])
lebron_df['date'] = pd.to_datetime(lebron_df['date'])

# Agregar columnas auxiliares
for df in [jordan_df, lebron_df]:
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.day // 7
    df['weekday'] = df['date'].dt.weekday

# Agrupar por mes, semana y día
jordan_grouped = jordan_df.groupby(['month', 'week', 'weekday'])['pts'].mean()
lebron_grouped = lebron_df.groupby(['month', 'week', 'weekday'])['pts'].mean()

# Pivotear
pivot_jordan = jordan_grouped.unstack(level=-1)
pivot_lebron = lebron_grouped.unstack(level=-1)

# Meses válidos
valid_months = sorted(set(pivot_jordan.index.get_level_values(0)).union(set(pivot_lebron.index.get_level_values(0))))
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Función para rellenar grilla 5x7
def pad_month(df, month):
    grid = pd.DataFrame(index=range(5), columns=range(7))
    if month in df.index:
        month_data = df.loc[month]
        for week in month_data.index:
            for day in month_data.columns:
                grid.loc[week, day] = month_data.loc[week, day]
    return grid.astype(float)

# Crear visualización
fig, axes = plt.subplots(len(valid_months), 2, figsize=(12, len(valid_months) * 2.2))
plt.subplots_adjust(hspace=0.8)

for i, month in enumerate(valid_months):
    ax_jordan = axes[i, 0]
    ax_lebron = axes[i, 1]

    jordan_month = pad_month(pivot_jordan, month)
    lebron_month = pad_month(pivot_lebron, month)

    sns.heatmap(jordan_month, cmap="Blues", ax=ax_jordan, cbar=False, linewidths=0.5, linecolor='gray', square=True, vmin=0)
    ax_jordan.set_title(f"{month_names[month - 1]} - Jordan", fontsize=10)
    ax_jordan.set_xticks(range(7))
    ax_jordan.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], fontsize=7)
    ax_jordan.set_yticks([])

    sns.heatmap(lebron_month, cmap="Blues", ax=ax_lebron, cbar=False, linewidths=0.5, linecolor='gray', square=True, vmin=0)
    ax_lebron.set_title(f"{month_names[month - 1]} - LeBron", fontsize=10)
    ax_lebron.set_xticks(range(7))
    ax_lebron.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], fontsize=7)
    ax_lebron.set_yticks([])

# Título general y guardado
plt.suptitle("Comparación mensual - Promedio de puntos por día (Jordan vs LeBron)", fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("jordan_vs_lebron_heatmap_final.png", dpi=300)
plt.close()
print("✅ Imagen generada: jordan_vs_lebron_heatmap_final.png")
