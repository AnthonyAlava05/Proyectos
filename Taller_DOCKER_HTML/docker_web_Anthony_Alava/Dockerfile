# Usar una imagen base ligera de Python
FROM python:3.9-slim
# Configurar el directorio de trabajo en el contenedor
WORKDIR /app
# Copiar los archivos al contenedor
COPY app.py tabla.html /app/
# Instalar Flask
RUN pip install flask
# Exponer el puerto en el que la aplicación correrá
EXPOSE 8080
# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
