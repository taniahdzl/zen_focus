# 🪴 Zen Focus: Gamificación y Enfoque Profundo (Deep Work)

[![PyPI version](https://img.shields.io/pypi/v/zen-focus.svg?color=success)](https://pypi.org/project/zen-focus/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/taniahdzl/zen_focus/blob/main/Tutorial_Zen_Focus.ipynb)

**Zen Focus** es una librería de Python orientada a proteger la atención de desarrolladores, científicos de datos y estudiantes. 

Cuando ejecutamos procesos de alta carga computacional (limpieza de DataFrames gigantes, entrenamiento de modelos, simulaciones estadísticas), los tiempos de espera nos hacen perder nuestro estado de *Deep Work* al abrir redes sociales. Zen Focus resuelve esto mediante **gamificación visual** en la terminal y un **escudo de red** a nivel del sistema operativo.

---

## ✨ Características Principales

1. **Gamificación Visual (POO):** Arte ASCII interactivo que evoluciona en 5 fases proporcionalmente al avance de tu código o tiempo de sesión.
2. **Arquitectura Extensible:** Motor basado en clases abstractas (`TemaBase`). Incluye temas predeterminados: `PlantaFlor`, `Cohete`, `Edificio` y `Bebida`.
3. **Escudo de Red (Context Manager):** Modifica dinámicamente el archivo `hosts` (`/etc/hosts` o `System32/drivers/etc/hosts`) para bloquear sitios web distractores y restaura la conexión de forma segura al finalizar o en caso de error.
4. **Interfaz de Terminal (CLI):** Integración nativa con `rich` para paneles en vivo que no inundan la consola.
5. **Decorador `@con_progreso`:** Gamifica cualquier función Python sin modificar su código interno. El tema evoluciona mientras la función se ejecuta.
6. **Widgets Interactivos:** Explora los temas en Jupyter Notebooks y Google Colab con controles interactivos de sliders y botones.

---

## 🚀 Instalación

Instala la última versión estable directamente desde PyPI:

```bash
pip install zen-focus rich
```

Para probar de inmediato sin configuraciones locales, haz clic en el botón de Open in Colab en la parte superior.

---

## 📖 Uso Básico
La librería puede usarse de varias maneras: integrada en scripts, como decorador, en sesiones dedicadas o en notebooks interactivos.

### 1. Gamificar un Script Largo
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

### 2. Decorador `@con_progreso`
Gamifica funciones automáticamente con un simple decorador. Perfecto para entrenamientos de ML, procesamiento de datos y análisis científicos:

```python
from zen_focus.decoradores import con_progreso
from zen_focus.temas import Cohete

@con_progreso(tema=Cohete("Análisis de datos"), pasos=3)
def pipeline_datos(df):
    df = df.dropna()           # Paso 1
    yield
    df = df[df['valor'] > 0]   # Paso 2
    yield
    resultado = df.sum()       # Paso 3
    return resultado

resultado = pipeline_datos(mi_df)
```

**Sin yield (avance automático en background):**
```python
@con_progreso(tema=PlantaFlor("Entrenamiento"), retardo=1.0)
def entrenar_modelo(X_train, y_train):
    return modelo.fit(X_train, y_train)
```

### 3. Modo Deep Work (Con bloqueo de sitios)
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

### 4. Widget Interactivo (Jupyter / Colab)
Explora y controla los temas interactivamente en notebooks:

```python
from zen_focus.widgets import TemaWidget
from zen_focus.temas import PlantaFlor

# Crear y mostrar el widget
widget = TemaWidget(PlantaFlor("Mi Planta"))
widget.mostrar()
```

El widget incluye:
- **Slider de evolución:** Controla el nivel del tema (1 a n)
- **Botón Evolucionar:** Avanza un nivel (+)
- **Botón Penalizar:** Retrocede un nivel (−)
- **Botón Reset:** Reinicia a nivel 1
- **Vista en vivo:** Arte ASCII actualizado dinámicamente

*Requiere:* `pip install ipywidgets`

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