# tests/test_offers.py
import sys
import os
import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

# Agregar el directorio padre al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ===== IMPORTAR LOGGING =====
try:
    from config.logging_config import get_logger

    LOGGING_AVAILABLE = True
except ImportError:
    import logging


    def get_logger(name):
        return logging.getLogger(name)


    LOGGING_AVAILABLE = False

# ===== IMPORTAR CREDENCIALES DE FORMA SEGURA =====
try:
    # Intentar importar desde archivo de credenciales
    from config.credentials import (
        MYBEES_EMAIL,
        MYBEES_PASSWORD,
        MYBEES_URL
    )

    logger = get_logger(__name__)
    logger.info("Credenciales cargadas desde config/credentials.py")

except ImportError:
    # Fallback: Intentar obtener desde variables de entorno
    logger = get_logger(__name__)
    logger.warning("No se encontró config/credentials.py, intentando variables de entorno...")

    MYBEES_EMAIL = os.getenv('MYBEES_EMAIL')
    MYBEES_PASSWORD = os.getenv('MYBEES_PASSWORD')
    MYBEES_URL = os.getenv('MYBEES_URL', 'https://mybees.mx')

    if not MYBEES_EMAIL or not MYBEES_PASSWORD:
        error_msg = """
        ERROR: Credenciales no encontradas!

        Por favor, realiza una de estas opciones:

        OPCIÓN 1 (Recomendada):
        1. Copia el template: cp config/credentials_template.py config/credentials.py
        2. Edita config/credentials.py con tus credenciales reales

        OPCIÓN 2:
        Define variables de entorno:
        - Linux/Mac: export MYBEES_EMAIL="tu@email.com" && export MYBEES_PASSWORD="tupassword"
        - Windows: set MYBEES_EMAIL=tu@email.com && set MYBEES_PASSWORD=tupassword
        """
        logger.error(error_msg)
        raise Exception(error_msg)
    else:
        logger.info("Credenciales cargadas desde variables de entorno")


def close_pop_up_window(driver):
    """Función helper global para cerrar ventanas popup"""
    logger = get_logger("popup_handler")

    try:
        popup_window = driver.find_element(By.XPATH,
                                           "//*[@id='header-section']/button[1]/div[1]/svg[1]/g[1]/g[1]/path[1]")
        popup_window.click()
        logger.info("Popup window closed")
        time.sleep(2)
    except NoSuchElementException:
        logger.info("Popup window not found (esto es normal)")
    except Exception as e:
        logger.warning(f"Error cerrando popup: {str(e)}")


class TestOffers:
    """Tests para ofertas en MyBees - CON CREDENCIALES SEGURAS"""

    def test_offers(self, driver, test_logger=None):
        """TEST PRINCIPAL DE OFERTAS - USANDO CREDENCIALES SEGURAS"""

        # Usar test_logger si está disponible
        if test_logger and LOGGING_AVAILABLE:
            logger = test_logger
            logger.info("INICIANDO TEST DE OFERTAS - MYBEES")
        else:
            logger = get_logger(__name__)
            logger.info("Starting automation...")

        try:
            # Navegar a MyBees usando URL de configuración
            logger.info(f"Navegando a {MYBEES_URL}")
            driver.get(MYBEES_URL)
            logger.info("Página MyBees cargada")
            time.sleep(2)

            """ 
            # Código original comentado para cookies
            cookie_accept = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
            cookie_accept.click()
            time.sleep(2) 
            """

            actual_url = driver.current_url
            logger.info(f"Current URL: {actual_url}")

            # LOGIN - USANDO CREDENCIALES SEGURAS
            logger.info("Buscando botón de login...")
            login_button = driver.find_element(By.NAME, "guest_homepage_login_button")
            login_button.click()
            logger.info("Login button clicked")
            time.sleep(3)

            # CREDENCIALES DESDE CONFIGURACIÓN (NO HARDCODEADAS)
            logger.info(f"Ingresando email: {MYBEES_EMAIL}")
            email = driver.find_element(By.ID, "signInName")
            email.send_keys(MYBEES_EMAIL)  # Credencial segura
            logger.info("Email ingresado")

            logger.info("Ingresando password...")
            password = driver.find_element(By.ID, "password")
            password.send_keys(MYBEES_PASSWORD)  # Credencial segura
            logger.info("Password ingresado")

            time.sleep(2)
            password.send_keys(Keys.ENTER)
            logger.info("Formulario enviado")

            time.sleep(5)
            logger.info("Login completado")

            # Cerrar popup
            logger.info("Verificando popups...")
            close_pop_up_window(driver)

            # Navegar a ofertas
            logger.info("Navegando a ofertas...")
            offers_button = driver.find_element(By.XPATH,
                                                "//*[@id='menu']/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/h2[1]/a[1]")
            offers_button.click()
            logger.info("Offers button clicked")
            time.sleep(2)

            # Verificación de URL
            actual_url = driver.current_url
            expected_url = "https://mybees.mx/discounts#combos"
            logger.info(f"Verificando URL")
            logger.info(f"   Actual: {actual_url}")
            logger.info(f"   Esperada: {expected_url}")

            assert actual_url == expected_url, f"URL no coincide: {actual_url}"
            logger.info("URL verificada correctamente")

            # Obtener productos
            logger.info("Obteniendo productos...")
            names = driver.find_elements(By.CSS_SELECTOR, "span.bees-text.bees-product-card-title")

            if names:
                logger.info(f"Se encontraron {len(names)} productos en ofertas:")
                for index, name in enumerate(names):
                    product_name = name.text.strip()
                    logger.info(f"  {index + 1}. {product_name}")
                    # Mantener línea original para compatibilidad
                    print(f"{index}: {name.text}")
            else:
                logger.warning("No se encontraron productos")

            time.sleep(3)
            logger.info("Test completado exitosamente!")

        except Exception as e:
            logger.error(f"TEST FAILED: {str(e)}")

            # Screenshot automático en errores
            try:
                timestamp = int(time.time())
                screenshot_name = f"error_test_offers_{timestamp}.png"

                logs_dir = "logs"
                os.makedirs(logs_dir, exist_ok=True)

                screenshot_path = os.path.join(logs_dir, screenshot_name)
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot guardado: {screenshot_name}")
            except Exception as screenshot_error:
                logger.warning(f"No se pudo guardar screenshot: {screenshot_error}")

            raise


# Logger global para compatibilidad
logger = get_logger(__name__)