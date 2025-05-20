import sys
import re
from ttkbootstrap import Window
from ttkbootstrap.widgets import Label, Entry, Button, Separator, DateEntry
from tkinter import ttk, messagebox
from conexion.conexion import conexion

# Validar si el script fue llamado con argumento
if len(sys.argv) <= 1:
    messagebox.showerror("Acceso denegado", "Debes iniciar sesión primero")
    sys.exit()

nombre_usuario = sys.argv[1]

# Crear ventana principal
root = Window(themename="darkly")
root.title("Constructora")
root.iconbitmap("icon.ico")
root.geometry("900x800")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.columnconfigure(0, weight=1)

# Variables globales
id_material_seleccionado = None

# ---------------- FUNCIONES DE VALIDACIÓN ----------------

def limpiar_caracteres(texto, tipo="general"):
    """Elimina caracteres especiales según el tipo de dato"""
    if not texto:
        return ""
    
    # Limpieza básica para todos los casos
    texto = texto.strip()
    
    if tipo == "nombre":
        # Permite letras, números, espacios y algunos caracteres básicos
        return re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\-\.]', '', texto)
    elif tipo == "id":
        # Solo números
        return re.sub(r'[^0-9]', '', texto)
    elif tipo == "fecha":
        # Formato fecha YYYY-MM-DD
        return re.sub(r'[^0-9\-]', '', texto)
    else:
        # Limpieza general (conserva letras, números y espacios)
        return re.sub(r'[^a-zA-Z0-9\s]', '', texto)

def validar_nombre_material(nombre):
    """Valida el nombre del material"""
    nombre = limpiar_caracteres(nombre, "nombre")
    if not nombre or len(nombre) < 3 or len(nombre) > 100:
        return False, "El nombre debe tener entre 3 y 100 caracteres válidos"
    return True, nombre

# ---------------- FUNCIONES PRINCIPALES ----------------

def mostrar_materiales():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id_materiales, nombre FROM materiales")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()
        mostrar_label.config(text="Materiales cargados correctamente", bootstyle="info")
    except Exception as e:
        mostrar_label.config(text=f"Error al mostrar materiales: {str(e)}", bootstyle="danger")

def on_material_select(event):
    global id_material_seleccionado
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], 'values')
        id_material_seleccionado = values[0]
        nombre_entry.delete(0, 'end')
        nombre_entry.insert(0, values[1])

def registrar_material():
    nombre = nombre_entry.get()
    valido, mensaje = validar_nombre_material(nombre)
    if not valido:
        registro_label.config(text=mensaje, bootstyle="danger")
        return
    
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO materiales (nombre) VALUES (?)", (mensaje,))  # Usamos el nombre validado
        conn.commit()
        conn.close()
        nombre_entry.delete(0, 'end')
        mostrar_materiales()
        registro_label.config(text="Material registrado", bootstyle="success")
    except Exception as e:
        registro_label.config(text=f"Error: {str(e)}", bootstyle="danger")

def actualizar_material():
    global id_material_seleccionado
    nombre = nombre_entry.get()
    valido, mensaje = validar_nombre_material(nombre)
    
    if not valido:
        registro_label.config(text=mensaje, bootstyle="danger")
        return
        
    if not id_material_seleccionado:
        registro_label.config(text="Selecciona un material", bootstyle="warning")
        return
        
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE materiales SET nombre = ? WHERE id_materiales = ?", 
                     (mensaje, id_material_seleccionado))  # Usamos el nombre validado
        conn.commit()
        conn.close()
        nombre_entry.delete(0, 'end')
        id_material_seleccionado = None
        mostrar_materiales()
        registro_label.config(text="Material actualizado", bootstyle="success")
    except Exception as e:
        registro_label.config(text=f"Error: {str(e)}", bootstyle="danger")

def eliminar_material():
    global id_material_seleccionado
    if not id_material_seleccionado:
        registro_label.config(text="Selecciona un material", bootstyle="warning")
        return
        
    try:
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materiales WHERE id_materiales = ?", (id_material_seleccionado,))
        conn.commit()
        conn.close()
        nombre_entry.delete(0, 'end')
        id_material_seleccionado = None
        mostrar_materiales()
        registro_label.config(text="Material eliminado", bootstyle="success")
    except Exception as e:
        registro_label.config(text=f"Error: {str(e)}", bootstyle="danger")

