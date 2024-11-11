# Entorno de Desarrollo

Este es un script completamente configurable diseñado para automatizar la configuración de un entorno de desarrollo. Su objetivo es ofrecer una solución sencilla, similar a Docker, pero sin la complejidad que implica configurar y manejar contenedores. Con este script, podrás crear un entorno aislado en tu máquina, utilizando una carpeta `venv` para almacenar todas las dependencias de tu repositorio personal. Es compatible con sistemas operativos **Windows** y **Linux**.

## Consideraciones Importantes

Los requisitos básicos para ejecutar este script son: **Python**, **npm**, y **pip** (pip se instalará automáticamente si no está presente).

Este script ha sido diseñado para ser lo más general posible, pero ha sido adaptado específicamente a mi proyecto **MasterPath**. En este proyecto, automatizo la instalación de todas las dependencias necesarias para que el entorno de desarrollo funcione correctamente. Si deseas usar este script para configurar tu propio entorno de desarrollo y no necesitas las dependencias específicas de mi proyecto, puedes modificar el archivo `ed.bash` según tus necesidades. Para ello, sigue estos pasos:

1. **Edita el archivo `ed.bash`** de acuerdo a tus requerimientos.
2. En el mismo directorio donde se encuentra el archivo, ejecuta el siguiente comando para hacerlo ejecutable:

   ```bash
   chmod +x ed.bash

Este comando le otorgará permisos de ejecución al archivo, permitiendo que sea reconocido como un script ejecutable por tu sistema.

Si no deseas modificar el archivo manualmente, también puedes descargar el release del repositorio y colocar el URL del repositorio que deseas clonar. El script se encargará de clonar el repositorio y de instalar automáticamente las dependencias necesarias.

## Instrucciones de Ejecución

1. **Clonar el Repositorio:**
Primero, necesitas clonar el repositorio que contiene el archivo ed.bash. Puedes hacerlo ejecutando el siguiente comando en tu terminal o descargarndo el archivo ejecutable del release:

   ```bash
   git clone <https://github.com/Maty1534/Entorno-Desarrollo.git>
   ```

2. **Hacer Ejecutable el Script:**
En el directorio donde se encuentra el archivo ed.bash, ejecuta el siguiente comando para darle permisos de ejecución:

   ```bash
   chmod +x ed.bash
   ```

3. **Ejecutar el Script:**
Una vez que el archivo es ejecutable, simplemente ejecútalo con:

   ```bash
   ./ed.bash
   ```

Esto iniciará el proceso de configuración del entorno de desarrollo. El script realizará los siguientes pasos automáticamente:

- Verificará si tienes Python, npm y pip instalados. Si no están presentes, se instalarán.
- Creará un entorno virtual (venv) para aislar las dependencias.
- Clonará el repositorio especificado y descargará las dependencias necesarias.
- Instalación de las dependencias de npm y pip.
- Configurará y ejecutará los servidores necesarios (Flask y Parcel) para tu entorno de desarrollo.

## Curiosidades del Proyecto MasterPath

**MasterPath** es un proyecto basado en **Flask** para el **frontend**, pero optimizado con **Parcel**, un bundler que mejora el rendimiento de la aplicación web. Gracias a Parcel, se logra una carga más rápida de los archivos y un desarrollo más eficiente, ya que facilita la ejecución modular de las APIs en archivos JavaScript. Esto permite una estructura más limpia y optimizada del proyecto, a la vez que minimiza los errores y facilita la depuración.

Al trabajar con Parcel, se ejecutan dos servidores durante el desarrollo: uno para **Flask** y otro para **Parcel**, permitiendo que las modificaciones en el código sean reflejadas al instante. Aunque pueden surgir errores ocasionales debido a conflictos con otras dependencias, el uso de un entorno virtual (**venv**) ayuda a aislar estas dependencias, evitando que interfieran con el sistema o con otros proyectos. De esta manera, las dependencias del proyecto quedan completamente encapsuladas, asegurando que el entorno de desarrollo sea limpio y controlado.
