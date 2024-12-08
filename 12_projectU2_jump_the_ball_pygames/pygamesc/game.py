import pygame
import random
import csv
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
import math
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import graphviz

directory_to_save_datasets = 'C:/git/IAClass/12_projectU2_jump_the_ball_pygames/datasets/'
directory_to_save_desition_tree = 'C:/git/IAClass/12_projectU2_jump_the_ball_pygames/desition_tree/'
desition_tree_tarined = None
directory_to_save_neural_network = 'C:/git/IAClass/12_projectU2_jump_the_ball_pygames/neural_network/'
neural_network_trained = None


last_csv_path_saved_for_horizontal_ball = ''
last_csv_path_saved_for_vertical_ball = ''
last_csv_path_saved_for_diagonal_ball = ''

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_manual = False
modo_auto = False  
modo_2_balas = False 
modo_3_balas = False 

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []
datos_modelo_vertical_ball = []
datos_modelo_diagonal_ball = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -20  # Velocidad de la bala hacia la izquierda
bala_disparada = False

bala2 = pygame.Rect(random.randint(0, w - 16), 0, 16, 16)
velocidad_bala2 = 5  # Velocidad de la bala hacia abajo
bala2_disparada = False

bala3 = pygame.Rect(w - 16, random.randint(0, h - 16), 16, 16)
velocidad_bala3_x = 0
velocidad_bala3_y = 0
bala3_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w


def generate_desition_treee():
    global last_csv_path_saved_for_horizontal_ball, directory_to_save_desition_tree

    if last_csv_path_saved_for_horizontal_ball == '':
        print('Primero debe de guardar el data set')
        return

    # Asegurarse de que el directorio existe
    os.makedirs(directory_to_save_desition_tree, exist_ok=True)

    # Leer el CSV sin encabezados
    dataset = pd.read_csv(last_csv_path_saved_for_horizontal_ball, header=None)

    # Eliminar la primera fila que contiene encabezados incorrectos
    dataset_cleaned = dataset.iloc[1:].reset_index(drop=True)
    dataset_cleaned = dataset_cleaned.dropna()

    # Guardar el CSV limpio sin índice
    cleaned_csv_path = os.path.join(directory_to_save_desition_tree, 'dataset_cleaned.csv')
    dataset_cleaned.to_csv(cleaned_csv_path, index=False, header=False)
    print(f"CSV limpio guardado en: {cleaned_csv_path}")

    # Definir características (X) y etiquetas (y)
    X = dataset_cleaned.iloc[:, :2]  # Las dos primeras columnas son las características
    y = dataset_cleaned.iloc[:, 2]   # La tercera columna es la etiqueta

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear el clasificador de Árbol de Decisión
    clf = DecisionTreeClassifier()

    # Entrenar el modelo
    clf.fit(X_train, y_train)

    # Exportar el árbol de decisión en formato DOT
    dot_data = export_graphviz(clf, out_file=None, 
                               feature_names=['V. Bala', 'D. Bala'],  
                               class_names=['C. 0 (Suelo)', 'C. 1 (Salto)'],    
                               filled=True, rounded=True,  
                               special_characters=True)  

    # Crear el gráfico con graphviz
    graph = graphviz.Source(dot_data)

    # Guardar el gráfico como PDF y PNG en el directorio especificado
    pdf_path = os.path.join(directory_to_save_desition_tree, 'decision_tree')
    graph.render(pdf_path, format='pdf', cleanup=True)

    print(f"Árbol de decisión guardado como PDF en: {pdf_path}")

    # Opcional: Mostrar el gráfico
    graph.view()

    # # Guardar el modelo entrenado
    # model_path = os.path.join(directory_to_save_desition_tree, 'decision_tree_model')
    # joblib.dump(clf, model_path)
    # print(f"Modelo de árbol de decisión guardado en: {model_path}")

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-10, -4)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para disparar la segunda bala
def disparar_bala2():
    global bala2_disparada, bala2, velocidad_bala2
    if not bala2_disparada:
        bala2.x = random.randint(0, w - 16)
        bala2.y = 0
        velocidad_bala2 = random.randint(3, 7)  # Velocidad aleatoria hacia abajo
        bala2_disparada = True

# Función para reiniciar la posición de la segunda bala
def reset_bala2():
    global bala2, bala2_disparada
    bala2.x = random.randint(0, w - 16)
    bala2.y = 0
    bala2_disparada = False

