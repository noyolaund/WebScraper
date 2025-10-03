# config/credentials_template.py
"""
TEMPLATE DE CREDENCIALES
========================
Este archivo SÍ se versiona en Git como ejemplo.

INSTRUCCIONES DE USO:
1. Copia este archivo como 'credentials.py' en el mismo directorio
2. Edita 'credentials.py' con tus credenciales reales
3. NUNCA versiones 'credentials.py' (está en .gitignore)

Comando para copiar:
    cp config/credentials_template.py config/credentials.py

Luego edita config/credentials.py con tus datos reales.
"""

# ===== CREDENCIALES MYBEES =====
# Reemplaza con tus credenciales reales en credentials.py
MYBEES_EMAIL = "tu_email@ejemplo.com"
MYBEES_PASSWORD = "tu_password_aqui"

# ===== URLS DEL AMBIENTE =====
# Puedes tener diferentes ambientes
MYBEES_URL_PROD = "https://mybees.mx"
MYBEES_URL_DEV = "https://dev.mybees.mx"  # Si existe
MYBEES_URL_STAGING = "https://staging.mybees.mx"  # Si existe

# Ambiente por defecto
MYBEES_URL = MYBEES_URL_PROD

# ===== OTRAS CONFIGURACIONES =====
# Timeouts (en segundos)
DEFAULT_TIMEOUT = 10
PAGE_LOAD_TIMEOUT = 30

# Browser config
DEFAULT_BROWSER = "chrome"
HEADLESS_MODE = False  # True para ejecutar sin ventana

# ===== NOTAS DE SEGURIDAD =====
# Para mayor seguridad, considera usar variables de entorno:
#
# import os
# MYBEES_EMAIL = os.getenv('MYBEES_EMAIL', 'default@email.com')
# MYBEES_PASSWORD = os.getenv('MYBEES_PASSWORD', 'default_password')
#
# Y definirlas en tu sistema:
# export MYBEES_EMAIL="tu_email@ejemplo.com"
# export MYBEES_PASSWORD="tu_password"