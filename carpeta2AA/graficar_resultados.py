import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leer CSV
df = pd.read_csv("resultados_por_pregunta.csv")

# ==============================
# 1. Tiempo por pregunta y modelo
# ==============================
plt.figure(figsize=(14, 6))
sns.barplot(data=df, x="modelo", y="tiempo_segundos", hue="pregunta")
plt.legend([],[], frameon=False)
plt.title("Tiempo por pregunta y modelo")
plt.xticks(rotation=0)
plt.ylabel("Tiempo (segundos)")
plt.tight_layout()
plt.savefig("tiempos_por_pregunta.png")
plt.show()
plt.close()  # ✅ Cierra la figura para evitar sobreposición

# ==============================
# 2. Tiempo promedio por modelo
# ==============================
media = df.groupby("modelo")["tiempo_segundos"].mean().reset_index()

plt.figure(figsize=(6, 5))
sns.barplot(data=media, x="modelo", y="tiempo_segundos")
plt.title("Tiempo promedio por modelo")
plt.ylabel("Tiempo medio (segundos)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("tiempo_promedio_modelo.png")
plt.show()
plt.close()  # ✅ Cierra la figura

print("\n📊 Tiempo medio por modelo (segundos):")
print(media)

# ==============================
# 3. Boxplot (variabilidad por modelo)
# ==============================
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="modelo", y="tiempo_segundos")
plt.title("Distribución de tiempos por modelo")
plt.ylabel("Tiempo (segundos)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("distribucion_tiempos.png")
plt.show()
plt.close()  # ✅ Cierra la figura