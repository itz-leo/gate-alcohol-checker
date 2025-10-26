import os
import json
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image # Importante

# Cargar variables de entorno (API_KEY) desde un archivo .env
load_dotenv()

# 1. Verificar y configurar la API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=api_key)

# 2. Usar el nombre de modelo
model_name = 'gemini-2.5-flash'
model = genai.GenerativeModel(model_name)

# 3. PROMPT
PROMPT_BOTELLA = """
You are an expert quality inspector for an airline catering company. Analyze the provided image of an alcohol bottle.
Based on your visual assessment, return a valid JSON object with the following keys and value types:
- "cleanliness": string, one of 'Excellent', 'Good', 'Fair', 'Poor'. Assess smudges, residue, or dirt.
- "sealStatus": string, one of 'Sealed', 'Resealed', 'Opened'. Look for an intact foil/plastic seal over the cap. If it's broken or missing, it's 'Opened'.
- "fillLevel": number, an estimated percentage of liquid remaining in the bottle, from 0 to 100.
- "labelStatus": string, one of 'Intact', 'Slightly Damaged', 'Heavily Damaged'. Look for tears, water damage, or peeling.

Your response must be ONLY the JSON object, without any surrounding text, explanations, or markdown formatting like ```json.
"""

def analizar_pil_image(img: Image.Image) -> dict:
    """
    Analiza un objeto de imagen PIL y devuelve un dict.
    """
    try:
        # Enviar el prompt y la imagen al modelo
        response = model.generate_content([PROMPT_BOTELLA, img])
        text = response.text.strip()
        
        # Limpiar la respuesta para asegurar que sea un JSON válido
        cleaned_text = text.replace("```json", "").replace("```", "").strip()
        
        parsed_data = json.loads(cleaned_text)
        return parsed_data
        
    except Exception as e:
        print(f"Error llamando a la API de Gemini: {e}")
        raise Exception("Failed to get a valid analysis from the AI model.")


def analizar_imagen_botella(file_path: str) -> dict:
    """
    Analiza una imagen de botella desde una ruta de archivo y devuelve un dict.
    """
    
    # 3. Verificar si el archivo existe
    image_path = Path(file_path)
    if not image_path.exists():
        raise FileNotFoundError(f"File not found at path: {file_path}")

    # 4. Cargar la imagen usando PIL
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        raise

    # 5. Llamar a la función principal de análisis
    return analizar_pil_image(img)


if __name__ == "__main__":
    ruta_de_imagen = "img/botella1.jpg" 
    
    try:
        analisis = analizar_imagen_botella(ruta_de_imagen)
        print("Análisis completado:")
        print(json.dumps(analisis, indent=2))
        
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)