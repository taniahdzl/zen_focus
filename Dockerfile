# 1. Imagen base oficial de Python
FROM python:3.11-slim

# 2. Evitar que Python genere archivos .pyc y use buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. Copiamos solo lo necesario para instalar primero
COPY pyproject.toml .
COPY README.md .

# 2. Instalamos dependencias básicas
RUN pip install --upgrade pip
RUN pip install pytest rich setuptools

# 3. Copiamos el código fuente
COPY zen_focus/ ./zen_focus/
COPY prueba.py .
COPY tests/ ./tests/

# 4. Instalamos la librería en modo editable
RUN pip install -e .

# 5. Ejecutamos el script de prueba
CMD ["python", "prueba.py"]
