import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("resultados-comparativa.csv")

plt.figure(figsize=(8, 5))
plt.bar(df["modelo"], df["tiempo_segundos"], color=["#007acc", "#f28e2b", "#76b041"])
plt.title("Comparativa de tiempos de respuesta entre modelos")
plt.xlabel("Modelo")
plt.ylabel("Tiempo (segundos)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig("grafico_resultado.png")
plt.show()