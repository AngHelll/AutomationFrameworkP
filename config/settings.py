import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configuraciones generales
BASE_URL = os.getenv("BASE_URL", "https://example.com/login")  # URL del sitio de prueba
BROWSER = os.getenv("BROWSER", "chrome")  # Navegador por defecto

# Tiempo de espera implícito en segundos
IMPLICIT_WAIT = 10

# Credenciales de prueba
TEST_USER = os.getenv("TEST_USER", "usuario_prueba")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password_prueba")
