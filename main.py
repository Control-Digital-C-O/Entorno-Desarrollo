import os
import subprocess
import tempfile
import shutil
import sys
from pathlib import Path
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk


def verificar_url_repositorio(url):
    """Verifica si el URL del repositorio es válido usando git ls-remote."""
    try:
        subprocess.run(["git", "ls-remote", url],
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("URL no válido o no se pudo conectar al repositorio.")
        return False


def obtener_nombre_y_archivos_repositorio(url):
    """Clona el repositorio en una carpeta temporal y obtiene su nombre y archivos."""
    with tempfile.TemporaryDirectory() as temp_dir:
        subprocess.run(["git", "clone", "--depth",
                       "1", url, temp_dir], check=True)
        repo_name = Path(temp_dir).name
        archivos = [str(archivo.relative_to(temp_dir))
                    for archivo in Path(temp_dir).rglob('*') if archivo.is_file()]
        return repo_name, archivos


def seleccionar_carpeta_clonacion(default_dir):
    """Permite al usuario seleccionar la carpeta de clonación, usando la predeterminada o creando otra."""
    print(f"\nCarpeta de clonación predeterminada: {default_dir}")
    custom_dir = input(
        "¿Desea cambiar la carpeta de clonación? (s/n): ").strip().lower()

    if custom_dir == 's':
        user_dir = input("Ingrese la ruta de la carpeta deseada: ").strip()

        # Intentar crear la carpeta personalizada y manejar errores
        try:
            os.makedirs(user_dir, exist_ok=True)
            print(f"Carpeta de clonación configurada en: {user_dir}")
            return user_dir
        except PermissionError:
            print("Error: No tienes permisos para crear la carpeta en esa ubicación.")
            return None
        except OSError as e:
            print(
                f"Error: No se pudo crear la carpeta de clonación. Detalles: {e}")
            return None
    return default_dir


def clone_repository(repo_url, destination_folder, root):
    """Clona el repositorio dentro de su propia carpeta en la ubicación de destino."""
    repo_name = os.path.basename(repo_url).replace('.git', '')
    repo_path = os.path.join(destination_folder, repo_name)

    # Crear la carpeta de destino si no existe
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Ejecutar el comando de clonación de git
    try:
        process = subprocess.Popen(
            ["git", "clone", repo_url, repo_path],
            stdout=subprocess.PIPE,  # Capturar salida estándar
            stderr=subprocess.PIPE,  # Capturar salida de error
            text=True
        )

        # Procesar salida línea por línea
        for line in process.stdout:
            # Actualizar el log
            text_log.insert(tk.END, line)
            text_log.see(tk.END)  # Scroll automático

            # Simular progreso (esto es un ejemplo, git no da progreso directamente)
            progress["value"] += 5
            root.update_idletasks()

        process.wait()  # Esperar a que el proceso termine
        if process.returncode == 0:
            print(f"Repositorio clonado con éxito en: {repo_path}")
            # Listar archivos principales como vista previa
            show_file_preview(destination_folder)
            return repo_path  # Devuelve la ruta del repositorio clonado
        else:
            raise subprocess.CalledProcessError(
                process.returncode, process.args)
    except subprocess.CalledProcessError as e:
        text_log.insert(
            tk.END, f"Error al clonar el repositorio: {e.stderr}\n")
        text_log.see(tk.END)
        print(f"Error al clonar el repositorio: {e.stderr}")
        return None


def show_file_preview(folder_path):
    print("\nVista previa de archivos en el proyecto:")
    for root, dirs, files in os.walk(folder_path):
        # Mostrar solo los archivos principales (en la raíz y carpetas clave)
        if root == folder_path or os.path.basename(root) in ["src", "lib"]:
            for file in files:
                print("- ", os.path.relpath(os.path.join(root, file), folder_path))
    print("\nFinal de la vista previa de archivos.")


def detect_dependencies(project_folder):
    print("\n--- Detectando dependencias ---")
    dependencies = {}

    # Detectar Node.js (buscando package.json)
    package_json_path = os.path.join(project_folder, 'package.json')
    if os.path.exists(package_json_path):
        dependencies['Node.js'] = 'package.json'
        print("Archivo de configuración Node.js detectado (package.json).")

    # Detectar Python (buscando requirements.txt o Pipfile)
    requirements_txt_path = os.path.join(project_folder, 'requirements.txt')
    pipfile_path = os.path.join(project_folder, 'Pipfile')
    if os.path.exists(requirements_txt_path):
        dependencies['Python'] = 'requirements.txt'
        print("Archivo de configuración de Python detectado (requirements.txt).")
    elif os.path.exists(pipfile_path):
        dependencies['Python'] = 'Pipfile'
        print("Archivo de configuración de Python detectado (Pipfile).")

    # Detectar entorno virtual (venv)
    venv_path = os.path.join(project_folder, 'venv')
    if os.path.exists(venv_path):
        dependencies['Python virtual environment'] = 'venv'
        print("Entorno virtual detectado (venv).")

    # Mostrar resumen de las dependencias
    if dependencies:
        print("\n--- Resumen de dependencias detectadas ---")
        for dep, config_file in dependencies.items():
            print(f"{dep} (configurado en: {config_file})")
    else:
        print("No se detectaron dependencias específicas en el proyecto.")

    return dependencies


def install_dependency(dependency_name, install_command, manual_instructions):
    """Intenta instalar una dependencia automáticamente o da instrucciones para instalarla manualmente."""
    print(f"\nSe necesita instalar {dependency_name}.")
    choice = input(f"¿Quieres instalar {
                   dependency_name} automáticamente? (s/n): ").lower()

    if choice == 's':
        try:
            print(f"Instalando {dependency_name}...")
            subprocess.run(install_command, check=True)
            print(f"{dependency_name} se instaló correctamente.")
        except subprocess.CalledProcessError:
            print(f"Error: No se pudo instalar {
                  dependency_name} automáticamente.")
    else:
        print(f"Instrucciones para instalar {dependency_name} manualmente:")
        print(manual_instructions)


def install_required_dependencies(dependencies):
    """Verifica e instala automáticamente las dependencias detectadas en el sistema."""

    # Verificar si git está instalado
    if not shutil.which("git"):
        print("Error: Git no está instalado. Por favor, instala Git y vuelve a intentarlo.")
        return

    # Verificar Node.js y npm
    if 'Node.js' in dependencies:
        if not shutil.which("node") or not shutil.which("npm"):
            install_dependency(
                "Node.js y npm",
                ["npm", "install", "-g", "node"],
                "Visita https://nodejs.org para descargar e instalar Node.js y npm."
            )
        else:
            print("Node.js y npm ya están instalados.")

    # Verificar Python
    if 'Python' in dependencies:
        if not shutil.which("python3"):
            install_dependency(
                "Python",
                ["apt-get", "install", "python3"],
                "Instala Python desde https://www.python.org/ para obtener la versión adecuada."
            )
        if not shutil.which("pip"):
            install_dependency(
                "pip",
                ["python3", "-m", "ensurepip", "--upgrade"],
                "Instala pip con el comando 'python3 -m ensurepip --upgrade' o descarga desde https://pip.pypa.io."
            )

    # Instalar dependencias específicas de Node.js o Python en el proyecto
    project_requirements = {
        "Node.js": ("npm install", "Ejecuta 'npm install' en el directorio del proyecto."),
        "Python": ("pip install -r requirements.txt", "Ejecuta 'pip install -r requirements.txt' en el entorno virtual.")
    }

    for dep, (command, manual_instruction) in project_requirements.items():
        if dep in dependencies:
            print(f"\nPara completar la instalación de {dep}:")
            choice = input(f"¿Quieres ejecutar '{
                           command}' automáticamente? (s/n): ").lower()
            if choice == 's':
                subprocess.run(command, shell=True, check=False)
                print(f"{dep} se configuró correctamente.")
            else:
                print(f"Instrucción: {manual_instruction}")


def setup_python_virtualenv(project_folder):
    """Crea un entorno virtual dentro de la carpeta del proyecto clonado."""
    venv_path = os.path.join(project_folder, '.venv')
    if not os.path.exists(venv_path):
        print(f"Creando entorno virtual en: {venv_path}")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        print("Entorno virtual creado con éxito.")
    else:
        print("El entorno virtual ya existe.")

    # Activar el entorno virtual según el sistema operativo
    if os.name == 'nt':  # Windows
        activate_script = r"venv\Scripts\activate.bat"
    else:  # Unix/macOS
        activate_script = "source venv/bin/activate"

    print(f"Para activar el entorno virtual, ejecute: {activate_script}")


def setup_environment_variables():
    """Configura las variables de entorno desde un archivo .env si está presente."""
    if os.path.exists(".env"):
        print("Cargando variables de entorno desde el archivo .env...")
        load_dotenv(".env")
        print("Variables de entorno configuradas.")
    else:
        print("No se encontró un archivo .env. Puedes crear uno para definir variables de entorno.")


def install_python_dependencies():
    """Instala las dependencias de Python si requirements.txt está presente."""
    if os.path.exists("requirements.txt"):
        print("Se detectó requirements.txt. Instalando dependencias de Python...")
        subprocess.run(["venv/bin/pip", "install", "-r",
                       "requirements.txt"], check=True)
        print("Dependencias de Python instaladas correctamente.")
    else:
        print("No se detectó requirements.txt. Saltando instalación de dependencias de Python.")


def install_node_dependencies():
    """Instala las dependencias de Node.js si package.json está presente."""
    if os.path.exists("package.json"):
        print("Se detectó package.json. Instalando dependencias de Node.js...")
        subprocess.run(["npm", "install"], check=True)
        print("Dependencias de Node.js instaladas correctamente.")
    else:
        print(
            "No se detectó package.json. Saltando instalación de dependencias de Node.js.")


def gui_verificar_url():
    """GUI para verificar URL del repositorio."""
    url = entry_url.get().strip()
    if verificar_url_repositorio(url):
        messagebox.showinfo("Éxito", "El URL del repositorio es válido.")
    else:
        messagebox.showerror(
            "Error", "El URL del repositorio no es válido o no se pudo conectar.")


def gui_seleccionar_carpeta():
    """GUI para seleccionar carpeta de clonación."""
    folder = filedialog.askdirectory(title="Seleccionar carpeta de clonación")
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)
        messagebox.showinfo("Carpeta seleccionada",
                            f"Carpeta configurada: {folder}")
    else:
        messagebox.showerror("Error", "No se seleccionó ninguna carpeta.")


