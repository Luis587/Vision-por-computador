import cv2
import numpy as np
import tkinter as tk
from tkinter import Label
from PIL import ImageTk, Image
import time
import serial


size_screen = "1300x650"
color_blue = "#182c84"
color_yellow = "#f4bc11"
color_gris = "#cacacb"
font_label = "Calibri Light"

# Definir los rangos de colores en HSV
lower_red = np.array([0, 110, 50])
upper_red = np.array([10, 150, 150])
lower_red2 = np.array([170, 100, 70])
upper_red2 = np.array([180, 255, 255])
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 30])
lower_black2 = np.array([0, 0, 0])
upper_black2 = np.array([180, 255, 50])
lower_silver = np.array([0, 0, 150])
upper_silver = np.array([180, 50, 255])

# Contadores de colores
color_counters = {
    "Rojo": 0,
    "Negro": 0,
    "Plata": 0
}

# Variables para el conteo de colores
color_detected = False
color_detection_start_time = None
previous_color = None

# Tiempo de detección necesario para contar el color (en segundos)
color_detection_time = 1.5


# Función para actualizar los contadores de colores en la interfaz
def update_color_counters(color_name):
    if color_name in color_counters:
        color_counters[color_name] += 1
        color_counter_labels[color_name].config(text=f"{color_name}: {color_counters[color_name]}", font=("Calibri Light", 14))

# Función para detectar y mostrar el nombre del color predominante
def detect_color_name(frame, mask, color_name, x, y):
    global color_detected, color_detection_start_time, previous_color

    # Encontrar los contornos de los objetos detectados
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    color_detected_now = False

    for contour in contours:
        # Obtener el centro del contorno si el área es mayor que cero
        area = cv2.contourArea(contour)
        if area > 0:
            M = cv2.moments(contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Verificar si el centro del contorno está dentro del área de detección
            if x <= cx <= x + color_zone_size and y <= cy <= y + color_zone_size:
                # Calcular el porcentaje de área ocupada por el contorno
                area_ratio = area / (color_zone_size * color_zone_size)

                if area_ratio >= 0.40:  # Si el área ocupa al menos el 95% del cuadro de detección
                    color_detected_now = True
                    break

    # Mostrar el nombre del color predominante dentro del recuadro de detección
    if color_detected_now:
        cv2.putText(frame, color_name, (x + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if not color_detected:
            # Si no se ha detectado un color previamente, iniciar el temporizador
            color_detection_start_time = time.time()
            color_detected = True
    else:
        # Reiniciar el temporizador y el estado de detección si el color no está presente
        if color_detected:
            elapsed_time = time.time() - color_detection_start_time
            if elapsed_time >= color_detection_time:
                update_color_counters(previous_color)
            color_detected = False
            previous_color = None

    # Verificar si hay un cambio en el objeto detectado
    if previous_color != color_name:
        if previous_color is not None and color_detected:
            elapsed_time = time.time() - color_detection_start_time
            if elapsed_time >= color_detection_time:
                update_color_counters(previous_color)
                color_detected = False
                previous_color = None
        previous_color = color_name

# Función para seleccionar el color
def select_color():
    global selected_color
    selected_color = color_selector.get()
    print("Color seleccionado:", selected_color)

# Función para resetear los contadores de colores
def reset_color_counters():
    for color_name in color_counters:
        color_counters[color_name] = 0
        color_counter_labels[color_name].config(text=f"{color_name}: {color_counters[color_name]}", font=("Calibri Light", 14))

# Función para iniciar la cámara
def start_camera():
    global video_capture, camera_active
    camera_active = True
    video_capture = cv2.VideoCapture(0)
    show_frame()

# Función para detener la cámara
def stop_camera():
    global video_capture, camera_active
    camera_active = False
    video_capture.release()
    cv2.destroyAllWindows()
    clear_canvas()

# Función para mostrar los frames de la cámara en el lienzo de tkinter
def show_frame():
    if not camera_active:
        return

    _, frame = video_capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Aplicar las máscaras para detectar los colores
    if selected_color == "Rojo":
        mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask, mask2)
    elif selected_color == "Negro":
        mask = cv2.inRange(hsv_frame, lower_black, upper_black)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask, mask2)
    elif selected_color == "Plata":
        mask = cv2.inRange(hsv_frame, lower_silver, upper_silver)
    else:
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)

    # Filtrar la máscara para mejorar la precisión
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Detectar y mostrar el nombre del color predominante
    detect_color_name(frame, mask, selected_color, color_zone_x, color_zone_y)

    # Dibujar el recuadro de detección
    cv2.rectangle(frame, (color_zone_x, color_zone_y), (color_zone_x + color_zone_size, color_zone_y + color_zone_size), (0, 255, 0), 2)

    # Mostrar el frame con los nombres de los colores
    image = Image.fromarray(frame)
    image_tk = ImageTk.PhotoImage(image)
    canvas.create_image(canvas_width / 2, canvas_height / 2, anchor=tk.CENTER, image=image_tk)
    canvas.image = image_tk

    # Llamar a la función show_frame después de 15 milisegundos (aproximadamente 66 fps)
    window.after(15, show_frame)

