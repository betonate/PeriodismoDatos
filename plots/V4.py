import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = [
    {
        "Player": "Michael Jordan",
        "PTS": 30.1,
        "REB": 6.2,
        "AST": 5.3,
        "STL": 2.3,
        "BLK": 0.8,
    },
    {
        "Player": "LeBron James",
        "PTS": 27.1,
        "REB": 7.5,
        "AST": 7.4,
        "STL": 1.5,
        "BLK": 0.8,
    },
]

df = pd.DataFrame(data)


#Normalización [0, 1]

metrics = ["PTS", "REB", "AST", "STL", "BLK"]
df_norm = df.copy()
for col in metrics:
    max_val = df[col].max()
    df_norm[col] = df[col] / max_val


angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]  # cerrar el círculo

def plot_radar(ax, values, label):
    values = values.tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, label=label)
    ax.fill(angles, values, alpha=0.25)

fig = plt.figure(figsize=(6, 6))
ax = plt.subplot(111, polar=True)
plot_radar(ax, df_norm.loc[0, metrics], "Michael Jordan")
plot_radar(ax, df_norm.loc[1, metrics], "LeBron James")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics)
ax.set_yticks([])
ax.set_title("Comparación Normalizada – Jordan vs LeBron", y=1.08, fontsize=14, weight="bold")
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.show()
