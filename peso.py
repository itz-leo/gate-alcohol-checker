from conexionBD import *

def registrar_peso(peso_actual_gramos): #Peso en gramos. Obtenido por la bascula
    print(f"⚖️ Peso registrado: {peso_actual_gramos}g")
    return peso_actual_gramos

def obtener_botella(nombre_botella): #Obtiene la información de la botella mediante escaner
    print(f"🧾 Botella identificada: {nombre_botella}")
    return nombre_botella

def obtener_peso_max(nombre_botella):
    conexion,cursor = conectar()
    # Botella viene como parámetro
    botella = obtener_botella(nombre_botella)
    cursor.execute(f"select Peso from botellas_nuevas where nombre ='{botella}'")
    peso_max = cursor.fetchone()
    if peso_max:
        return peso_max[0]
    else:
        print(f"ADVERTENCIA: No se encontró peso máximo para '{nombre_botella}' en la BD.")
        return None

def obtener_politica(Aerolinea):
    conexion,cursor = conectar()
    cursor.execute(f"select Porcentaje_Contenido from sla_policy where Aerolinea='{Aerolinea}'")
    politica = cursor.fetchone()
    if politica:
        return politica[0]
    else:
        print(f"ADVERTENCIA: No se encontró política SLA para '{Aerolinea}'. Usando 70% por defecto.")
        return 70

def determinar_porcentaje(nombre_botella, peso_actual_gramos, Aerolinea):
    peso = registrar_peso(peso_actual_gramos) #Obtener el peso de la botella en la workstation
    peso_max = obtener_peso_max(nombre_botella) #Obtener peso maximo de la botella seleccionada
    
    if peso_max is None or peso_max == 0:
        print("Error: No se puede calcular porcentaje sin peso máximo. Asumiendo 0%.")
        return 0.0 # No se puede dividir por cero o None

    porcentaje = (peso*100)/peso_max
    print(f"Cálculo de porcentaje: ({peso} * 100) / {peso_max} = {porcentaje:.2f}%")
    return porcentaje
