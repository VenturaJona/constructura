import sqlite3

def conexion():
    try: 
        conn = sqlite3.connect('../constructora.db')
        return conn
    except sqlite3.Error as err:
        print(f"Error de conexión: {err}")
        return None

# Llamada a la función para probar la conexión
if __name__ == "__main__":
    conexion()
