# 🪴 Zen Focus: Gamificación y Enfoque Profundo (Deep Work)

[![PyPI version](https://badge.fury.io/py/zen-focus.svg)](https://badge.fury.io/py/zen-focus)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/zen_focus/blob/main/Tutorial_Zen_Focus_Moni.ipynb)

**Zen Focus** es una librería de Python orientada a proteger la atención de desarrolladores, científicos de datos y estudiantes. 

Cuando ejecutamos procesos de alta carga computacional (limpieza de DataFrames gigantes, entrenamiento de modelos, simulaciones estadísticas), los tiempos de espera nos hacen perder nuestro estado de *Deep Work* al abrir redes sociales. Zen Focus resuelve esto mediante **gamificación visual** en la terminal y un **escudo de red** a nivel del sistema operativo.

---

## ✨ Características Principales

1. **Gamificación Visual (POO):** Arte ASCII interactivo que evoluciona en 5 fases proporcionalmente al avance de tu código o tiempo de sesión.
2. **Arquitectura Extensible:** Motor basado en clases abstractas (`TemaBase`). Incluye temas predeterminados: `PlantaFlor`, `Cohete`, `Edificio` y `Bebida`.
3. **Escudo de Red (Context Manager):** Modifica dinámicamente el archivo `hosts` (`/etc/hosts` o `System32/drivers/etc/hosts`) para bloquear sitios web distractores y restaura la conexión de forma segura al finalizar o en caso de error.
4. **Interfaz de Terminal (CLI):** Integración nativa con `rich` para paneles en vivo que no inundan la consola.

---

## 🚀 Instalación

Instala la última versión estable directamente desde PyPI:

```bash
pip install zen-focus rich