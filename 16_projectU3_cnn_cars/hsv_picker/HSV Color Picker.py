
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from sklearn.cluster import KMeans
import os

image_hsv = None
drawing = False
ix, iy = -1, -1
painted_pixels = []
zoom_factor = 2
zoom_size = 200

ftypes = [
    ("All files", "*.*")
]
images_folder = "images"

def draw(event, x, y, flags, param):
    global ix, iy, drawing, image, image_hsv, painted_pixels, zoom_factor

    if event == cv2.EVENT_MOUSEMOVE:
        show_zoom(x, y)
        if drawing:
            cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
            painted_pixels.extend(image_hsv[y-3:y+4, x-3:x+4].reshape(-1, 3))

    elif event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
        painted_pixels.extend(image_hsv[y-3:y+4, x-3:x+4].reshape(-1, 3))

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            zoom_factor = min(zoom_factor + 0.2, 5)
        else:
            zoom_factor = max(zoom_factor - 0.2, 1)
        show_zoom(x, y)

def show_zoom(x, y):
    global image, zoom_factor, zoom_size
    
    half_size = int(zoom_size / (2 * zoom_factor))
    y1, y2 = max(y - half_size, 0), min(y + half_size, image.shape[0])
    x1, x2 = max(x - half_size, 0), min(x + half_size, image.shape[1])

    zoomed = image[y1:y2, x1:x2]
    zoomed = cv2.resize(zoomed, (zoom_size, zoom_size), interpolation=cv2.INTER_LINEAR)

    cv2.circle(zoomed, (zoom_size//2, zoom_size//2), 3, (0, 0, 255), -1)

    cv2.imshow("Zoom", zoomed)

def get_hsv_ranges():
    global painted_pixels, image_hsv
    if not painted_pixels:
        print("No se ha pintado ningún área.")
        return

    painted_pixels = np.array(painted_pixels)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(painted_pixels)

    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_indices = np.argsort(counts)[::-1]
    
    print("sorted_indices: " + str(sorted_indices))
    
    for i, idx in enumerate(sorted_indices):
        cluster = painted_pixels[kmeans.labels_ == idx]
        
        h_min, s_min, v_min = np.min(cluster, axis=0)
        h_max, s_max, v_max = np.max(cluster, axis=0)

        print(f"Grupo de color {i+1}:")
        print(f"  Rango HSV mínimo: [{h_min}, {s_min}, {v_min}]")
        print(f"  Rango HSV máximo: [{h_max}, {s_max}, {v_max}]")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow(f"Mask {i+1}", mask)

def get_hsv_ranges_full_image():
    global image_hsv
    
    pixels = image_hsv.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(pixels)

    unique, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_indices = np.argsort(counts)[::-1]
    
    print("Rangos HSV para toda la imagen:")
    
    for i, idx in enumerate(sorted_indices):
        cluster = pixels[kmeans.labels_ == idx]
        
        h_min, s_min, v_min = np.min(cluster, axis=0)
        h_max, s_max, v_max = np.max(cluster, axis=0)

        print(f"Grupo de color {i+1}:")
        print(f"  Rango HSV mínimo: [{h_min}, {s_min}, {v_min}]")
        print(f"  Rango HSV máximo: [{h_max}, {s_max}, {v_max}]")

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow(f"Full Image Mask {i+1}", mask)

def set_up_image_root_path(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, path)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    return image_dir

def open_file_dialog(image_dir):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        initialdir=image_dir,
        filetypes=ftypes
    )
    root.update()

    if not file_path:
        print("No se seleccionó ninguna imagen.")
        return None

    print(f"Intentando abrir la imagen: {file_path}")
    return file_path
    
def main():
    global image, image_hsv, painted_pixels

    image_dir = set_up_image_root_path(images_folder)
    file_path = open_file_dialog(image_dir)
    if file_path is None or not os.path.exists(file_path):
        print(f"El archivo no existe o no se seleccionó: {file_path}")
        return

    image = cv2.imread(file_path)
    if image is None:
        print(f"No se pudo leer la imagen: {file_path}")
        return
    print(f"Imagen cargada exitosamente. Tamaño: {image.shape}")

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", draw)

    while True:
        cv2.imshow("image", image)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('r'):
            get_hsv_ranges()
        elif k == ord('a'):
            get_hsv_ranges_full_image()
        elif k == ord('c'):
            image = cv2.imread(file_path)
            painted_pixels = []

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()