def registrar_cita():
    fecha = limpiar_caracteres(fecha_entry.entry.get(), "fecha")
    if not fecha or len(fecha) != 10:  # YYYY-MM-DD
        cita_label.config(text="Fecha inválida", bootstyle="danger")
        return
        
    try:
        conn = conexion()
        cursor = conn.cursor()
        # Validamos también el nombre de usuario
        usuario_limpio = limpiar_caracteres(nombre_usuario, "nombre")
        cursor.execute("SELECT id_clientes FROM clientes WHERE nombre = ?", (usuario_limpio,))
        cliente = cursor.fetchone()
        
        if not cliente:
            cita_label.config(text="Cliente no encontrado", bootstyle="danger")
            return
            
        id_cliente = cliente[0]
        cursor.execute("INSERT INTO citas (id_clientes, fecha) VALUES (?, ?)", (id_cliente, fecha))
        conn.commit()
        conn.close()
        cita_label.config(text="Cita registrada", bootstyle="success")
    except Exception as e:
        cita_label.config(text=f"Error: {str(e)}", bootstyle="danger")

# ---------------- INTERFAZ (igual que antes) ----------------

usuario_label = Label(main_frame, text=f"Usuario: {nombre_usuario}", font=('Helvetica', 18, 'bold'), anchor="center")
usuario_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

Label(main_frame, text="Registrar Material", font=('Helvetica', 16, 'bold'), bootstyle="info").grid(row=1, column=0, sticky="ew")

nombre_entry = Entry(main_frame, font=('Helvetica', 12))
nombre_entry.grid(row=2, column=0, pady=5, sticky="ew")

btn_frame = ttk.Frame(main_frame)
btn_frame.grid(row=3, column=0, pady=10, sticky="ew")
Button(btn_frame, text="Registrar", command=registrar_material, bootstyle="success").grid(row=0, column=0, padx=5)
Button(btn_frame, text="Actualizar", command=actualizar_material, bootstyle="warning").grid(row=0, column=1, padx=5)
Button(btn_frame, text="Eliminar", command=eliminar_material, bootstyle="danger").grid(row=0, column=2, padx=5)

registro_label = Label(main_frame, text="", font=('Helvetica', 12))
registro_label.grid(row=4, column=0, pady=5, sticky="ew")

Separator(main_frame, bootstyle="secondary").grid(row=5, column=0, pady=20, sticky="ew")

tree = ttk.Treeview(main_frame, columns=("ID", "Nombre"), show="headings", height=10)
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.column("ID", width=80, anchor="center")
tree.column("Nombre", width=300, anchor="center")
tree.grid(row=6, column=0, sticky="nsew")
tree.bind("<<TreeviewSelect>>", on_material_select)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=6, column=1, sticky="ns")

main_frame.rowconfigure(6, weight=1)

mostrar_label = Label(main_frame, text="", font=('Helvetica', 12))
mostrar_label.grid(row=7, column=0, pady=10, sticky="ew")

Separator(main_frame, bootstyle="secondary").grid(row=8, column=0, pady=20, sticky="ew")

# --- Sección de Citas ---
Label(main_frame, text="Agendar Cita", font=('Helvetica', 16, 'bold'), bootstyle="info").grid(row=9, column=0, sticky="ew", pady=(10, 10))
fecha_entry = DateEntry(main_frame, dateformat="%Y-%m-%d", width=20)
fecha_entry.grid(row=10, column=0, pady=5, sticky="ew")
Button(main_frame, text="Registrar Cita", command=registrar_cita, bootstyle="success-outline").grid(row=11, column=0, pady=5, sticky="ew")

cita_label = Label(main_frame, text="", font=('Helvetica', 12))
cita_label.grid(row=12, column=0, pady=5, sticky="ew")

# ---------------- Cargar datos ----------------

mostrar_materiales()
root.mainloop()