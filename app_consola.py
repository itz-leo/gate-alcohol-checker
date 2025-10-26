import os
from main import decidir_accion, _normalize_airline
from peso import determinar_porcentaje
from analisis_vision import analizar_imagen_botella

def ejecutar_proceso_completo():
    print("--- Iniciando Proceso de Clasificación de Botellas ---")
    
    # 1. SIMULACIÓN DE ENTRADAS DEL HARDWARE
    aerolinea_input = input("✈️ Introduce el nombre de la Aerolínea (ej: PatoVuelo): ")
    aerolinea_norm = _normalize_airline(aerolinea_input) # Aquí se usa el normalizador de main.py
    
    # Simula el escaneo del código de barras
    nombre_botella_input = input("🧾 Escanea la botella (introduce el nombre, ej: 'Kahlúa Liqueur '): ")
    
    # Simula la lectura de la báscula
    try:
        peso_input = float(input("⚖️ Introduce el peso actual en gramos (ej: 500): "))
    except ValueError:
        print("Error: Peso inválido. Abortando.")
        return

    # Simula la captura de la cámara
    ruta_imagen_input = input("📸 Introduce la ruta a la imagen de la botella (ej: 'img/botella1.jpg'): ")

    if not os.path.exists(ruta_imagen_input):
        print(f"Error: La imagen '{ruta_imagen_input}' no existe. Abortando.")
        print("Por favor, crea una imagen de prueba y asegúrate que la ruta es correcta.")
        return

    print("\n--- Procesando Datos ---")

    # 2. OBTENER DATOS DE VISIÓN (Gemini API)
    datos_vision = analizar_imagen_botella(ruta_imagen_input)
    
    # 3. OBTENER DATOS DE PESO (BD + Báscula)
    # Esta función devuelve el porcentaje REAL
    porcentaje_real = determinar_porcentaje(nombre_botella_input, peso_input, aerolinea_norm)

    # 4. ENSAMBLAR DICCIONARIO para main.py
    datos_completos = {
        "ESTATUS_SELLO": datos_vision.get("sealStatus", "Opened"),
        "ESTATUS_ETIQUETA": datos_vision.get("labelStatus", "Heavily Damaged"),
        "LIMPIEZA": datos_vision.get("cleanliness", "Poor"),
        "PORCENTAJE_CONTENIDO": porcentaje_real # Esto viene de la báscula
    }
    
    print(f"\n--- Datos Compilados para Decisión ---")
    print(datos_completos)

    # 5. TOMAR DECISIÓN
    accion_final = decidir_accion(datos_completos, aerolinea_norm)
    
    print("\n================================")
    print(f"  ACCIÓN RECOMENDADA: {accion_final}  ")
    print("================================")

if __name__ == "__main__":
    ejecutar_proceso_completo()