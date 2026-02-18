import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --------------------------------------------------
# Cargar variables de entorno
# --------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró GENAI_API_KEY en el archivo .env")

# --------------------------------------------------
# Inicializar cliente Gemini
# --------------------------------------------------
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# Función solicitada
# --------------------------------------------------
def procesar_articulo(texto, tarea):
    """
    Procesa un artículo usando IA.

    :param texto: Texto largo a procesar
    :param tarea: 'resumir' o 'profesionalizar'
    :return: Texto procesado
    """

    if tarea not in ["resumir", "profesionalizar"]:
        raise ValueError("La tarea debe ser 'resumir' o 'profesionalizar'")

    system_instruction = """
Eres un Editor Editorial de prestigio.
Editas textos con altos estándares de claridad,
precisión técnica y rigor profesional.
"""

    if tarea == "resumir":
        prompt = f"""
Genera un resumen ejecutivo del siguiente texto:

{texto}
"""
    else:
        prompt = f"""
Edita el siguiente texto para que suene formal,
técnico y profesional, manteniendo el significado original:

{texto}
"""

    config = types.GenerateContentConfig(
        max_output_tokens=2048,
        system_instruction=system_instruction # Instrucción del sistema para guiar el comportamiento del modelo
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=config,
        contents=prompt
    )

    return response.text


# 
# Ejecución del programa
# 
if __name__ == "__main__":
    texto_prueba = """
    La inteligencia artificial está cambiando la manera en que las organizaciones
    analizan información, optimizan procesos y toman decisiones estratégicas.
    """

    print("=== Procesador de Textos Inteligente ===")
    print("1. Resumir")
    print("2. Profesionalizar\n")

    opcion = input("Seleccione una opción (1 o 2): ")

    if opcion == "1":
        resultado = procesar_articulo(texto_prueba, "resumir")
    elif opcion == "2":
        resultado = procesar_articulo(texto_prueba, "profesionalizar")
    else:
        raise ValueError("Opción inválida")

    print("\n--- Resultado ---\n")
    print(resultado)
