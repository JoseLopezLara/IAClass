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


directory_to_save_datasets = 'C:/git/IAClass/12_jump_the_ball_pygames/datasets/'
last_csv_path_saved = ''

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
modo_auto = False  # Indica si el modo de juego es automático

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

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

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-20, -8)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

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

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))

# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")

def trace_dataset():

    if(last_csv_path_saved == ''):
        print("Primero debe de guardar el data set.")  
        print("La ruta invalida es: ", last_csv_path_saved)
        return  
    
    df = pd.read_csv(last_csv_path_saved)

    # Verify if the columns don't contain text. If so, convert them to numeric or replace them with NaN
    df['Velocidad Bala'] = pd.to_numeric(df['Velocidad Bala'], errors='coerce')
    df['Desplazamiento Bala'] = pd.to_numeric(df['Desplazamiento Bala'], errors='coerce')
    df['Estatus Salto'] = pd.to_numeric(df['Estatus Salto'], errors='coerce')


    # Replace negative values with his absolute value. Before this, we delete NaN values
    df = df.dropna()
    df['Velocidad Bala'] = df['Velocidad Bala'].abs()
    df['Desplazamiento Bala'] = df['Desplazamiento Bala'].abs()

    # Stadistics of the data
    print("\n------------ DATA EXAMPLE ------------")
    print(df.head())
    print("\n------------ TYPES OF PARAMS ------------")
    print(df.dtypes)
    print("\n------------ STATISTICS ------------")
    print(df.describe())
    print("\n------------ CORRELATIONS ------------")
    print(df.corr())

    # Create 3d chart and and 3d grid. Then, graph the data, additional labels and finally a colorbar
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

    # 2D grafic scatter.
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Desplazamiento Bala'], df['Velocidad Bala'], c=df['Estatus Salto'], cmap='viridis')
    plt.scatter(df['Desplazamiento Bala'], df['Velocidad Bala'], c=df['Estatus Salto'], cmap='viridis')
    plt.xlabel('Desplazamiento Bala')
    plt.ylabel('Velocidad Bala')
    plt.title('Desplazamiento vs Velocidad de la Bala')
    plt.colorbar(label='Estatus Salto')
    plt.show()

def save_data_set(datos_modelo):
    global last_csv_path_saved
    # Generar un nombre de archivo único con la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dataset_{timestamp}.csv"
    
    # Crear la ruta completa del archivo
    file_path = os.path.join(directory_to_save_datasets, filename)
    
    try:
        # Asegurarse de que el directorio existe
        os.makedirs(directory_to_save_datasets, exist_ok=True)
        
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir el encabezado
            writer.writerow(["Velocidad Bala", "Desplazamiento Bala", "Estatus Salto"])
            
            # Escribir los datos
            for dato in datos_modelo:
                writer.writerow(dato)
        
        last_csv_path_saved = file_path 
        print(f"Dataset guardado exitosamente como '{last_csv_path_saved}'")
    except Exception as e:
        print(f"Error al guardar el dataset: {e}")


def print_menu_options():
    lineas = [
        "Presiona 'A' para Auto",
        "'M' para Manual",
        "'G' Para almacenar dataset",
        "'T' Para graficar dataset",
        "",
        "'Q' para Salir"
    ]
    
    # Init position
    x = w // 4
    y = h // 2 - (len(lineas) * 20)  # Ajusta el desplazamiento vertical según el número de líneas
    
    for linea in lineas:
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto, (x, y))
        y += 40  
    pygame.display.flip() 

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    
    print_menu_options()
    
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    modo_auto = True
                    menu_activo = False
                elif evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                elif evento.key == pygame.K_g:
                    save_data_set(datos_modelo)
                    menu_activo = True
                elif evento.key == pygame.K_t:
                    trace_dataset()
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
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
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(30)  # Limitar el juego a 30 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
