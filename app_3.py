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
    raise ValueError("❌ No se encontró GENAI_API_KEY en el archivo .env")

# --------------------------------------------------
# Inicializar cliente Gemini
# --------------------------------------------------
client = genai.Client(api_key=API_KEY)

# --------------------------------------------------
# Configuración del sistema (ROL)
# --------------------------------------------------
config = types.GenerateContentConfig(
    max_output_tokens=2048,
    system_instruction="""
Eres un vendedor amable y profesional de una tienda de tecnología.
Tu objetivo es asesorar a los clientes de forma clara, cordial y técnica,
explicando especificaciones de productos tecnológicos de manera sencilla.
"""
)

# --------------------------------------------------
# Historial inicial (FEW-SHOT) - CORREGIDO
# --------------------------------------------------
history = [
    {
        "role": "user",
        "parts": [
            {"text": "¿Qué características tiene el portátil Lenovo ThinkPad X1?"}
        ]
    },
    {
        "role": "model",
        "parts": [
            {
                "text": (
                    "El Lenovo ThinkPad X1 cuenta con procesador Intel Core i7, "
                    "16 GB de RAM, almacenamiento SSD de 1 TB, pantalla de 14 pulgadas "
                    "Full HD y un diseño ligero ideal para trabajo profesional."
                )
            }
        ]
    },
    {
        "role": "user",
        "parts": [
            {"text": "¿Qué me puedes decir del iPhone 14?"}
        ]
    },
    {
        "role": "model",
        "parts": [
            {
                "text": (
                    "El iPhone 14 incluye una pantalla OLED de 6.1 pulgadas, "
                    "chip A15 Bionic, sistema de doble cámara de 12 MP, "
                    "conectividad 5G y alto rendimiento."
                )
            }
        ]
    }
]

# --------------------------------------------------
# Inicializar chat con historial
# --------------------------------------------------
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=config,
    history=history
)

print("=== Chat de Soporte – Tienda de Tecnología ===")
print("Escribe 'finalizar' para terminar\n")

# --------------------------------------------------
# Bucle de conversación
# --------------------------------------------------
while True:
    user_input = input("Cliente: ")

    if user_input.lower() == "finalizar":
        print("Vendedor: ¡Gracias por visitar nuestra tienda! 😊")
        break

    try:
        response = chat.send_message(user_input)
        print(f"\nVendedor: {response.text}\n")

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
