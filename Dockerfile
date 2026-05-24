# Usa una imagen oficial liviana de Python 3.12 como base del contenedor.
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc dentro del contenedor.
ENV PYTHONDONTWRITEBYTECODE=1
# Hace que los mensajes de Python salgan inmediatamente en consola.
ENV PYTHONUNBUFFERED=1
# Permite importar modulos que estan dentro de /proyecto/app.
ENV PYTHONPATH=/proyecto/app

# Define /proyecto como carpeta de trabajo dentro del contenedor.
WORKDIR /proyecto

# Instala librerias del sistema necesarias para que matplotlib pueda generar imagenes.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libfreetype6 fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Copia primero el archivo de dependencias para aprovechar cache de Docker.
COPY requirements.txt .
# Instala las librerias de Python indicadas en requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copia la carpeta principal de codigo de la aplicacion.
COPY app ./app
# Copia la carpeta de salidas para que exista dentro de la imagen.
COPY outputs ./outputs
# Copia el README dentro del contenedor como documentacion del proyecto.
COPY README.md .

# Expone el puerto 8000, que es donde corre la interfaz web.
EXPOSE 8000

# Ejecuta la aplicacion web con Waitress, un servidor WSGI mas adecuado para Docker.
CMD ["waitress-serve", "--host=0.0.0.0", "--port=8000", "web:aplicacion"]
