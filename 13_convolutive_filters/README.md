<p style="text-align: right;"><em>DATE: JANUARY - JUNE 2024</em></p>

# **PROJECT UNIT NUMBER ONE**

## **Shortest route to make**

### Made In: Python

#### Activity number: 13

#### **DESCRIPTION:**

#### For this activity we have to analize desitions tree using the diferents datasets created in exercise number 09

________________________________________________________
________________________________________________________

#### Student: José López Lara

#### Control Number: 19120194

* [x] Student Email: <l19120194@morelia.tecnm.mx>
* [x] Personal Email: <jose.lopez.lara.cto@gmail.com>
* [x] GitHub Profile: [JoseLopezLara](https://github.com/JoseLopezLara)
* [x] Linkedin Profile: [in/jose-lopez-lara/](https://www.linkedin.com/in/jose-lopez-lara/)

________________________________________________________
________________________________________________________

### **STEP ONE: Generate multiple destions tree using below datasets**

#### I have played in 5 time in differents modes

1. Dataset1: Play and I lost iinmediatly
2. Dataset2: Inrregular game (Double jumps) and I  lost in 5 seconds.
3. Dataset3: Regular game and I lost in 25 seconds.
4. Dataset4: Inrregular game (Double jumps) and I lost in 25 seconds.
5. Dataset5: Regular game and I lost in 50 seconds.

### **Code used**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

# Cargar el dataset

# csv_file_name = 'DATASET1-ME-DEJO-PERDER-AL-INICIO'
# csv_file_name = 'DATASET2-JUEGO-IRREGULAR-5SEG'
# csv_file_name = 'DATASET3-JUEGO-REGULAR-25SEG'
csv_file_name = 'DATASET4-JUEGO-IRREGULAR-SALTOS-DOBLES-25SEG'
# csv_file_name = 'DATASET5-JUGO-REGULAR-50SEG'

file_path = 'C:/git/IAClass/10_graph_desition_tree/datasets/' + csv_file_name + '.csv'

dataset = pd.read_csv(file_path)

# Eliminar columnas innecesarias (como la vacía "Unnamed: 3")
#dataset = dataset.drop(columns=['Unnamed: 3'])

# Definir características (X) y etiquetas (y)
X = dataset.iloc[:, :2]  # Las dos primeras columnas son las características
y = dataset.iloc[:, 2]   # La tercera columna es la etiqueta

# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el clasificador de Árbol de Decisión | ESTA CLASE GENERA UN ARBOL DE DESICIÓN PARA PODER ENTENAR EL MODELO
clf = DecisionTreeClassifier()

# Entrenar el modelo | FIT ES LO QUE SE UTILIZA PARA GENERAR EL ENTRENAMIENTO
clf.fit(X_train, y_train)

# Exportar el árbol de decisión en formato DOT para su visualización
# Parámetros de export_graphviz():
# - clf: El clasificador de árbol de decisión entrenado.
# - out_file=None: Indica que el resultado se devuelve como una cadena en lugar de escribirse en un archivo.
# - feature_names=['Feature 1', 'Feature 2']: Nombra las características. En tu caso, corresponden a 'Desplazamiento Bala' y 'Velocidad Bala'.
# - class_names=['Clase 0', 'Clase 1']: Nombra las clases. Aquí, 'Clase 0' probablemente significa "no saltar" y 'Clase 1' "saltar".
# - filled=True: Colorea los nodos según la clase mayoritaria.
# - rounded=True: Hace que los nodos tengan esquinas redondeadas.
# - special_characters=True: Permite el uso de caracteres especiales en las etiquetas de los nodos.
dot_data = export_graphviz(clf, out_file=None, 
                           feature_names=['D. Bala', 'V. Bala'],  
                           class_names=['C. 0 (Suelo)', 'C. 1 (Salto)'],    
                           filled=True, rounded=True,  
                           special_characters=True)  

# Crear el gráfico con graphviz
graph = graphviz.Source(dot_data)

# Mostrar el gráfico
graph.render("decision_tree")  # Esto guarda el gráfico como 'decision_tree.pdf' en el directorio de trabajo
# Mostrar el gráfico
graph.view()

```

### Interpretation

Any node represents the  decision of the tree. It is checking if the bullet is more than X units (Distance or velocity)  from the player. If it is, it slightly favors the decision not to jump (Class 0) or jump (Clas 1).

**For dataset: DATASET1-ME-DEJO-PERDER-AL-INICIO**
![image](image1.png)

**For dataset: DATASET2-JUEGO-IRREGULAR-5SEG**
![image](image2.png)

**For dataset: DATASET3-JUEGO-REGULAR-25SEG**
![image](image3.png)

**For dataset: DATASET4-JUEGO-IRREGULAR-SALTOS-DOBLES-25SEG**
![image](image4.png)

**For dataset: DATASET5-JUGO-REGULAR-50SEG**
![image](image5.png)
