"""
zen_focus.decoradores
─────────────────────
Decorador @con_progreso para gamificar cualquier función de procesamiento
de datos sin modificar su código interno.

Uso básico:
    from zen_focus.decoradores import con_progreso
    from zen_focus.temas import PlantaFlor

    @con_progreso(tema=PlantaFlor("Bonsai"))
    def entrenar_modelo(X, y):
        modelo.fit(X, y)

    entrenar_modelo(X_train, y_train)

Con número de pasos conocido (para avanzar el tema proporcionalmente):
    @con_progreso(tema=Cohete("Apollo"), pasos=10)
    def procesar_lotes(datos):
        for lote in datos:
            procesar(lote)
            yield          # ← cada yield avanza un nivel
"""

import functools
import threading
import time

from .motor import _es_notebook


def con_progreso(tema, pasos: int = None, retardo: float = 1.0):
    """
    Decorador que muestra el tema evolucionando mientras la función decorada
    se ejecuta en un hilo de fondo.

    Parámetros
    ----------
    tema : TemaBase
        Instancia de cualquier tema (PlantaFlor, Cohete, Edificio, Bebida…).
    pasos : int | None
        Si se conoce de antemano, el tema avanza proporcionalmente.
        Si es None, avanza un nivel cada `retardo` segundos.
    retardo : float
        Segundos entre actualizaciones visuales.  Default: 1.0.

    Ejemplo con pandas / sklearn:
        @con_progreso(tema=PlantaFlor("Análisis"), pasos=3)
        def pipeline(df):
            df = df.dropna()
            yield           # paso 1 completado
            df = escalar(df)
            yield           # paso 2 completado
            return modelo.fit(df)

    Si la función no usa yield, el tema avanza automáticamente en segundo plano.
    """

    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tema.nivel_actual = 1  # reset antes de cada llamada

            en_nb = _es_notebook()

            # ── caso A: función generadora (usa yield para señalar pasos) ──
            if _es_generadora(func):
                return _ejecutar_con_pasos(func, args, kwargs, tema, en_nb)

            # ── caso B: función normal (avance automático en background) ──
            return _ejecutar_con_hilo(func, args, kwargs, tema, retardo, en_nb)

        return wrapper

    return decorador


# ── ejecución con yield (pasos explícitos) ────────────────────────────────

def _ejecutar_con_pasos(func, args, kwargs, tema, en_nb):
    """Avanza el tema cada vez que la función generadora hace yield."""
    try:
        from IPython.display import display, HTML, clear_output
    except ImportError:
        en_nb = False

    gen = func(*args, **kwargs)
    resultado = None
    paso = 0

    while True:
        try:
            next(gen)
            paso += 1
            if tema.nivel_actual < tema.nivel_maximo:
                tema.evolucionar()
            _mostrar(tema, en_nb, label=f"Paso {paso} completado")
        except StopIteration as e:
            resultado = e.value
            break

    # frame final al 100 %
    while tema.nivel_actual < tema.nivel_maximo:
        tema.evolucionar()
    _mostrar(tema, en_nb, label="¡Completado!", final=True)
    return resultado


# ── ejecución con hilo (avance automático) ───────────────────────────────

def _ejecutar_con_hilo(func, args, kwargs, tema, retardo, en_nb):
    resultado_container = [None]
    excepcion_container = [None]
    terminado = threading.Event()

    def target():
        try:
            resultado_container[0] = func(*args, **kwargs)
        except Exception as e:
            excepcion_container[0] = e
        finally:
            terminado.set()

    hilo = threading.Thread(target=target, daemon=True)
    hilo.start()

    while not terminado.is_set():
        if tema.nivel_actual < tema.nivel_maximo:
            tema.evolucionar()
        _mostrar(tema, en_nb)
        terminado.wait(timeout=retardo)

    # frame final
    while tema.nivel_actual < tema.nivel_maximo:
        tema.evolucionar()
    _mostrar(tema, en_nb, final=True)

    if excepcion_container[0]:
        raise excepcion_container[0]
    return resultado_container[0]


# ── render helper ─────────────────────────────────────────────────────────

def _mostrar(tema, en_nb: bool, label: str = "Procesando…", final: bool = False):
    if en_nb:
        _mostrar_nb(tema, label, final)
    else:
        _mostrar_terminal(tema, label, final)


def _mostrar_nb(tema, label: str, final: bool):
    try:
        from IPython.display import display, HTML, clear_output
    except ImportError:
        return

    porcentaje = int((tema.nivel_actual / tema.nivel_maximo) * 100)
    barra_llena = int((tema.nivel_actual / tema.nivel_maximo) * 20)
    barra = "█" * barra_llena + "░" * (20 - barra_llena)
    color = "#2d9e75" if not final else "#198754"
    icono = "✅" if final else "⚙️"

    arte_escapado = (
        tema.renderizar()
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    html = f"""
    <div style="
        font-family: monospace;
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 4px solid {color};
        border-radius: 8px;
        padding: 16px 20px;
        display: inline-block;
        min-width: 320px;
    ">
        <div style="color:{color};font-weight:bold;font-size:13px;margin-bottom:8px;">
            {icono} {tema.nombre} — <span style="font-weight:normal;">{label}</span>
        </div>
        <pre style="margin:0 0 12px;font-size:14px;line-height:1.4;
                    color:#212529;background:transparent;">{arte_escapado}</pre>
        <div style="font-size:12px;color:#6c757d;">
            Nivel {tema.nivel_actual}/{tema.nivel_maximo}
            &nbsp; <span style="color:{color};">{barra}</span>
            &nbsp; {porcentaje}%
        </div>
    </div>
    """
    clear_output(wait=True)
    display(HTML(html))


def _mostrar_terminal(tema, label: str, final: bool):
    from rich.console import Console
    from rich.panel import Panel
    c = Console()
    color = "green" if not final else "gold1"
    c.print(Panel(
        f"{tema.renderizar()}\n\n[{color}]{label}[/{color}]",
        title=f"[bold {color}]{tema.nombre}[/bold {color}]",
        border_style=color,
        padding=(1, 2),
    ))


# ── utilidad interna ──────────────────────────────────────────────────────

def _es_generadora(func) -> bool:
    import inspect
    return inspect.isgeneratorfunction(func)