# Función para limpiar el lienzo de tkinter
def clear_canvas():
    canvas.delete("all")

# Crear la ventana de tkinter
window = tk.Tk()
window.geometry("1500x700")
im_fondo = Image.open("C:/Users/Luis Alvarado/OneDrive/Escritorio/PROYECTO SCADA/bg2.jpg")
im_fondo = im_fondo.resize((800, 800), Image.ANTIALIAS)
im_fondo = ImageTk.PhotoImage(im_fondo)
label_fondo = Label(window, image=im_fondo)
label_fondo.place(x=460, y=0, relwidth=1, relheight=1)
window.title("Vision por Computadora / Estacion Distribucion")

# Crear el selector de color
color_selector = tk.StringVar(window)
color_selector.set("Ninguno")  # Valor predeterminado
color_option_menu = tk.OptionMenu(window, color_selector, "Ninguno", "Rojo", "Negro", "Plata")
color_option_menu.grid(row=0, column=0, padx=10, pady=10)
color_option_menu.place(x=1250,y=20)

# Crear el botón para seleccionar el color
select_button = tk.Button(window, text="Seleccionar", fg="white", bg=color_blue, activebackground=color_yellow, borderwidth=5, height="1", width="8", command=select_color)
select_button.grid(row=0, column=1, padx=10, pady=10)
select_button.place(x=1400, y=20)

# Crear el botón para resetear los contadores
reset_button = tk.Button(window, text="Resetear Contadores", fg="white", bg=color_blue, font=(font_label, 15), activebackground=color_yellow, borderwidth=10, height="2", width="60", command=reset_color_counters)
reset_button.grid(row=0, column=2, padx=10, pady=10)
reset_button.place(x=100, y = 700)

# Crear el botón para iniciar la cámara
start_button = tk.Button(window, text="Camera ON", command=start_camera, fg="white", bg="green", activebackground=color_yellow, borderwidth=10, height="1", width="15")
start_button.grid(row=1, column=0, padx=10, pady=10)
start_button.place(x=830, y = 20)

# Crear el botón para detener la cámara
stop_button = tk.Button(window, text="Camera OFF", command=stop_camera, fg="white", bg="red", activebackground=color_yellow, borderwidth=10, height="1", width="15")
stop_button.grid(row=1, column=1, padx=10, pady=10)
stop_button.place(x=830,y=70)

# Botones del panel START
on_button = tk.Button(window, text = "START", fg="white", bg=color_blue, activebackground=color_yellow, borderwidth=15, height="1", width="8") 
on_button.grid(row=1, column=2, padx=10, pady=10)
on_button.place(x= 1130, y=290)

# Botones del panel STOP
off_button = tk.Button(window, text = "STOP", fg="white", bg="red", activebackground=color_yellow, borderwidth=15, height="1", width="8") 
off_button.grid(row=1, column=2, padx=10, pady=10)
off_button.place(x= 1120, y=360)

# Botones del panel RESET
res_button = tk.Button(window, text = "RESET", fg="white", bg="black", activebackground=color_yellow, borderwidth=15, height="1", width="8") 
res_button.grid(row=1, column=2, padx=10, pady=10)
res_button.place(x= 1110, y=430)

# Crear el lienzo para mostrar el video
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# Dimensiones y posición del recuadro de detección
color_zone_size = 50
color_zone_x = int((canvas_width - color_zone_size) / 2)
color_zone_y = int((canvas_height - color_zone_size) / 2)

# Variable para indicar si la cámara está activa o no
camera_active = False

# Variable para almacenar el color seleccionado
selected_color = "Ninguno"

# Crear etiquetas para los contadores de colores
color_counter_labels = {}
for i, color_name in enumerate(color_counters):
    color_counter_labels[color_name] = tk.Label(window, text=f"{color_name}: {color_counters[color_name]}", font=("Calibri Light", 14, "bold"))
    color_counter_labels[color_name].grid(row=3, column=i, padx=10, pady=10)

# Ejecutar la ventana de tkinter
window.mainloop()