# 🚀 Guía Completa para Novatos - Framework de Automatización

## 📖 ¿Qué es este proyecto?

Este es un **Framework de Automatización de Pruebas** construido con Python. En términos simples, es una herramienta que permite automatizar la prueba de sitios web de manera profesional y organizada.

### 🤔 ¿Para qué sirve?

- **Automatizar pruebas**: En lugar de hacer clic manualmente en un sitio web, este framework lo hace automáticamente
- **Ahorrar tiempo**: Ejecuta cientos de pruebas en minutos en lugar de horas
- **Detectar errores**: Encuentra problemas en sitios web antes de que los usuarios los vean
- **Mantener calidad**: Asegura que el sitio web funcione correctamente después de cambios

---

## 🎯 Conceptos Básicos que Necesitas Entender

### 1. **¿Qué es Python?**
Python es un lenguaje de programación muy popular y fácil de aprender. Es como escribir instrucciones en español para que la computadora las entienda.

**Ejemplo simple:**
```python
# Esto es Python
nombre = "Juan"
edad = 25
print(f"Hola {nombre}, tienes {edad} años")
```

### 2. **¿Qué es Selenium?**
Selenium es una herramienta que permite controlar un navegador web (Chrome, Firefox) desde código Python. Es como tener un "robot" que hace clic y navega por sitios web.

### 3. **¿Qué es Pytest?**
Pytest es un framework para ejecutar pruebas de manera organizada. Es como un "organizador" que ejecuta todas tus pruebas y te dice cuáles pasaron y cuáles fallaron.

---

## 🏗️ Estructura del Proyecto (Explicado de Forma Simple)

```
AutomationFramework/          ← Carpeta principal del proyecto
├── config/                  ← Configuraciones (como ajustes del navegador)
├── pages/                   ← Páginas web que vamos a probar
├── tests/                   ← Las pruebas que vamos a ejecutar
├── utils/                   ← Herramientas útiles
├── test_data/              ← Datos de prueba
├── logs/                    ← Registros de lo que pasa
├── screenshots/             ← Capturas de pantalla cuando algo falla
└── reports/                 ← Reportes de las pruebas
```

**Explicación simple:**
- **config**: Es como la "configuración" de tu teléfono - ajustes básicos
- **pages**: Son las páginas web que vamos a probar (como Facebook, Google)
- **tests**: Son las "preguntas" que le hacemos al sitio web para ver si funciona
- **utils**: Son herramientas que nos ayudan (como un martillo para un carpintero)
- **test_data**: Son los datos que usamos para las pruebas (usuarios, contraseñas)
- **logs**: Es como un "diario" que registra todo lo que pasa
- **screenshots**: Son fotos que se toman cuando algo sale mal
- **reports**: Son resúmenes de cómo salieron las pruebas

---

## 🚀 Cómo Empezar (Paso a Paso)