def gui_clonar_repositorio():
    """GUI para clonar el repositorio y crear el entorno virtual."""
    url = entry_url.get().strip()
    folder = entry_folder.get().strip()

    if not url or not folder:
        messagebox.showerror(
            "Error", "Debe proporcionar el URL del repositorio y la carpeta de destino.")
        return

    # Limpiar el listbox antes de la nueva clonación
    listbox_carpetas.delete(0, tk.END)

    # Clonar el repositorio
    repo_path = clone_repository(url, folder, root)
    if repo_path:
        messagebox.showinfo("Éxito", f"Repositorio clonado en {repo_path}")

        # Mostrar las primeras 10 carpetas en el listbox
        carpetas = mostrar_10_carpetas(repo_path)
        for carpeta in carpetas:
            listbox_carpetas.insert(tk.END, carpeta)

        # Crear entorno virtual
        setup_python_virtualenv(repo_path)
    else:
        messagebox.showerror("Error", "No se pudo clonar el repositorio.")


def gui_detectar_dependencias():
    """GUI para detectar dependencias."""
    folder = entry_folder.get().strip()
    if not folder:
        messagebox.showerror(
            "Error", "Debe proporcionar la carpeta del proyecto.")
        return
    dependencies = detect_dependencies(folder)
    if dependencies:
        messagebox.showinfo("Dependencias detectadas", "\n".join(
            [f"{k}: {v}" for k, v in dependencies.items()]))
    else:
        messagebox.showinfo("Sin dependencias",
                            "No se detectaron dependencias específicas.")


