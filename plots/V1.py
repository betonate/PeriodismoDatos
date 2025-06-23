import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("Team_Stats_Per_Game.csv")

df["pts_per_game"] = pd.to_numeric(df["pts_per_game"], errors="coerce")
df_clean = df.dropna(subset=["pts_per_game"])

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_clean, x="pts_per_game", inner="quartile", color="skyblue")

plt.title("Distribución del promedio de puntos por equipo - NBA 2025", fontsize=14, weight='bold')
plt.xlabel("Puntos por partido")
plt.yticks([]) 

plt.tight_layout()
plt.savefig("violinplot_pts_per_game_nba2025.png", dpi=300)  

plt.show()
