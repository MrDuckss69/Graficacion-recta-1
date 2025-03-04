import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para inicializar la gráfica vacía
def inicializar_grafica():
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    global fig, ax
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Gráfica del Método DDA")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_xlim(-999, 999)
    ax.set_ylim(-999, 999)
    ax.set_aspect('equal', 'box')

    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')

    # Conectar el evento de movimiento del mouse con la función de mostrar coordenadas
    canvas.mpl_connect('motion_notify_event', on_move)

# Función que se ejecuta cuando el mouse se mueve sobre la gráfica
def on_move(event):
    if event.inaxes != ax:  # Si el mouse no está dentro de los ejes de la gráfica
        return

    # Obtener las coordenadas del mouse en el gráfico
    x, y = event.xdata, event.ydata
    
    if x is not None and y is not None:  # Si las coordenadas son válidas
        # Actualizar la etiqueta con las coordenadas del punto
        label_coordenadas.config(text=f"Coordenadas: X = {x:.2f}, Y = {y:.2f}")

# Función para calcular la pendiente y graficar usando el método DDA
def calcular_y_graficar():
    try:
        xa = float(entry_xa.get())
        ya = float(entry_ya.get())
        xb = float(entry_xb.get())
        yb = float(entry_yb.get())

        dx = xb - xa
        dy = yb - ya

        # Calcular la pendiente
        pendiente = 'Infinita (línea vertical)' if dx == 0 else f"{(dy / dx):.2f}"
        label_resultado.config(text=f"Pendiente (m): {pendiente}")

        pasos = int(max(abs(dx), abs(dy)))
        x_incremento = dx / pasos
        y_incremento = dy / pasos

        x = xa
        y = ya

        # Listas para la tabla DDA
        pasos_lista, x_lista, y_lista = [], [], []

        for i in range(pasos + 1):
            pasos_lista.append(i)
            x_lista.append(round(x, 2))
            y_lista.append(round(y, 2))
            x += x_incremento
            y += y_incremento

        # Dibujar la línea DDA en la gráfica existente
        ax.plot(x_lista, y_lista, marker='o', color='blue', label='Línea DDA')
        ax.legend()

        # Hacer zoom en la parte de la recta
        min_x, max_x = min(x_lista), max(x_lista)
        min_y, max_y = min(y_lista), max(y_lista)
        margen = 100  # Margen adicional para el zoom
        ax.set_xlim(min_x - margen, max_x + margen)
        ax.set_ylim(min_y - margen, max_y + margen)

        # Redibujar la gráfica
        canvas.draw()

        # Mostrar la tabla DDA en la interfaz Tkinter
        mostrar_tabla_dda(pasos_lista, x_lista, y_lista)

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para mostrar la tabla DDA
def mostrar_tabla_dda(pasos_lista, x_lista, y_lista):
    # Limpiar el frame de la tabla
    for widget in frame_tabla.winfo_children():
        widget.destroy()

    # Crear un widget Text para mostrar la tabla
    tabla_texto = tk.Text(frame_tabla, height=30, width=20, font=("Arial", 14))
    tabla_texto.insert(tk.END, f"{'Paso':<6}{'X':<10}{'Y':<10}\n")
    tabla_texto.insert(tk.END, f"{'-'*26}\n")
    for paso, x_val, y_val in zip(pasos_lista, x_lista, y_lista):
        tabla_texto.insert(tk.END, f"{paso:<6}{x_val:<10}{y_val:<10}\n")
    tabla_texto.config(state='disabled')
    tabla_texto.pack()

# Función para limpiar la gráfica
def limpiar_grafica():
    # Limpiar la gráfica actual
    ax.cla()  # Limpiar los ejes de la gráfica
    ax.set_title("Gráfica del Método DDA")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_xlim(-999, 999)  # Límites para el eje X de -999 a 999
    ax.set_ylim(-999, 999)  # Límites para el eje Y de -999 a 999
    ax.set_aspect('equal', 'box')

    # Redibujar la gráfica vacía
    canvas.draw()