def mostrar_10_carpetas(folder_path):
    """Obtiene las primeras 10 carpetas del proyecto clonado."""
    carpetas = [f.name for f in Path(folder_path).iterdir() if f.is_dir()]
    return carpetas[:10]  # Retorna solo las primeras 10 carpetas


def main():
    """Interfaz gráfica principal."""
    global entry_url, entry_folder, listbox_carpetas, progress, text_log, root  # Referencias globales

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Asistente de Configuración de Entorno")

    # URL del repositorio
    tk.Label(root, text="URL del Repositorio:").grid(
        row=0, column=0, padx=10, pady=5, sticky="w")
    entry_url = tk.Entry(root, width=50)
    entry_url.grid(row=0, column=1, padx=10, pady=5)

    # Carpeta de clonación
    tk.Label(root, text="Carpeta de Clonación:").grid(
        row=1, column=0, padx=10, pady=5, sticky="w")
    entry_folder = tk.Entry(root, width=50)
    entry_folder.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Seleccionar...", command=gui_seleccionar_carpeta).grid(
        row=1, column=2, padx=10, pady=5)

    # Botones para las acciones
    tk.Button(root, text="Verificar URL", command=gui_verificar_url).grid(
        row=2, column=0, padx=10, pady=10)
    tk.Button(root, text="Clonar Repositorio", command=gui_clonar_repositorio).grid(
        row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Detectar Dependencias", command=gui_detectar_dependencias).grid(
        row=3, column=0, padx=10, pady=10)
    tk.Button(root, text="Salir", command=root.quit).grid(
        row=3, column=1, padx=10, pady=10)

    # Barra de progreso
    progress = ttk.Progressbar(
        root, orient="horizontal", length=300, mode="determinate")
    progress.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    # Log de clonación
    text_log = tk.Text(root, width=40, height=5)
    text_log.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    # Listbox para carpetas
    listbox_carpetas = tk.Listbox(root, width=40, height=15)
    listbox_carpetas.grid(row=0, column=3, rowspan=5, padx=10, pady=5)

    # Ejecutar el loop principal
    root.mainloop()


if __name__ == "__main__":
    main()