### Paso 1: Instalar Python
1. Ve a [python.org](https://python.org)
2. Descarga la versión más reciente de Python
3. Instálala (marca la casilla "Add Python to PATH")
4. Verifica la instalación abriendo una terminal y escribiendo: `python --version`

### Paso 2: Descargar el Proyecto
1. Abre una terminal (PowerShell en Windows)
2. Navega a donde quieres guardar el proyecto
3. Ejecuta: `git clone <URL-del-proyecto>`
4. Entra a la carpeta: `cd AutomationFramework`

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

**¿Qué hace esto?**
- `pip` es como un "gestor de paquetes" que instala herramientas
- `requirements.txt` es una lista de todas las herramientas que necesitamos
- Es como ir a una tienda con una lista de compras

### Paso 4: Configurar el Entorno
Crea un archivo llamado `.env` en la carpeta principal:

```env
# Configuración básica
TEST_ENV=staging
BASE_URL=https://cli.github.com

# Configuración del navegador
BROWSER=chrome
HEADLESS=false
IMPLICIT_WAIT=10
EXPLICIT_WAIT=20

# Configuración de pruebas
SCREENSHOT_ON_FAILURE=true
RETRY_COUNT=3
RETRY_DELAY=2
```

**¿Qué significa cada línea?**
- `TEST_ENV=staging`: El entorno de pruebas (como "modo de prueba")
- `BASE_URL`: La dirección del sitio web que vamos a probar
- `BROWSER=chrome`: Qué navegador usar (Chrome, Firefox, Edge)
- `HEADLESS=false`: Si queremos ver el navegador (false = sí, true = no)
- `IMPLICIT_WAIT=10`: Cuánto esperar por elementos (en segundos)
- `SCREENSHOT_ON_FAILURE=true`: Tomar fotos cuando algo falle

---

## 🧪 Ejecutar tu Primera Prueba

### Opción 1: Ejecutar Todas las Pruebas
```bash
pytest
```

### Opción 2: Ejecutar Pruebas Específicas
```bash
# Solo pruebas de login
pytest tests/test_login.py

# Solo pruebas de GitHub CLI
pytest tests/test_github_cli.py

# Con más información
pytest -v

# Ver lo que pasa en tiempo real
pytest -s
```

### Opción 3: Ejecutar en Modo Visual
```bash
# Ver el navegador mientras se ejecutan las pruebas
pytest --browser=chrome --headless=false
```

---

## 📝 Entender el Código (Explicado de Forma Simple)

### Ejemplo 1: Página de Login
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_page_loaded(self):
        """Verificar si la página cargó correctamente"""
        return "Example Domain" in self.driver.title
```

**¿Qué hace cada parte?**
- `from selenium...`: Importar herramientas de Selenium (como traer herramientas de una caja)
- `class LoginPage`: Crear una "clase" que representa la página de login
- `def __init__(self, driver)`: Constructor - se ejecuta cuando creamos la página
- `self.driver = driver`: Guardar el navegador para usarlo después
- `self.wait = WebDriverWait(driver, 10)`: Crear un "esperador" de 10 segundos
- `def is_page_loaded(self)`: Función que verifica si la página cargó

### Ejemplo 2: Una Prueba Simple
```python
import pytest
from pages.login_page import LoginPage

class TestLogin:
    def test_page_loads(self, driver):
        """Verificar que la página de login carga correctamente"""
        # Crear la página de login
        login_page = LoginPage(driver)
        
        # Verificar que la página cargó
        assert login_page.is_page_loaded()
        
        # Verificar que el título es correcto
        assert "Example Domain" in driver.title
```

**¿Qué hace cada parte?**
- `import pytest`: Importar el framework de pruebas
- `from pages.login_page import LoginPage`: Traer la clase LoginPage
- `class TestLogin`: Crear una clase para organizar las pruebas de login
- `def test_page_loads(self, driver)`: Función de prueba (debe empezar con "test_")
- `login_page = LoginPage(driver)`: Crear una instancia de la página de login
- `assert login_page.is_page_loaded()`: Verificar que algo sea verdadero
- `assert "Example Domain" in driver.title`: Verificar que el título contenga cierto texto

---

## 🔧 Conceptos Intermedios

### 1. **Page Object Model (POM)**
Es una forma organizada de escribir código donde cada página web tiene su propia "clase" con métodos específicos.

**Ventajas:**
- Código más organizado
- Fácil de mantener
- Reutilizable

**Ejemplo:**
```python
class LoginPage:
    # Localizadores (dónde encontrar elementos)
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    
    def enter_username(self, username):
        """Escribir nombre de usuario"""
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)
    
    def enter_password(self, password):
        """Escribir contraseña"""
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
    
    def click_login(self):
        """Hacer clic en el botón de login"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
```

### 2. **Localizadores (Cómo Encontrar Elementos)**
```python
# Por ID (más confiable)
(By.ID, "username")

# Por nombre
(By.NAME, "username")

# Por clase CSS
(By.CLASS_NAME, "btn-primary")

# Por texto del enlace
(By.LINK_TEXT, "Iniciar Sesión")

# Por texto parcial del enlace
(By.PARTIAL_LINK_TEXT, "Iniciar")

# Por selector CSS
(By.CSS_SELECTOR, "#username")

# Por XPath (más flexible pero más frágil)
(By.XPATH, "//input[@id='username']")
```

### 3. **Esperas (Waits)**
```python
# Espera implícita (automática)
driver.implicitly_wait(10)  # Espera hasta 10 segundos

# Espera explícita (más control)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Esperar hasta que un elemento sea visible
element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "username"))
)

# Esperar hasta que un elemento sea clickeable
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "login-btn"))
)
```

---

## 🎨 Escribir tu Primera Prueba Completa

Vamos a crear una prueba paso a paso:

### Paso 1: Crear la Página
Crea un archivo `pages/mi_pagina.py`:

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MiPagina:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navegar_a_pagina(self, url):
        """Navegar a una página específica"""
        self.driver.get(url)
    
    def obtener_titulo(self):
        """Obtener el título de la página"""
        return self.driver.title
    
    def buscar_elemento(self, texto):
        """Buscar un elemento por texto"""
        return self.driver.find_element(By.LINK_TEXT, texto)
    
    def hacer_clic_en_enlace(self, texto):
        """Hacer clic en un enlace específico"""
        enlace = self.buscar_elemento(texto)
        enlace.click()
```

### Paso 2: Crear la Prueba
Crea un archivo `tests/test_mi_pagina.py`:

```python
import pytest
from pages.mi_pagina import MiPagina

class TestMiPagina:
    def test_pagina_carga_correctamente(self, driver):
        """Verificar que la página carga correctamente"""
        # Crear instancia de la página
        pagina = MiPagina(driver)
        
        # Navegar a la página
        pagina.navegar_a_pagina("https://www.google.com")
        
        # Verificar que el título contiene "Google"
        titulo = pagina.obtener_titulo()
        assert "Google" in titulo, f"El título '{titulo}' no contiene 'Google'"
        
        print(f"✅ La página cargó correctamente. Título: {titulo}")
    
    def test_buscar_en_google(self, driver):
        """Verificar que podemos buscar en Google"""
        # Crear instancia de la página
        pagina = MiPagina(driver)
        
        # Navegar a Google
        pagina.navegar_a_pagina("https://www.google.com")
        
        # Verificar que estamos en Google
        titulo = pagina.obtener_titulo()
        assert "Google" in titulo
        
        print("✅ Google cargó correctamente")
```

### Paso 3: Ejecutar la Prueba
```bash
# Ejecutar solo esta prueba
pytest tests/test_mi_pagina.py -v

# Ejecutar con más información
pytest tests/test_mi_pagina.py -v -s
```

---

## 🐛 Solucionar Problemas Comunes

### Problema 1: "Element not found"
**Síntoma:** La prueba falla porque no puede encontrar un elemento

**Soluciones:**
1. **Verificar el localizador:**
```python
# En lugar de esto (puede fallar):
elemento = driver.find_element(By.ID, "username")

# Usar esto (más robusto):
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

elemento = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "username"))
)
```

2. **Verificar que la página cargó:**
```python
# Esperar a que la página cargue completamente
WebDriverWait(driver, 10).until(
    lambda driver: driver.execute_script("return document.readyState") == "complete"
)
```

### Problema 2: "Test is flaky" (Prueba inestable)
**Síntoma:** La prueba pasa a veces y falla otras

**Soluciones:**
1. **Usar esperas explícitas:**
```python
# En lugar de esperas implícitas
driver.implicitly_wait(10)

# Usar esperas explícitas
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "button"))
)
```

2. **Implementar reintentos:**
```python
from utils.retry_mechanism import retry_on_exception

@retry_on_exception(max_attempts=3, delay=1.0)
def operacion_inestable():
    """Operación que puede fallar ocasionalmente"""
    return hacer_algo()
```

### Problema 3: "Browser crashes"
**Síntoma:** El navegador se cierra inesperadamente

**Soluciones:**
1. **Usar opciones del navegador:**
```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
```

2. **Limpiar recursos:**
```python
def teardown_method(self):
    """Limpiar después de cada prueba"""
    if hasattr(self, 'driver'):
        self.driver.quit()
```

---

## 📊 Generar Reportes

### Reporte HTML Simple
```bash
# Generar reporte HTML
pytest --html=reports/reporte.html --self-contained-html

# Ver el reporte
# Abre el archivo reports/reporte.html en tu navegador
```

### Reporte con Allure (Más Profesional)
```bash
# Instalar Allure
pip install allure-pytest

# Ejecutar pruebas con Allure
pytest --alluredir=reports/allure-results

# Generar reporte
allure serve reports/allure-results
```

---

## 🚀 Consejos para Principiantes

### 1. **Empieza Simple**
- No intentes automatizar todo de una vez
- Comienza con una sola página
- Agrega funcionalidad gradualmente

### 2. **Usa Nombres Descriptivos**
```python
# ❌ Malo
def test_1(self):
    pass

# ✅ Bueno
def test_login_con_usuario_valido(self):
    pass
```

### 3. **Comenta tu Código**
```python
def test_login_exitoso(self):
    """Verificar que un usuario puede iniciar sesión correctamente"""
    # Paso 1: Navegar a la página de login
    self.login_page.navegar_a_login()
    
    # Paso 2: Ingresar credenciales
    self.login_page.ingresar_usuario("usuario@ejemplo.com")
    self.login_page.ingresar_password("password123")
    
    # Paso 3: Hacer clic en login
    self.login_page.hacer_clic_login()
    
    # Paso 4: Verificar que estamos en el dashboard
    assert self.dashboard_page.esta_en_dashboard()
```

### 4. **Maneja Errores Gracefully**
```python
def test_elemento_con_manejo_de_errores(self):
    """Prueba con manejo de errores"""
    try:
        elemento = self.driver.find_element(By.ID, "elemento-que-puede-no-existir")
        elemento.click()
    except Exception as e:
        print(f"⚠️ El elemento no se encontró: {e}")
        # Continuar con la prueba o hacer algo alternativo
        pass
```

### 5. **Usa Datos de Prueba Externos**
```python
# En lugar de hardcodear datos
def test_login(self):
    self.login_page.login("usuario@ejemplo.com", "password123")

# Usar datos externos
def test_login(self):
    usuario = self.test_data.get_usuario("usuario_valido")
    self.login_page.login(usuario["email"], usuario["password"])
```

---

## 🔍 Debugging (Encontrar y Arreglar Errores)

### 1. **Usar Print Statements**
```python
def test_debug(self):
    print("🔍 Iniciando prueba...")
    
    # Hacer algo
    resultado = self.hacer_algo()
    print(f"🔍 Resultado: {resultado}")
    
    # Verificar algo
    assert resultado == "esperado"
    print("✅ Prueba completada exitosamente")
```

### 2. **Usar Logging**
```python
from utils.logger import logger

def test_con_logging(self):
    logger.info("🚀 Iniciando prueba de login")
    
    try:
        self.login_page.login("usuario", "password")
        logger.info("✅ Login exitoso")
    except Exception as e:
        logger.error(f"❌ Error en login: {e}")
        raise
```

### 3. **Tomar Screenshots**
```python
from utils.screenshot_capture import ScreenshotCapture

def test_con_screenshot(self):
    screenshot = ScreenshotCapture(self.driver)
    
    try:
        # Hacer algo que puede fallar
        self.hacer_algo_riesgoso()
    except Exception as e:
        # Tomar screenshot del error
        screenshot.capture_on_failure("test_con_screenshot", str(e))
        raise
```

---

## 📚 Recursos para Aprender Más

### 1. **Python Básico**
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [W3Schools Python](https://www.w3schools.com/python/)
- [Codecademy Python](https://www.codecademy.com/learn/learn-python-3)

### 2. **Selenium**
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Selenium Tutorial](https://selenium-python.readthedocs.io/getting-started.html)

### 3. **Pytest**
- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Tutorial](https://docs.pytest.org/en/stable/getting-started.html)

### 4. **Videos en Español**
- [YouTube: Python para Principiantes](https://www.youtube.com/results?search_query=python+para+principiantes+español)
- [YouTube: Selenium Tutorial Español](https://www.youtube.com/results?search_query=selenium+tutorial+español)

---

## 🎯 Próximos Pasos

### Nivel Básico (Lo que ya sabes)
- ✅ Entender la estructura del proyecto
- ✅ Ejecutar pruebas existentes
- ✅ Crear pruebas simples

### Nivel Intermedio (Próximo objetivo)
- 🔄 Crear páginas más complejas
- 🔄 Implementar manejo de errores
- 🔄 Usar datos de prueba externos
- 🔄 Generar reportes

### Nivel Avanzado (Futuro)
- 🚀 Crear frameworks personalizados
- 🚀 Implementar CI/CD
- 🚀 Optimizar rendimiento
- 🚀 Crear librerías reutilizables

---

## 💡 Trucos y Consejos Útiles

### 1. **Atajos de Teclado Útiles**
- `Ctrl + C`: Detener la ejecución de pruebas
- `Ctrl + Shift + P` (VS Code): Comando palette
- `F5`: Ejecutar archivo actual

### 2. **Comandos Útiles**
```bash
# Ver qué pruebas existen
pytest --collect-only

# Ejecutar pruebas que contengan cierta palabra
pytest -k "login"

# Ejecutar pruebas que fallen
pytest --lf

# Ejecutar pruebas que pasaron la última vez
pytest --ff
```

### 3. **Variables de Entorno Útiles**
```bash
# Ejecutar en modo debug
PYTHONPATH=. pytest -v

# Ejecutar con navegador específico
BROWSER=firefox pytest

# Ejecutar en modo headless
HEADLESS=true pytest
```

---

## 🆘 ¿Necesitas Ayuda?

### 1. **Revisar Logs**
Los logs están en la carpeta `logs/`. Revisa el archivo más reciente para ver qué pasó.

### 2. **Revisar Screenshots**
Si una prueba falla, revisa la carpeta `screenshots/` para ver qué pasó.

### 3. **Usar Google**
La mayoría de errores ya tienen solución en Stack Overflow o GitHub.

### 4. **Preguntar en Comunidades**
- Stack Overflow
- Reddit r/learnpython
- Discord de Python
- Grupos de Facebook de programadores

---

## 🎉 ¡Felicidades!

Si llegaste hasta aquí, ya tienes una base sólida para trabajar con este framework de automatización. Recuerda:

1. **La práctica hace al maestro** - Ejecuta muchas pruebas
2. **No tengas miedo de experimentar** - Prueba cosas nuevas
3. **Aprende de los errores** - Cada fallo es una oportunidad de aprendizaje
4. **Pregunta cuando no sepas algo** - Es normal tener dudas

¡Buena suerte en tu viaje de automatización! 🚀

---

**Última actualización:** Enero 2025  
**Versión del framework:** 1.0  
**Autor:** Equipo de Automatización
