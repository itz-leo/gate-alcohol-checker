# --- conexionBD.py (ACTUALIZADO) ---

import mysql.connector

def conectar():
    try:
        conexion=mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="bottle_handling"
        )
        cursor=conexion.cursor(buffered=True)
        return conexion, cursor
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise e

def verificar_usuario(username, password):
    try:
        conexion, cursor = conectar()
        
        # Usamos parámetros (%s) para prevenir Inyección SQL
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        
        cursor.execute(query, (username, password))
        
        resultado = cursor.fetchone() # Obtiene un resultado (o None)
        
        cursor.close()
        conexion.close()
        
        if resultado:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error durante la verificación de usuario: {e}")
        # Si hay un error de BD (ej. tabla no existe), fallamos la validación
        # y lo reportamos a la consola de Streamlit.
        raise Exception(f"Error de base de datos al verificar usuario: {e}")
