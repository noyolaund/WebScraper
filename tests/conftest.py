# tests/conftest.py
import pytest
import sys
import os
from selenium import webdriver

# Modern Selenium 4.6+ approach: Selenium Manager handles drivers automatically
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Agregar el directorio padre al path para importar la configuración
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    # Importar configuración de logging
    from config.logging_config import setup_logging, get_logger

    # Configurar logging al inicio de la sesión de pruebas
    logger = setup_logging()
    LOGGING_AVAILABLE = True
except ImportError as e:
    print(f"Warning: No se pudo importar logging config: {e}")
    print("Continuando sin logging avanzado...")
    LOGGING_AVAILABLE = False

    # Fallback a logging básico
    import logging

    logging.basicConfig(level=logging.INFO)


    def get_logger(name):
        return logging.getLogger(name)


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Send 'chrome' or 'firefox' as parameter for execution"
    )


def pytest_configure(config):
    """Configuración que se ejecuta antes de todas las pruebas"""
    if LOGGING_AVAILABLE:
        logger = get_logger("pytest_session")
        logger.info("=" * 80)
        logger.info("INICIANDO SESIÓN DE PRUEBAS - MYBEES AUTOMATION")
        logger.info("=" * 80)
        browser = config.getoption("--browser")
        logger.info(f"Browser seleccionado: {browser}")


def pytest_sessionfinish(session, exitstatus):
    """Se ejecuta al finalizar todas las pruebas"""
    if LOGGING_AVAILABLE:
        logger = get_logger("pytest_session")
        logger.info("=" * 80)
        logger.info(f"SESIÓN DE PRUEBAS FINALIZADA - Exit status: {exitstatus}")
        logger.info("=" * 80)


@pytest.fixture()
def driver(request):
    browser = request.config.getoption("--browser")
    # Default driver value
    driver = ""

    # Setup
    if LOGGING_AVAILABLE:
        logger = get_logger("driver_fixture")
        logger.info(f"Setting up: {browser} driver")
    else:
        print(f"\nSetting up: {browser} driver")
        logger = get_logger("driver")

    if browser == "chrome":
        # Chrome options setup for headless mode
        chrome_options = ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1820,980')

        # ✅ Enable BiDi for accessibility locators
        chrome_options.set_capability("webSocketUrl", True)

        # Modern approach: Use Selenium Manager (no webdriver-manager needed)
        driver = webdriver.Chrome(options=chrome_options)

        if LOGGING_AVAILABLE:
            logger.info("Chrome driver configurado exitosamente")

    # Implicit wait setup for our framework
    driver.implicitly_wait(5)
    yield driver

    # Tear down
    if LOGGING_AVAILABLE:
        logger.info(f"Tear down: {browser} driver")
    else:
        print(f"\nTear down: {browser} driver")
    driver.quit()


@pytest.fixture()
def test_logger(request):
    """Fixture que proporciona un logger específico para cada test"""
    if LOGGING_AVAILABLE:
        test_name = request.node.name
        logger = get_logger(f"test.{test_name}")
        logger.info(f"Iniciando test: {test_name}")
        yield logger
        logger.info(f"Test finalizado: {test_name}")
    else:
        yield get_logger("test")


# Hooks para logging automático (solo si logging está disponible)
if LOGGING_AVAILABLE:
    def pytest_runtest_setup(item):
        """Se ejecuta antes de cada test"""
        logger = get_logger("pytest_hooks")
        logger.info(f"PREPARANDO: {item.name}")


    def pytest_runtest_call(item):
        """Se ejecuta durante la ejecución del test"""
        logger = get_logger("pytest_hooks")
        logger.info(f"EJECUTANDO: {item.name}")


    def pytest_runtest_teardown(item):
        """Se ejecuta después de cada test"""
        logger = get_logger("pytest_hooks")
        logger.info(f"LIMPIEZA: {item.name}")


    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        """Hook para capturar el resultado de cada test"""
        outcome = yield
        result = outcome.get_result()

        logger = get_logger("test_results")

        if call.when == "call":
            if result.outcome == "passed":
                logger.info(f"PASÓ: {item.name}")
            elif result.outcome == "failed":
                logger.error(f"FALLÓ: {item.name}")
                if result.longrepr:
                    # Log solo la línea principal del error, no todo el traceback
                    error_lines = str(result.longrepr).split('\n')
                    for line in error_lines[-3:]:  # Últimas 3 líneas del error
                        if line.strip():
                            logger.error(f"   {line.strip()}")
            elif result.outcome == "skipped":
                logger.warning(f"OMITIDO: {item.name}")