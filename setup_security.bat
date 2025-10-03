@echo off
REM setup_security.bat
REM Script para configurar seguridad en Windows

echo ============================================
echo  CONFIGURACION DE SEGURIDAD - MYBEES PROJECT
echo ============================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "tests" (
    echo [ERROR] No se encuentra el directorio 'tests'
    echo Por favor ejecuta este script desde la raiz del proyecto
    pause
    exit /b 1
)

echo [Paso 1] Verificando .gitignore...
if exist ".gitignore" (
    echo [OK] .gitignore encontrado
) else (
    echo [ERROR] Por favor crea el archivo .gitignore primero
    pause
    exit /b 1
)
echo.

echo [Paso 2] Eliminando archivos de cache de Git...
git rm -r --cached __pycache__ 2>nul
git rm -r --cached **/__pycache__ 2>nul
git rm --cached **/*.pyc 2>nul
git rm --cached **/*.pyo 2>nul
echo [OK] Cache limpiado
echo.

echo [Paso 3] Eliminando logs de Git...
git rm -r --cached logs/ 2>nul
git rm --cached **/*.log 2>nul
echo [OK] Logs limpiados
echo.

echo [Paso 4] Configurando estructura de credenciales...
if not exist "config" mkdir config
type nul > config\__init__.py
echo [OK] Directorio config verificado

if not exist "config\credentials.py" (
    if exist "config\credentials_template.py" (
        echo [INFO] Creando config\credentials.py desde template...
        copy config\credentials_template.py config\credentials.py
        echo [OK] config\credentials.py creado
        echo [IMPORTANTE] Edita config\credentials.py con tus credenciales reales
    ) else (
        echo [ADVERTENCIA] credentials_template.py no encontrado
    )
) else (
    echo [OK] config\credentials.py ya existe
)
echo.

echo [Paso 5] Verificando que credentials.py NO este en Git...
git ls-files --error-unmatch config\credentials.py >nul 2>&1
if %errorlevel% == 0 (
    echo [ALERTA] config\credentials.py esta versionado en Git!
    echo Removiendo del repositorio...
    git rm --cached config\credentials.py
    echo [OK] Removido de Git
) else (
    echo [OK] config\credentials.py NO esta en Git
)
echo.

echo [Paso 6] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "screenshots" mkdir screenshots
echo [OK] Directorios creados
echo.

echo [Paso 7] Creando .gitkeep...
type nul > logs\.gitkeep
git add logs\.gitkeep 2>nul
echo [OK] .gitkeep creado
echo.

echo ============================================
echo  RESUMEN DE CAMBIOS
echo ============================================
echo.
git status --short
echo.

echo ============================================
echo  CONFIGURACION COMPLETADA
echo ============================================
echo.
echo PROXIMOS PASOS:
echo.
echo 1. Edita tus credenciales:
echo    notepad config\credentials.py
echo.
echo 2. Verifica los cambios:
echo    git status
echo.
echo 3. Haz commit:
echo    git add .gitignore config\__init__.py config\credentials_template.py
echo    git commit -m "Add security: .gitignore and credentials management"
echo.
echo [IMPORTANTE] Nunca hagas 'git add config\credentials.py'
echo.
pause