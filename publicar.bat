@echo off
chcp 65001 >nul
cls
title Telegram Justi - Publicar en GitHub

:: ============================================================
:: Leer version desde buildVars.py automaticamente
:: ============================================================
set VERSION=1.0.0
for /f "tokens=2 delims==" %%A in ('findstr /C:"addon_version=" buildVars.py 2^>nul') do (
    set "RAW=%%A"
)
if defined RAW (
    set "RAW=%RAW:"=%"
    for /f "tokens=1 delims=," %%B in ("%RAW%") do set "VERSION=%%B"
)

echo ============================================================
echo   Telegram Justi - Script de publicacion en GitHub
echo ============================================================
echo.
set REPO_URL=https://github.com/JustiCode/Telegram-Justi-v1.0---Lanzamiento-Disruptivo-para-Versiones-Unigram-y-Desktop-.git
set BRANCH=main
echo  Version: %VERSION%
echo  Repositorio: %REPO_URL%
echo  Rama: %BRANCH%
echo.
echo  Que deseas hacer?
echo.
echo  [1] Subida completa (limpiar, commit, push y crear tag/release)
echo  [2] Solo commit y push (sin tag)
echo  [3] Solo crear tag y push del tag
echo  [4] Inicializar repositorio (primera vez)
echo  [5] Compilar complemento localmente (scons)
echo  [6] Generar plantilla de traduccion (.pot)
echo  [7] Instalar dependencias (scons + markdown)
echo  [8] Salir
echo.
set /p OPCION="  Elige una opcion (1-8): "
if "%OPCION%"=="1" goto FULL
if "%OPCION%"=="2" goto PUSH_ONLY
if "%OPCION%"=="3" goto TAG_ONLY
if "%OPCION%"=="4" goto INIT
if "%OPCION%"=="5" goto BUILD
if "%OPCION%"=="6" goto POT
if "%OPCION%"=="7" goto DEPS
if "%OPCION%"=="8" goto END
echo  Opcion no valida.
goto END

:: ============================================================
:: Verificar que git esta instalado
:: ============================================================
:CHECK_GIT
where git >nul 2>nul
if errorlevel 1 (
    echo.
    echo  ERROR: Git no esta instalado o no esta en el PATH.
    echo  Descargalo desde: https://git-scm.com/downloads
    goto END
)
goto :eof

:: ============================================================
:: Verificar que scons esta instalado
:: ============================================================
:CHECK_SCONS
where scons >nul 2>nul
if errorlevel 1 (
    echo.
    echo  AVISO: SCons no esta instalado.
    echo.
    set /p INST_SCONS="  Deseas instalarlo ahora? (S/N): "
    if /i "%INST_SCONS%"=="S" (
        echo.
        echo --- Instalando SCons y Markdown ---
        pip install scons markdown
        echo.
        echo  Dependencias instaladas correctamente.
    ) else (
        echo  Abortado. Instala SCons manualmente con: pip install scons
        goto END
    )
)
goto :eof

:: ============================================================
:: Opcion 4: Inicializar repositorio
:: ============================================================
:INIT
call :CHECK_GIT
echo.
echo --- Inicializando repositorio ---
if exist ".git" (
echo  Ya existe un repositorio git en este directorio.
echo  Si deseas reinicializarlo, elimina la carpeta .git manualmente.
goto END
)
git init
git remote add origin %REPO_URL%
git branch -M %BRANCH%
echo.
echo  Repositorio inicializado correctamente.
echo  Ahora puedes usar la opcion [1] para subir el codigo.
goto END

:: ============================================================
:: Opcion 1: Subida completa
:: ============================================================
:FULL
call :CHECK_GIT
echo.
echo --- Limpiando artefactos de compilacion ---
if exist ".sconsign.dblite" del /q ".sconsign.dblite"
for %%F in (*.nvda-addon) do del /q "%%F"
for %%F in (*.pot) do del /q "%%F"
echo.
set /p MSG="  Mensaje del commit (Enter para usar 'Version %VERSION%'): "
if "%MSG%"=="" set MSG=Version %VERSION%
echo.
echo --- Agregando cambios ---
git add --all
echo --- Creando commit ---
git commit -m "%MSG%"
echo --- Subiendo a %BRANCH% ---
git push -u origin %BRANCH%
echo --- Creando tag %VERSION% ---
git tag %VERSION%
echo --- Subiendo tags ---
git push --tags
echo.
echo  Publicacion completa! El workflow de GitHub Actions generara
echo  el complemento .nvda-addon automaticamente y creara el release.
goto END

