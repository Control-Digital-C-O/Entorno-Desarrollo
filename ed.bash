#!/bin/bash

# Pedir al usuario la URL del repositorio
read -p "Introduce la URL del repositorio (por ejemplo: https://github.com/usuario/nombre-del-repositorio.git): " REPO_URL

# Validar que la URL sea del formato correcto
if [[ ! "$REPO_URL" =~ ^https://github\.com/.+\.git$ ]]; then
    echo "La URL ingresada no es válida. Asegúrate de que sea una URL válida de GitHub."
    exit 1
fi

# Extraer el nombre del repositorio desde la URL
PROJECT_DIR=$(basename -s .git $REPO_URL)

# Mostrar el nombre del repositorio y pedir confirmación
echo "El nombre del repositorio es: $PROJECT_DIR"
read -p "¿Es este el repositorio correcto? (s/n): " confirmacion

if [[ "$confirmacion" != "s" && "$confirmacion" != "S" ]]; then
    echo "Por favor, verifica la URL e inténtalo nuevamente."
    exit 1
fi

# 1. Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python no está instalado. Por favor instálalo y vuelve a ejecutar el script."
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
        exit 1
    fi
fi

# Confirmación de que pip está instalado
if ! command -v pip &> /dev/null; then
    echo "Error: pip no se pudo instalar. Revisa el sistema e intenta instalarlo manualmente."
    exit 1
fi

# 3. Verificar si npm está instalado
if ! command -v npm &> /dev/null; then
    echo "npm no está instalado. Por favor instala Node.js y npm y vuelve a ejecutar el script."
    exit 1
fi

# 4. Clonar el repositorio
echo "Clonando el repositorio desde $REPO_URL..."
git clone $REPO_URL $PROJECT_DIR
cd $PROJECT_DIR || { echo "Error: no se pudo acceder a la carpeta del proyecto"; exit 1; }

# 5. Crear y activar el entorno virtual
echo "Creando el entorno virtual en venv..."
python3 -m venv venv

# Activar el entorno virtual según el sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate  # Para Linux/MacOS
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate  # Para Windows
else
    echo "Sistema operativo no soportado para la activación del entorno virtual."
    exit 1
fi

# 6. Instalar las dependencias de Python
echo "Instalando las dependencias de Python..."
pip install -r requirements.txt

# 7. Instalar dependencias de Node.js
echo "Instalando dependencias de Node.js con npm..."
npm install

# 8. Instalar concurrently para ejecutar múltiples servidores
echo "Instalando concurrently..."
npm install concurrently --save-dev

# Desactivar el entorno virtual
deactivate

echo "El entorno de desarrollo está listo."
