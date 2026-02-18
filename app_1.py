import os
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("GENAI_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la variable GENAI_API_KEY")

# Inicializar cliente de Gemini
client = genai.Client(api_key=API_KEY)

# Petición simple al modelo
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explica qué es la inferencia en Inteligencia Artificial en menos de 50 palabras."
)

# Mostrar respuesta
print(response.text)
