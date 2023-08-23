import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import serial
import time

font_label = "Calibri Light"
size_screen = "1300x650"
color_blue = "#182c84"
color_yellow = "#f4bc11"
color_gris = "#cacacb"

Red = 0
Black = 0
Silver = 0

rojo=1
negro=1
plata=1
def callback ():

    ret, frame = cap.read()
    global Red, Black ,Silver,rojo,negro,plata


    if ret:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # convertir imágen del espacio BGR a RGB
        hsv_frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape
        
        cx = int(width / 2)
        cy = int(height / 2)
        
        # Pick pixel value
        pixel_center = hsv_frame2[cy, cx]
        hue_value = pixel_center[0]
        dato1 = 0
        dato2 = 0
        dato3 = 0
        dato4 = 0
        dato5 = 0
        dato6 = 0

        print(hue_value)
        color = ""
        if hue_value < 4:
            color = "NEGRO"
            if negro==0:
                Black=Black+1
            negro= 1
            dato1 = 1
        
        elif hue_value < 6:
            dato3 = 0

        elif hue_value < 15:
            dato2= 0
            color = "GRIS"

            if plata==0:
                Silver=Silver+1
            dato3 = 1
            plata= 1
        elif hue_value < 30:
            color = ""

            #if plata==0:
             #   Silver=Silver+1
            #dato3 = 1
            #plata= 1

        elif hue_value < 84:
             dato4 = 1
        elif hue_value < 120:
            color = "GRIS"
            if plata==0:
                Silver=Silver+1
            dato3 = 1
            plata= 1

        elif hue_value < 175:
            dato4 = 1
        else:
            color = "ROJO"
            if rojo==0:
                Red=Red+1   
            dato5 = 1
            rojo=1

        
        datos = "{},{},{},{},{}\n".format(dato1, dato2, dato3, dato4, dato5)
        puerto_serie.write(datos.encode())
        pixel_center_bgr = hsv_frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        cv2.rectangle(hsv_frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
        cv2.putText(hsv_frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
        cv2.circle(hsv_frame, (cx, cy), 5, (25, 25, 25), 3)
        
        

        TotalRed = Label(root, text = Red, font=(font_label, 15))
        TotalRed.grid(row = 3, column = 0)
        TotalRed.place(x=900,y=50)

        TotalBlack = Label(root, text = Black, font=(font_label, 15))
        TotalBlack.grid(row = 5, column = 0)
        TotalBlack.place(x=900,y=150)


        TotalSilver = Label(root, text = Silver, font=(font_label, 15))
        TotalSilver.grid(row = 7, column = 0)
        TotalSilver.place(x=900,y=250)

        img= Image.fromarray(hsv_frame)
        tkimage = ImageTk.PhotoImage(img)
        label.configure (image = tkimage)
        label.image = tkimage
        root.after (1, callback)
        
        
def update_clock():
    
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time,bg=color_yellow)
    clock_label.place(x=1150,y=550)
    clock_label.after(1000, update_clock)
    
def nextFR():
    global rojo
    rojo = 0
    

def nextFN():
    global negro
    negro= 0

def nextFP():
    global plata
    plata= 0


puerto_serie = serial.Serial('COM9', 9600) 
cap= cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
root = tk.Tk()
root.geometry(size_screen)
root.title ("Vision por computadora / Estacion Distribucion")
##root.configure(bg="white")
numImagen = IntVar()
numImagen.set
label=Label (root) 
label.grid (row=1, padx=20, pady=20)

LTotalRed = Label(root, text = 'Total Rojas', bg=color_blue, font=(font_label, 15), fg="white")
LTotalRed.grid(row = 2, column = 0)
LTotalRed.place(x=725,y=50)
LTotalBlack = Label(root, text = 'Total Negras', bg=color_blue, font=(font_label, 15), fg="white")
LTotalBlack.grid(row = 4, column = 0)
LTotalBlack.place(x=725,y=150)
LTotalSilver = Label(root, text = 'Total grises', bg=color_blue, font=(font_label, 15), fg="white")
LTotalSilver.grid(row = 6, column = 0)
LTotalSilver.place(x=725,y=250)
#LTotalPieces = Label(root, text = 'Total processed pieces', bg=color_blue, fg="white")
#LTotalPieces.grid(row = 8, column = 0)
#LTotalPieces.place(x=725,y=150)
################################################################
LTotalRed2 = Label(root, text = 'Piezas Rojas', bg="red", font=(font_label, 15), fg="white")
LTotalRed2.grid(row = 2, column = 1)
LTotalRed2.place(x=950,y=50)
LTotalBlack2 = Label(root, text = 'Piezas Negras', bg="black", font=(font_label, 15), fg="white")
LTotalBlack2.grid(row = 4, column = 1) 
LTotalBlack2.place(x=950,y=150)
LTotalSilver2 = Label(root, text = 'Piezas Grises', bg="gray", font=(font_label, 15), fg="white")
LTotalSilver2.grid(row = 6, column = 1)
LTotalSilver2.place(x=950,y=250)
#LTotalPieces2 = Label(root, text = 'Piezas procesadas', bg=color_blue, fg="white")
#LTotalPieces2.grid(row = 8, column = 1)
#LTotalPieces2.place(x=890,y=400)
###############################################################
buttonSave = Button (root, text ="Ficha Roja", fg="black", bg=color_gris, activebackground="red", borderwidth=5, height="4", width="90", command=nextFR)
buttonSave.grid (row= 2, column = 5, padx=20, pady=20)
buttonSave.place(x=22,y=400)
buttonSave2 = Button (root, text ="Ficha Negra", fg="black", bg=color_gris, activebackground="black", borderwidth=5, height="4", width="90", command=nextFN)
buttonSave2.grid (row= 2, column = 3, padx=20, pady=20)
buttonSave2.place(x=22,y=480)
buttonSave3 = Button (root, text ="Ficha Gris", fg="black", bg=color_gris, activebackground="gray", borderwidth=5, height="4", width="90", command=nextFP)
buttonSave3.grid (row= 2, column = 4, padx=20, pady=20)
buttonSave3.place(x=22,y=560)

# Botones del panel START
on_button = tk.Button(root, text = "START", fg="white", bg=color_blue, activebackground=color_yellow, borderwidth=15, height="1", width="8") 
on_button.grid(row=1, column=2, padx=10, pady=10)
on_button.place(x= 900, y=290)

# Botones del panel STOP
off_button = tk.Button(root, text = "STOP", fg="white", bg="red", activebackground=color_yellow, borderwidth=15, height="1", width="8") 
off_button.grid(row=1, column=2, padx=10, pady=10)
off_button.place(x= 900, y=360)


# Botones del panel RESET
res_button = tk.Button(root, text = "RESET", fg="white", bg="black", activebackground=color_yellow, borderwidth=15, height="1", width="8") 
res_button.grid(row=1, column=2, padx=10, pady=10)
res_button.place(x= 900, y=430)

# Crear etiqueta para mostrar la hora
clock_label = tk.Label(root, font=("Calibri Light", 20))
clock_label.grid(row = 0, column = 3)
# Actualizar la hora cada segundo
update_clock()

root.after (1, callback) 
root.mainloop ()