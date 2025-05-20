from ttkbootstrap import Window
from ttkbootstrap.widgets import Label, Entry, Button
from tkinter import messagebox
from conexion.conexion import conexion
import subprocess
import sys
import bcrypt

root = Window(themename="darkly")
root.iconbitmap("icon.ico")
root.title("Constructora Registro")
root.geometry("900x800")

def registro_clientes():
    try:
        # Obtener datos del formulario
        nombre = nombre_entry.get().strip()
        telefono = telefono_entry.get().strip()
        contrasena = contrasena_entry.get().strip()
        
        # Validaciones básicas
        if not nombre or not telefono or not contrasena:
            registro_label.config(text="Error: Todos los campos son obligatorios", bootstyle="danger")
            return
            
        # Validar que el teléfono sea numérico
        if not telefono.isdigit():
            registro_label.config(text="Error: El teléfono debe contener solo números", bootstyle="danger")
            return
            
        # Validar longitud del teléfono (ejemplo: mínimo 8 dígitos)
        if len(telefono) < 8:
            registro_label.config(text="Error: Teléfono demasiado corto", bootstyle="danger")
            return
            
        # Verificar si el teléfono ya existe
        conn = conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT telefono FROM clientes WHERE telefono = ?", (telefono,))
        if cursor.fetchone() is not None:
            registro_label.config(text="Error: Este teléfono ya está registrado", bootstyle="danger")
            conn.close()
            return
            
        # Hash de la contraseña
        hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        
        # Insertar nuevo cliente
        cursor.execute(
            "INSERT INTO clientes (nombre, telefono, contrasena) VALUES (?, ?, ?)", 
            (nombre, telefono, hashed)
        )
        conn.commit()
        conn.close()
        
        # Mensaje de éxito y redirección
        messagebox.showinfo("Éxito", "Registro exitoso. Ahora puedes iniciar sesión.")
        root.destroy()
        subprocess.Popen([sys.executable, "login.py"])
        
    except Exception as e:
        registro_label.config(text=f"Error: {str(e)}", bootstyle="danger")
        print(f"Error completo: {str(e)}")  # Para depuración

# Interfaz gráfica
Label(root, text="Registrar cliente", font=('Helvetica', 14)).pack(pady=10)

nombre_entry = Entry(root, font=('Helvetica', 12))
nombre_entry.pack(pady=10)

telefono_entry = Entry(root, font=('Helvetica', 12))
telefono_entry.pack(pady=10)

contrasena_entry = Entry(root, font=('Helvetica', 12), show="*")  # Ocultar contraseña
contrasena_entry.pack(pady=10)

Button(root, text="Registrar", command=registro_clientes, bootstyle="primary").pack(pady=10)

registro_label = Label(root, text="", font=('Helvetica', 12))
registro_label.pack(pady=10)

# Link para ir a login
Button(
    root, 
    text="¿Ya tienes cuenta? Inicia sesión aquí", 
    bootstyle="link", 
    command=lambda: [root.destroy(), subprocess.Popen([sys.executable, "login.py"])]
).pack()

root.mainloop()