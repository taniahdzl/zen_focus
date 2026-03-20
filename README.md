# 🪴 Zen Focus
**Librería de productividad gamificada con bloqueo de distracciones.**

## Problema Real: 
Los desarrolladores y estudiantes de ciencia de datos a menudo pierden el enfoque debido a distracciones digitales (redes sociales) y la falta de retroalimentación visual durante tareas largas de procesamiento.
**Solución:** Zen Focus automatiza el bloqueo de distracciones a nivel de red y transforma el tiempo de espera en una experiencia de "crecimiento visual" (Gamificación), aumentando la retención en el estado de Deep Work.

## 🚀 Características
- **Escudo (Shield):** Bloqueo temporal de sitios web modificando `/etc/hosts`.
- **Temas Visuales:** 4 opciones de progreso ASCII (Planta, Cohete, Edificio, Bebida).
- **Interfaz Zen:** Panel dinámico en terminal usando `rich`.

## 🛠️ Instalación
1. Clonar el repositorio.
2. Crear entorno virtual: `python3 -m venv .venv`
3. Activar: `source .venv/bin/activate`
4. Instalar: `pip install -e .`

## 🧪 Testing
Ejecuta las pruebas unitarias con:
`python -m pytest tests/`
