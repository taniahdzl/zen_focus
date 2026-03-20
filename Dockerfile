# 1. Imagen base oficial de Python
FROM python:3.11-slim

# 2. Evitar que Python genere archivos .pyc y use buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar archivos de configuración e instalar dependencias
COPY pyproject.toml .
COPY README.md .
RUN pip install --upgrade pip
RUN pip install . pytest rich

# 5. Copiar el código fuente y los tests
COPY zen_focus/ ./zen_focus/
COPY tests/ ./tests/
COPY prueba.py /app/prueba.py

# Ejecutamos usando la ruta completa para que no haya error
CMD ["python", "/app/prueba.py"]

# 6. Por defecto, corremos los tests al iniciar
CMD ["pytest"]