# Función para disparar la tercera bala
def disparar_bala3():
    global bala3_disparada, bala3, velocidad_bala3_x, velocidad_bala3_y
    if not bala3_disparada:
        bala3.y = random.randint(0, h - 16)
        bala3.x = w - 16
        
        # angule and Speed X Y 
        angle = math.radians(180 - 25)
        
        speed = random.randint(5, 10)
        velocidad_bala3_x = speed * math.cos(angle)
        velocidad_bala3_y = speed * math.sin(angle)
        bala3_disparada = True

# Función para reiniciar la posición de la tercera bala
def reset_bala3():
    global bala3, bala3_disparada
    bala3.y = random.randint(0, h - 16)
    bala3.x = w - 16
    bala3_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

    # Mover y dibujar la segunda bala si está en modo 2 o 3 balas
    if modo_2_balas or modo_3_balas:
        if bala2_disparada:
            bala2.y += velocidad_bala2
        else:
            disparar_bala2()

        # Si la bala2 sale de la pantalla, reiniciar su posición
        if bala2.y > h:
            reset_bala2()

        pantalla.blit(bala_img, (bala2.x, bala2.y))

        # Colisión entre la bala2 y el jugador
        if jugador.colliderect(bala2):
            print("Colisión con bala 2 detectada!")
            reiniciar_juego()

    # Mover y dibujar la tercera bala si está en modo 3 balas
    if modo_3_balas:
        if bala3_disparada:
            bala3.x += velocidad_bala3_x
            bala3.y += velocidad_bala3_y
        else:
            disparar_bala3()

        # Si la bala3 sale de la pantalla, reiniciar su posición
        if bala3.x < 0 or bala3.y < 0 or bala3.y > h:
            reset_bala3()

        pantalla.blit(bala_img, (bala3.x, bala3.y))

        # Colisión entre la bala3 y el jugador
        if jugador.colliderect(bala3):
            print("Colisión con bala 3 detectada!")
            reiniciar_juego()

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, salto
    global bala, velocidad_bala
    global bala2, velocidad_bala2
    global bala3, velocidad_bala3_x, velocidad_bala3_y
    
    global modo_manual, modo_2_balas, modo_3_balas
    
    if modo_manual:
        distancia = abs(jugador.x - bala.x)
        salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
        # Guardar velocidad de la bala, distancia al jugador y si saltó o no
        datos_modelo.append((velocidad_bala, distancia, salto_hecho))
    
    if modo_2_balas:
        distancia = abs(jugador.x - bala.x)
        salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
        # Guardar velocidad de la bala, distancia al jugador y si saltó o no
        datos_modelo.append((velocidad_bala, distancia, salto_hecho))
        
        distanciaY = abs(jugador.y - bala2.y)
        datos_modelo_vertical_ball.append((velocidad_bala2, distanciaY))
    
    if modo_3_balas:    
        distancia = abs(jugador.x - bala.x)
        salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
        # Guardar velocidad de la bala, distancia al jugador y si saltó o no
        datos_modelo.append((velocidad_bala, distancia, salto_hecho))
        
        distanciaY = abs(jugador.y - bala2.y)
        datos_modelo_vertical_ball.append((velocidad_bala2, distanciaY))
        
        # Calcular la distancia hipotenusa entre el jugador y la bala3
        distancia_x_bala3 = jugador.x - bala3.x
        distancia_y_bala3 = jugador.y - bala3.y
        distancia_hipotenusa = math.sqrt(distancia_x_bala3**2 + distancia_y_bala3**2)
        datos_modelo_diagonal_ball.append((velocidad_bala3_x, velocidad_bala3_y, distancia_hipotenusa))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

