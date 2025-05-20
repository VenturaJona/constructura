from ttkbootstrap import Window
from ttkbootstrap.widgets import Label, Entry, Button
from tkinter import messagebox
from conexion.conexion import conexion
import subprocess
import sys
import bcrypt

root = Window(themename="darkly")
root.iconbitmap("icon.ico")
root.title("Constructora Login")
root.geometry("900x800")

def entrar():
    nombre = nombre_entry.get().strip()
    contrasena = contrasena_entry.get().strip()
    
    if not nombre or not contrasena:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    try:
        conn = conexion()
        cursor = conn.cursor()
        
        # Obtener el hash almacenado para este usuario
        cursor.execute("SELECT nombre, contrasena FROM clientes WHERE nombre = ?", (nombre,))
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            nombre_db, hashed_db = resultado
            # Verificar la contraseña con el hash almacenado
            if bcrypt.checkpw(contrasena.encode('utf-8'), hashed_db):
                messagebox.showinfo("Éxito", f"Bienvenido {nombre}")
                root.destroy()
                subprocess.Popen([sys.executable, "app.py", nombre])
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")
            
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        print(f"Error completo: {str(e)}")  # Para depuración

# Interfaz gráfica
Label(root, text="Inicio de Sesión", font=('Helvetica', 16, 'bold'), bootstyle="info").pack(pady=20)

nombre_entry = Entry(root, font=('Helvetica', 12))
nombre_entry.pack(pady=10)

contrasena_entry = Entry(root, font=('Helvetica', 12), show="*")  # Ocultar contraseña
contrasena_entry.pack(pady=10)

Button(root, text="Entrar", command=entrar, bootstyle="success-outline").pack(pady=10)

root.mainloop()