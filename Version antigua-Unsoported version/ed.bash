#!/bin/bash

# Pedir al usuario la URL del repositorio
read -p "Introduce la URL del repositorio (por ejemplo: https://github.com/usuario/nombre-del-repositorio.git): " REPO_URL
echo " "
# Validar que la URL sea del formato correcto
if [[ ! "$REPO_URL" =~ ^https://github\.com/.+\.git$ ]]; then
    echo "La URL ingresada no es válida. Asegúrate de que sea una URL válida de GitHub."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# Extraer el nombre del repositorio desde la URL
PROJECT_DIR=$(basename -s .git $REPO_URL)

# Mostrar el nombre del repositorio y pedir confirmación
echo "El nombre del repositorio es: $PROJECT_DIR"
read -p "¿Es este el repositorio correcto? (s/n): " confirmacion
echo " "
if [[ "$confirmacion" != "s" && "$confirmacion" != "S" ]]; then
    echo "Por favor, verifica la URL e inténtalo nuevamente."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# 1. Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python no está instalado. Por favor instálalo y vuelve a ejecutar el script."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# 2. Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Intentando instalar pip..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update
        sudo apt install -y python3-pip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python get-pip.py
        del get-pip.py
    else
        echo "Sistema operativo no soportado para la instalación automática de pip."
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    fi
fi

# Confirmación de que pip está instalado
if ! command -v pip &> /dev/null; then
    echo "Error: pip no se pudo instalar. Revisa el sistema e intenta instalarlo manualmente."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# 3. Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "npm no está instalado. Por favor instala Node.js y npm y vuelve a ejecutar el script."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# 4. Clonar el repositorio
echo "Clonando el repositorio desde $REPO_URL..."
git clone $REPO_URL $PROJECT_DIR
cd $PROJECT_DIR || { echo "Error: no se pudo acceder a la carpeta del proyecto"; exit 1; }
echo " "
# 5. Crear y activar el entorno virtual

# Verificar si ensurepip está disponible (para crear el entorno con pip)
if ! python3 -m ensurepip --help > /dev/null 2>&1; then
    echo "El módulo 'ensurepip' no está disponible. Intentando instalar ensurepip..."
    if [ "$OS" = "Linux" ]; then
        sudo apt install -y python3-ensurepip
    elif [ "$OS" = "Windows_NT" ]; then
        echo "Instala manualmente ensurepip en Windows."
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    fi
fi

# Verifica si el módulo venv está disponible en Python
if ! python3 -m venv --help &>/dev/null && ! python -m venv --help &>/dev/null; then
    echo "El módulo 'venv' no está instalado. Instalando ahora..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        echo "Instalar el venv manualmente"
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Para macOS
        brew install python3
        echo "Instalar el venv manualmente"
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* ]]; then
        # Para Windows (en Git Bash o Cygwin)
        echo "Instala Python 3 manualmente en Windows y asegúrate de agregarlo a PATH."
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    else
        echo "Sistema operativo no soportado. Por favor instala 'venv' manualmente."
        read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
        exit 1
    fi
fi

# Crear el entorno virtual en la carpeta venv
if [[ -d "venv" ]]; then
    echo "El entorno virtual ya existe, omitiendo creación."
else
    python3 -m venv venv || python -m venv venv
    echo "Entorno virtual creado en la carpeta 'venv'."
fi
echo " "
# Activar el entorno virtual según el sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate  # Para Linux/MacOS
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* || "$OSTYPE" == "cygwin"* ]]; then
    source venv/Scripts/activate  # Para Windows
else
    echo "Sistema operativo no soportado para la activación del entorno virtual."
    read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
    exit 1
fi

# 6. Instalar las dependencias de Python
echo "Instalando las dependencias de Python..."
pip install -r requirements.txt
echo " "
# 7. Instalar dependencias de Node.js
echo "Instalando dependencias de Node.js con npm..."
npm install
echo " "
# 8. Instalar concurrently para ejecutar múltiples servidores
echo "Instalando concurrently..."
npm install concurrently --save-dev
echo " "
# Desactivar el entorno virtual
deactivate
echo " "
echo "El entorno de desarrollo está listo."
echo "Todo finalizó correctamente."

read -n 1 -s -r -p "Presione cualquier tecla para finalizar..."
