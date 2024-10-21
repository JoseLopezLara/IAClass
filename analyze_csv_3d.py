import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ruta del archivo CSV (ajusta esta ruta según la ubicación de tu archivo)
csv_path = 'C:/ruta/a/tu/archivo.csv'

# Cargar el CSV
df = pd.read_csv(csv_path, header=None, names=['Desplazamiento_Bala', 'Velocidad_Bala', 'Estatus_Salto'])

# Separar los datos en columnas
df[['Desplazamiento_Bala', 'Velocidad_Bala']] = df['Desplazamiento_Bala'].str.split('-', expand=True).astype(int)
df['Estatus_Salto'] = df['Velocidad_Bala'].str[-1].astype(int)
df['Velocidad_Bala'] = df['Velocidad_Bala'].str[:-1].astype(int)

# Crear la figura y el eje 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar los puntos
scatter = ax.scatter(df['Desplazamiento_Bala'], 
                     df['Velocidad_Bala'], 
                     df['Estatus_Salto'],
                     c=df['Estatus_Salto'],  # Color basado en Estatus_Salto
                     cmap='viridis')

# Configurar etiquetas y título
ax.set_xlabel('Desplazamiento Bala')
ax.set_ylabel('Velocidad Bala')
ax.set_zlabel('Estatus Salto')
ax.set_title('Análisis 3D de Datos del Juego')

# Añadir una barra de color
plt.colorbar(scatter, label='Estatus Salto')

# Mostrar el gráfico
plt.show()

# Crear un gráfico de dispersión 2D adicional
plt.figure(figsize=(10, 6))
plt.scatter(df['Desplazamiento_Bala'], df['Velocidad_Bala'], c=df['Estatus_Salto'], cmap='viridis')
plt.xlabel('Desplazamiento Bala')
plt.ylabel('Velocidad Bala')
plt.title('Desplazamiento vs Velocidad de la Bala')
plt.colorbar(label='Estatus Salto')
plt.show()

# Imprimir estadísticas básicas
print(df.describe())

# Imprimir correlaciones
print("\nCorrelaciones:")
print(df.corr())