def trace_dataset():
    if(last_csv_path_saved_for_horizontal_ball == ''):
        print("Primero debe de guardar el data set.")  
        print("La ruta inválida es: ", last_csv_path_saved_for_horizontal_ball)
        return  

    df = pd.read_csv(last_csv_path_saved_for_horizontal_ball)

    # Verificar si las columnas no contienen texto. Si es así, convertirlas a numéricas o reemplazarlas con NaN
    df['Velocidad Bala'] = pd.to_numeric(df['Velocidad Bala'], errors='coerce')
    df['Desplazamiento Bala'] = pd.to_numeric(df['Desplazamiento Bala'], errors='coerce')
    df['Estatus Salto'] = pd.to_numeric(df['Estatus Salto'], errors='coerce')

    # Reemplazar valores negativos con su valor absoluto. Antes de esto, eliminamos valores NaN
    df = df.dropna()
    df['Velocidad Bala'] = df['Velocidad Bala'].abs()
    df['Desplazamiento Bala'] = df['Desplazamiento Bala'].abs()

    # Estadísticas de los datos
    print("\n------------ DATA EXAMPLE ------------")
    print(df.head())
    print("\n------------ TYPES OF PARAMS ------------")
    print(df.dtypes)
    print("\n------------ STATISTICS ------------")
    print(df.describe())
    print("\n------------ CORRELATIONS ------------")
    print(df.corr())

    # Crear gráfico 3D y una cuadrícula 3D. Luego, graficar los datos, etiquetas adicionales y finalmente una barra de color
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(df['Desplazamiento Bala'], 
                        df['Velocidad Bala'], 
                        df['Estatus Salto'],
                        c=df['Estatus Salto'], 
                        cmap='viridis')

    ax.set_xlabel('Desplazamiento Bala')
    ax.set_ylabel('Velocidad Bala')
    ax.set_zlabel('Estatus del Salto')
    ax.set_title('Análisis 3D de Datos del Juego')

    plt.colorbar(scatter, label='Estatus Salto')
    plt.show()

    # Gráfico de dispersión 2D.
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Desplazamiento Bala'], df['Velocidad Bala'], c=df['Estatus Salto'], cmap='viridis')
    plt.xlabel('Desplazamiento Bala')
    plt.ylabel('Velocidad Bala')
    plt.title('Desplazamiento vs Velocidad de la Bala')
    plt.colorbar(label='Estatus Salto')
    plt.show()

def save_data_set():
    global last_csv_path_saved_for_horizontal_ball, last_csv_path_saved_for_vertical_ball, last_csv_path_saved_for_diagonal_ball
    
    if modo_manual:
        # Generar un nombre de archivo único con la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_horizontal_ball = f"dataset_horizontal_ball_{timestamp}.csv"
        
        # Crear la ruta completa del archivo
        file_path_horizontal_ball = os.path.join(directory_to_save_datasets, filename_horizontal_ball)
        
        try:
            # Asegurarse de que el directorio existe
            os.makedirs(directory_to_save_datasets, exist_ok=True)
            
            with open(file_path_horizontal_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala", "Desplazamiento Bala", "Estatus Salto"])
                
                # Escribir los datos
                for dato in datos_modelo:
                    writer.writerow(dato)
            
            last_csv_path_saved_for_horizontal_ball = file_path_horizontal_ball 
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_horizontal_ball}'")
        except Exception as e:
            print(f"Error al guardar el dataset: {e}")
            
    if modo_2_balas:
        # Generar un nombre de archivo único con la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_horizontal_ball = f"dataset_horizontal_ball_{timestamp}.csv"
        filename_vertical_ball = f"dataset_vertical_ball_{timestamp}.csv"
        
        # Crear la ruta completa del archivo
        file_path_horizontal_ball = os.path.join(directory_to_save_datasets, filename_horizontal_ball)
        file_path_vertical_ball = os.path.join(directory_to_save_datasets, filename_vertical_ball)
        
        try:
            # Asegurarse de que el directorio existe
            os.makedirs(directory_to_save_datasets, exist_ok=True)
            
            with open(file_path_horizontal_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala", "Desplazamiento Bala", "Estatus Salto"])
                
                # Escribir los datos
                for dato in datos_modelo:
                    writer.writerow(dato)
            
            with open(file_path_vertical_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala", "Desplazamiento Bala Y", ""])
                
                # Escribir los datos
                for dato in datos_modelo_vertical_ball:
                    writer.writerow(dato)
            
            last_csv_path_saved_for_horizontal_ball = file_path_horizontal_ball 
            last_csv_path_saved_for_vertical_ball = file_path_vertical_ball 
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_horizontal_ball}'")
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_vertical_ball}'")
        except Exception as e:
            print(f"Error al guardar el dataset: {e}")
    
    if modo_3_balas:
        # Generar un nombre de archivo único con la fecha y hora actual
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_horizontal_ball = f"dataset_horizontal_ball_{timestamp}.csv"
        filename_vertical_ball = f"dataset_vertical_ball_{timestamp}.csv"
        filename_diagonal_ball = f"dataset_diagonal_ball_{timestamp}.csv"
        
        # Crear la ruta completa del archivo
        file_path_horizontal_ball = os.path.join(directory_to_save_datasets, filename_horizontal_ball)
        file_path_vertical_ball = os.path.join(directory_to_save_datasets, filename_vertical_ball)
        file_path_diagonal_ball = os.path.join(directory_to_save_datasets, filename_diagonal_ball)
        
        try:
            # Asegurarse de que el directorio existe
            os.makedirs(directory_to_save_datasets, exist_ok=True)
            
            with open(file_path_horizontal_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala", "Desplazamiento Bala", "Estatus Salto"])
                
                # Escribir los datos
                for dato in datos_modelo:
                    writer.writerow(dato)
            
            with open(file_path_vertical_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala", "Desplazamiento Bala Y", ""])
                
                # Escribir los datos
                for dato in datos_modelo_vertical_ball:
                    writer.writerow(dato)
                    
            with open(file_path_diagonal_ball, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado
                writer.writerow(["Velocidad Bala X", "Velocidad Bala Y", "Desplazamiento Hipotenusa"])
                
                # Escribir los datos
                for dato in datos_modelo_diagonal_ball:
                    writer.writerow(dato)
            
            last_csv_path_saved_for_horizontal_ball = file_path_horizontal_ball 
            last_csv_path_saved_for_vertical_ball = file_path_vertical_ball 
            last_csv_path_saved_for_diagonal_ball = file_path_diagonal_ball 
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_horizontal_ball}'")
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_vertical_ball}'")
            print(f"Dataset guardado exitosamente como '{last_csv_path_saved_for_diagonal_ball}'")
        except Exception as e:
            print(f"Error al guardar el dataset: {e}")

def print_menu_options():
    lineas = [
        "'D' para Auto con Desition Tree",
        "'M' para Manual",
        "'F' para entrenar modelos",
        "'G' Para almacenar dataset",
        "'T' Para graficar dataset",
        "Presiona '2' para modo 2 balas",
        "Presiona '3' para modo 3 balas",
        "",
        "'Q' para Salir"
    ]
    
    # Posición inicial
    x = w // 4
    y = h // 2 - (len(lineas) * 20)  # Ajusta el desplazamiento vertical según el número de líneas
    
    for linea in lineas:
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto, (x, y))
        y += 40  
    pygame.display.flip() 