# Función para hacer zoom manual
def zoom_manual():
    try:
        # Obtener los valores de los campos de entrada para el zoom manual
        lim_x_min = float(entry_lim_x_min.get())
        lim_x_max = float(entry_lim_x_max.get())
        lim_y_min = float(entry_lim_y_min.get())
        lim_y_max = float(entry_lim_y_max.get())

        # Actualizar los límites de la gráfica
        ax.set_xlim(lim_x_min, lim_x_max)
        ax.set_ylim(lim_y_min, lim_y_max)

        # Redibujar la gráfica con el zoom aplicado
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos para el zoom.")

# Función para mostrar la pantalla de inicio
def mostrar_pantalla_inicio():
    # Ocultar otros frames
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()

    # Mostrar pantalla de inicio
    frame_inicio.pack(expand=True, fill='both')

# Función para mostrar el menú de trazado
def mostrar_menu_trazado():
    frame_inicio.pack_forget()
    frame_opciones.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()
    frame_trazado.pack(expand=True, fill='both')

# Función para mostrar el menú de opciones
def mostrar_menu_opciones():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_grafica.pack_forget()
    frame_linea_recta.pack_forget()
    frame_opciones.pack(expand=True, fill='both')

# Función para mostrar la interfaz de línea recta
def mostrar_linea_recta():
    frame_inicio.pack_forget()
    frame_trazado.pack_forget()
    frame_opciones.pack_forget()
    frame_grafica.pack(side='right', expand=True, fill='both')
    frame_linea_recta.pack(side='left', fill='both')  # Asegurar que el frame de la línea recta se expanda

