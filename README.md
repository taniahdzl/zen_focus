# 🪴 Zen Focus: Gamificación y Enfoque Profundo (Deep Work)

[![PyPI version](https://badge.fury.io/py/zen-focus.svg)](https://badge.fury.io/py/zen-focus)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/taniahdzl/zen_focus/blob/main/Tutorial_Zen_Focus.ipynb)

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
```

Para probar de inmediato sin configuraciones locales, haz clic en el botón de Open in Colab en la parte superior.

---

## 📖 Uso Básico
La librería puede usarse de dos maneras principales: integrada en tus scripts largos o como una sesión de enfoque dedicada.

1. Gamificar un Script Largo
Importa un tema y hazlo evolucionar mientras tu código trabaja:

```python
from zen_focus.temas import PlantaFlor
import time

mi_planta = PlantaFlor(nombre="Girasol Analítico")

# Simulamos el procesamiento de datos por lotes
for lote in range(5):
    time.sleep(1) # Reemplaza con tu lógica de código pesada
    mi_planta.evolucionar()
    print(mi_planta.renderizar())
```
2. Modo Deep Work (Con bloqueo de sitios)
Utiliza la clase SesionZen junto con el Escudo para bloquear distracciones.
Nota: Este script requiere ser ejecutado con permisos de administrador (sudo) para modificar las rutas de red.

```python
from zen_focus.motor import SesionZen
from zen_focus.escudo import Escudo
from zen_focus.temas import Cohete

# 1. Definimos las distracciones
distracciones = ["twitter.com", "instagram.com", "youtube.com"]

# 2. El Context Manager garantiza que el internet regrese a la normalidad
with Escudo(bloquear=distracciones) as mi_escudo:
    
    # 3. Configuramos la sesión y el tema
    mision = Cohete(mision="Apolo 11")
    sesion = SesionZen(minutos=25, escudo=mi_escudo, tema=mision)
    
    # 4. ¡Iniciamos el motor en la terminal!
    sesion.iniciar()
```
---
## 🐳 Ejecución Local con Docker
Si deseas probar la interfaz completa y correr los tests automatizados en un entorno aislado sin modificar los permisos de red de tu máquina anfitriona, el proyecto incluye una configuración de Docker lista para usar.

Clona este repositorio y ejecuta:

```bash
docker compose up --build
```
Esto instalará la librería en modo editable, ejecutará las pruebas con `pytest` o levantará el panel interactivo directamente en el contenedor.

---
## 🏗️ Arquitectura y Extensión
Si deseas crear tus propios temas, simplemente hereda de la clase abstracta `TemaBase`:

```python
from zen_focus.base import TemaBase

class MiTemaCustom(TemaBase):
    def evolucionar(self):
        ...
    def penalizar(self):
        ...
    def renderizar(self) -> str:
        ...
```