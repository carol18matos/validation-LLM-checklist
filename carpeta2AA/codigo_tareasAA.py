from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import preprocessing
import numpy as np
from sklearn.metrics import classification_report,confusion_matrix,precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sbn

df = pd.read_csv("/content/drive/MyDrive/AAColab/malware_dataset.csv")

#Visualizar contenido (primeras filas)
df.head()

#Visualizar dimensiones del dataset
print(df.shape)

#Visualizar estadísticas descriptivas del dataset
df.describe()

#Visualizar información
df.info()

print(df.columns)

#Sentencia para borrar filas idénticas
df.drop_duplicates()

null_counts = df.isnull().sum()
null_counts[null_counts > 0]

# Separar las características (X) y la etiqueta (y)
X = df.drop("class", axis=1)
Y = df["class"].copy()

#Buscar valores string en el dataset
object_columns = X.select_dtypes(include=['object']).columns
print(object_columns)

for column in object_columns:
    print(f"\nColumna: {column}")
    print(X[column].unique())
    print('\n')
	
# Sustituir valores "?" por NaN
X["TelephonyManager.getSimCountryIso"] = pd.to_numeric(X["TelephonyManager.getSimCountryIso"], errors='coerce')

# Comprobar cuantos valores faltantes hay
num_na = X['TelephonyManager.getSimCountryIso'].isna().sum()
print("El total de valores faltantes es " + str(num_na))

# Sustituir valores "?" por NaN
X["TelephonyManager.getSimCountryIso"] = pd.to_numeric(X["TelephonyManager.getSimCountryIso"], errors='coerce')

# Comprobar cuantos valores faltantes hay
num_na = X['TelephonyManager.getSimCountryIso'].isna().sum()
print("El total de valores faltantes es " + str(num_na))

# Convertir la columna a tipo numérico
X["TelephonyManager.getSimCountryIso"] = X["TelephonyManager.getSimCountryIso"].astype(np.int64)

# Lista de valores binarios permitidos
valores_binarios = [0, 1]

# Comprobar si todos los valores en el DataFrame son binarios
son_binarios = X.isin(valores_binarios).all().all()

if son_binarios:
    print("Todos los datos en el DataFrame son binarios.")
else:
    print("No todos los datos en el DataFrame son binarios.")
	
	# Visualizar información del dataset
X.info()

#Dividimos los datos en conjuntos de entrenamiento y pruebas
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Se juntan las características de entrada y salida
combined_df = pd.concat([X_train, y_train], axis=1)

# Se comprueba el equilibrio del dataset una vez balanceado
class_distribution = combined_df['class'].value_counts()

# Se comprueba el número de instancias de cada tipo
class_distribution = df['class'].value_counts()
print(class_distribution)

plt.figure(figsize=(5, 5))
class_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribución de las clases')
plt.xlabel('Clases')
plt.ylabel('Número de instancias')
plt.show()

from imblearn.over_sampling import SMOTE

# Crear un objeto SMOTE
smote = SMOTE(random_state=42)

# Aplicar SMOTE a tu dataset
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# Se juntan las características de entrada y salida
combined_df = pd.concat([X_resampled, y_resampled], axis=1)

# Se comprueba el equilibrio del dataset una vez balanceado
class_distribution = combined_df['class'].value_counts()
print(class_distribution)

plt.figure(figsize=(5, 5))
class_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribución de las clases')
plt.xlabel('Clases')
plt.ylabel('Número de instancias')
plt.show()

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

# Crea un objeto SelectKBest con la prueba f score y especifica el número de características que deseas seleccionar (k)
selector = SelectKBest(score_func=f_classif, k=150)  # Selecciona las k mejores características

# Ajusta el selector a tus datos
X_selection = selector.fit_transform(X_train, y_train) #En X_new se guardan las carácteristicas seleccionadas
X_test_selection = selector.transform(X_test)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#Inicializar el modelo
logistic_regression = LogisticRegression(max_iter=3000)
logistic_regression.fit(X_resampled, y_resampled)

 # ajustamos el modelo
y_pred = logistic_regression.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy}")

#Aplicamos SMOTE en X e Y para la validación cruzada
X_smote, y_smote = smote.fit_resample(X, Y)

#Validación cruzada
from sklearn.model_selection import cross_val_score
from sklearn import metrics
clf = logistic_regression = LogisticRegression(max_iter=3000)
scores = cross_val_score(
    clf, X, Y, cv=10, scoring='accuracy')
scores

print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn.neighbors import KNeighborsClassifier

# Método para calcular número de vecinos óptimo
k_range = range(1, 20)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors = k,weights='distance')
    knn.fit(X_train, y_train)
    scores.append(knn.score(X_test, y_test))
plt.figure()
plt.xlabel('k')
plt.ylabel('accuracy')
plt.scatter(k_range, scores)
plt.xticks([0,5,10,15,20])

#Algoritmo KNN
neigh = KNeighborsClassifier(n_neighbors=4, weights='distance')
neigh.fit(X_train, y_train)
y_pred = neigh.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy}")

#Validación cruzada
from sklearn.model_selection import cross_val_score
from sklearn import metrics
clf = neigh = KNeighborsClassifier(n_neighbors=4, weights='distance')
scores = cross_val_score(
    clf, X, Y, cv=10, scoring='accuracy')
scores
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn.ensemble import RandomForestClassifier
# Crea el modelo Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrena el modelo con los datos de entrenamiento
rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy}")

#Validación cruzada
from sklearn.model_selection import cross_val_score
from sklearn import metrics
clf = rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
scores = cross_val_score(
    clf, X, Y, cv=10, scoring='accuracy')
scores
print("%0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