# Función para configurar el tamaño de la pantalla
def configurar_tamano_pantalla():
    try:
        ancho = int(entry_ancho.get())
        alto = int(entry_alto.get())
        root.geometry(f"{ancho}x{alto}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

# Función para cambiar la resolución a HD (1280x720)
def cambiar_resolucion_hd():
    root.geometry("1280x720")

# Función para cambiar la resolución a Full HD (1920x1080)
def cambiar_resolucion_full_hd():
    root.geometry("1920x1080")

# Función para cambiar la resolución a 2K (2560x1440)
def cambiar_resolucion_2k():
    root.geometry("2560x1440")

# Función para cambiar la resolución a 4K (3840x2160)
def cambiar_resolucion_4k():
    root.geometry("3840x2160")

# Función para salir de la aplicación
def salir():
    root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Aplicación de Gráficos")
root.state('zoomed')  # Pantalla completa

# Frame de inicio
frame_inicio = tk.Frame(root)
tk.Label(frame_inicio, text="Pantalla de Inicio", font=("Arial", 16)).pack(pady=20)
tk.Button(frame_inicio, text="1. Selección de Trazado", command=mostrar_menu_trazado, width=20).pack(pady=10)
tk.Button(frame_inicio, text="2. Opciones", command=mostrar_menu_opciones, width=20).pack(pady=10)
tk.Button(frame_inicio, text="3. Salir", command=salir, width=20).pack(pady=10)

# Frame de selección de trazado
frame_trazado = tk.Frame(root)
tk.Label(frame_trazado, text="Selección de Trazado", font=("Arial", 16)).pack(pady=20)
tk.Button(frame_trazado, text="1. Línea Recta", command=mostrar_linea_recta, width=20).pack(pady=10)
tk.Button(frame_trazado, text="2. Triángulo", command=lambda: messagebox.showinfo("Info", "Triángulo seleccionado"), width=20).pack(pady=10)
tk.Button(frame_trazado, text="3. Círculo", command=lambda: messagebox.showinfo("Info", "Círculo seleccionado"), width=20).pack(pady=10)
tk.Button(frame_trazado, text="4. Regresar", command=mostrar_pantalla_inicio, width=20).pack(pady=10)

# Frame de opciones
frame_opciones = tk.Frame(root)
tk.Label(frame_opciones, text="Opciones", font=("Arial", 16)).pack(pady=20)

# Botones para cambiar la resolución
tk.Label(frame_opciones, text="Cambiar Resolución:", font=("Arial", 12)).pack(pady=5)
tk.Button(frame_opciones, text="HD (1280x720)", command=cambiar_resolucion_hd, width=20).pack(pady=5)
tk.Button(frame_opciones, text="Full HD (1920x1080)", command=cambiar_resolucion_full_hd, width=20).pack(pady=5)
tk.Button(frame_opciones, text="2K (2560x1440)", command=cambiar_resolucion_2k, width=20).pack(pady=5)
tk.Button(frame_opciones, text="4K (3840x2160)", command=cambiar_resolucion_4k, width=20).pack(pady=5)

# Entradas de datos para el tamaño manual
tk.Label(frame_opciones, text="Tamaño Manual:", font=("Arial", 12)).pack(pady=10)
tk.Label(frame_opciones, text="Ancho de pantalla:").pack()
entry_ancho = tk.Entry(frame_opciones, width=10)
entry_ancho.pack()
tk.Label(frame_opciones, text="Alto de pantalla:").pack()
entry_alto = tk.Entry(frame_opciones, width=10)
entry_alto.pack()
tk.Button(frame_opciones, text="Aplicar", command=configurar_tamano_pantalla, width=20).pack(pady=10)

# Botón de regresar
tk.Button(frame_opciones, text="Regresar", command=mostrar_pantalla_inicio, width=20).pack(pady=10)

# Frame de línea recta
frame_linea_recta = tk.Frame(root, padx=10, pady=10)
tk.Label(frame_linea_recta, text="Línea Recta - Método DDA", font=("Arial", 12, "bold")).pack(pady=5)

# Entradas de datos para la línea recta
entry_xa = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Xa:").pack()
entry_xa.pack()

entry_ya = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Ya:").pack()
entry_ya.pack()

entry_xb = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Xb:").pack()
entry_xb.pack()

entry_yb = tk.Entry(frame_linea_recta, width=10)
tk.Label(frame_linea_recta, text="Yb:").pack()
entry_yb.pack()

# Botón de cálculo
tk.Button(frame_linea_recta, text="Calcular y Graficar", command=calcular_y_graficar, bg="green", fg="white").pack(pady=10)

# Resultado de la pendiente
label_resultado = tk.Label(frame_linea_recta, text="Pendiente (m): ", font=("Arial", 12))
label_resultado.pack(pady=5)

# Etiqueta para mostrar las coordenadas del mouse
label_coordenadas = tk.Label(frame_linea_recta, text="Coordenadas: ", font=("Arial", 10))
label_coordenadas.pack(pady=5)

# Campos de entrada para el zoom manual
tk.Label(frame_linea_recta, text="Zoom Manual", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(frame_linea_recta, text="Limite X Min:").pack()
entry_lim_x_min = tk.Entry(frame_linea_recta, width=10)
entry_lim_x_min.pack()

tk.Label(frame_linea_recta, text="Limite X Max:").pack()
entry_lim_x_max = tk.Entry(frame_linea_recta, width=10)
entry_lim_x_max.pack()

tk.Label(frame_linea_recta, text="Limite Y Min:").pack()
entry_lim_y_min = tk.Entry(frame_linea_recta, width=10)
entry_lim_y_min.pack()

tk.Label(frame_linea_recta, text="Limite Y Max:").pack()
entry_lim_y_max = tk.Entry(frame_linea_recta, width=10)
entry_lim_y_max.pack()

# Botón de zoom manual
tk.Button(frame_linea_recta, text="Aplicar Zoom", command=zoom_manual, bg="blue", fg="white").pack(pady=10)

# Botón de limpieza
tk.Button(frame_linea_recta, text="Limpiar Gráfica", command=limpiar_grafica, bg="red", fg="white").pack(pady=10)

# Frame de gráfica
frame_grafica = tk.Frame(root, padx=10, pady=10, bg='white')

# Frame de tabla
frame_tabla = tk.Frame(frame_linea_recta, pady=10)
frame_tabla.pack(fill='both', expand=True)  # Asegurar que el frame de la tabla esté visible

# Inicializar la gráfica vacía
inicializar_grafica()

# Mostrar pantalla de inicio al iniciar
mostrar_pantalla_inicio()

root.mainloop()