def train_models():
    generate_desition_treee()

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto, modo_manual, modo_2_balas, modo_3_balas
    pantalla.fill(NEGRO)
    
    print_menu_options()
    
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_d:
                    modo_auto = True
                    modo_manual = False
                    modo_2_balas = False
                    modo_3_balas = False
                    menu_activo = False
                    print('- - - - Option auto selected - - - -')
                    # generate_desition_treee()
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    modo_manual = True
                    modo_2_balas = False
                    modo_3_balas = False
                    menu_activo = False
                elif evento.key == pygame.K_f:
                    train_models()
                    menu_activo = True
                elif evento.key == pygame.K_g:
                    save_data_set()
                    menu_activo = True
                elif evento.key == pygame.K_t:
                    trace_dataset()
                elif evento.key == pygame.K_2:
                    modo_auto = False
                    modo_manual = False
                    modo_2_balas = True
                    modo_3_balas = False
                    menu_activo = False
                elif evento.key == pygame.K_3:
                    modo_auto = False
                    modo_manual = False
                    modo_2_balas = False
                    modo_3_balas = True
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, bala2_disparada, bala3_disparada
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Reiniciar la segunda bala
    bala2.x = random.randint(0, w - 16)
    bala2.y = 0
    bala2_disparada = False
    # Reiniciar la tercera bala
    bala3.x = w - 16
    bala3.y = random.randint(0, h - 16)
    bala3_disparada = False
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo

def main():
    global salto, en_suelo, bala_disparada

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    print('saltando...')
                    salto = True
                    en_suelo = False
                
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    # print("Juego terminado. Datos recopilados:", datos_modelo)
                    print("Juego terminado.")
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            # Move right or left
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                jugador.x -= 5  
            if keys[pygame.K_RIGHT]:
                jugador.x += 5  

            # Mantener al jugador dentro de los límites de la pantalla
            if jugador.x < 0:
                jugador.x = 0
            if jugador.x > w - jugador.width:
                jugador.x = w - jugador.width

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
