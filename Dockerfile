# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos archivos necesarios
COPY pyproject.toml .
COPY README.md .
COPY zen_focus/ ./zen_focus/
COPY tests/ ./tests/

# Instalamos la librería y pytest
RUN pip install . pytest rich

# Comando por defecto: correr los tests para demostrar que funciona
CMD ["pytest"]