:: ============================================================
:: Opcion 2: Solo commit y push
:: ============================================================
:PUSH_ONLY
call :CHECK_GIT
echo.
set /p MSG="  Mensaje del commit (Enter para usar 'Actualizacion'): "
if "%MSG%"=="" set MSG=Actualizacion
echo.
echo --- Agregando cambios ---
git add --all
echo --- Creando commit ---
git commit -m "%MSG%"
echo --- Subiendo a %BRANCH% ---
git push -u origin %BRANCH%
echo.
echo  Push completado. No se ha creado tag ni release.
goto END

:: ============================================================
:: Opcion 3: Solo crear tag
:: ============================================================
:TAG_ONLY
call :CHECK_GIT
echo.
echo --- Creando tag %VERSION% ---
git tag %VERSION%
echo --- Subiendo tags ---
git push --tags
echo.
echo  Tag %VERSION% creado y subido.
echo  El workflow de GitHub creara el release automaticamente.
goto END

:: ============================================================
:: Opcion 5: Compilar complemento
:: ============================================================
:BUILD
call :CHECK_SCONS
echo.
echo --- Compilando complemento localmente ---
scons --clean
echo.
scons
echo.
echo  Compilacion completada.
for %%F in (*.nvda-addon) do echo  Archivo generado: %%F
goto END

:: ============================================================
:: Opcion 6: Generar plantilla de traduccion
:: ============================================================
:POT
call :CHECK_SCONS
echo.
echo --- Generando plantilla de traduccion (.pot) ---
scons pot
echo.
echo  Plantilla de traduccion generada.
for %%F in (*.pot) do echo  Archivo generado: %%F
goto END

:: ============================================================
:: Opcion 7: Instalar dependencias
:: ============================================================
:DEPS
echo.
echo --- Verificando Python ---
where python >nul 2>nul
if errorlevel 1 (
    echo  ERROR: Python no esta instalado o no esta en el PATH.
    echo  Descargalo desde: https://www.python.org/downloads/
    goto END
)
echo  Python encontrado.
echo.
echo --- Verificando pip ---
python -m pip --version >nul 2>nul
if errorlevel 1 (
    echo  ERROR: pip no esta disponible.
    echo  Reinstala Python asegurandote de marcar "Add to PATH".
    goto END
)
echo  pip encontrado.
echo.
echo --- Verificando SCons ---
where scons >nul 2>nul
if errorlevel 1 (
    echo  SCons NO esta instalado. Instalando...
    pip install scons
    echo  SCons instalado correctamente.
) else (
    echo  SCons ya esta instalado.
)
echo.
echo --- Verificando Markdown ---
python -c "import markdown" >nul 2>nul
if errorlevel 1 (
    echo  Markdown NO esta instalado. Instalando...
    pip install markdown
    echo  Markdown instalado correctamente.
) else (
    echo  Markdown ya esta instalado.
)
echo.
echo --- Verificando Git ---
where git >nul 2>nul
if errorlevel 1 (
    echo  AVISO: Git NO esta instalado.
    echo  Descargalo desde: https://git-scm.com/downloads
    echo  Git es necesario para las opciones de commit/push/tag.
) else (
    echo  Git ya esta instalado.
)
echo.
echo --- Verificando GNU Gettext ---
where msgfmt >nul 2>nul
if errorlevel 1 (
    echo  AVISO: GNU Gettext (msgfmt) NO esta instalado.
    echo  Es necesario para compilar archivos de traduccion (.po a .mo).
    echo  Descargalo desde: https://gnuwin32.sourceforge.net/downlinks/gettext.php
    echo  O usa GitHub Actions para compilar (no necesita gettext local).
) else (
    echo  GNU Gettext ya esta instalado.
)
echo.
echo ============================================================
echo  Verificacion de dependencias completada.
echo ============================================================
goto END

:: ============================================================
:: Fin
:: ============================================================
:END
echo.
echo ============================================================
echo  Proceso finalizado.
echo ============================================================
pause
