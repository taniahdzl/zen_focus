"""
zen_focus.widgets
─────────────────
Widget interactivo para explorar los temas de zen_focus dentro de un
Jupyter Notebook o Google Colab.

Requiere: ipywidgets  (pip install ipywidgets)

Uso:
    from zen_focus.widgets import TemaWidget
    from zen_focus.temas import PlantaFlor

    w = TemaWidget(PlantaFlor("Demo"))
    w.mostrar()
"""


def TemaWidget(tema):
    """
    Devuelve un widget interactivo de ipywidgets para explorar el tema.

    Incluye:
    - Slider de nivel (1 … nivel_maximo)
    - Botón "Evolucionar +"
    - Botón "Penalizar −"
    - Botón "Reset"
    - Vista HTML del arte ASCII actualizada en vivo

    Parámetros
    ----------
    tema : TemaBase
        Instancia de cualquier subclase de TemaBase.

    Retorna
    -------
    ipywidgets.VBox (lista para mostrar con display() o como última línea)
    """
    try:
        import ipywidgets as widgets
        from IPython.display import display, HTML
    except ImportError:
        raise ImportError(
            "ipywidgets no está instalado. "
            "Instálalo con: pip install ipywidgets"
        )

    # ── estado ────────────────────────────────────────────────────────────
    tema.nivel_actual = 1

    # ── helpers ───────────────────────────────────────────────────────────

    def _html_arte(nivel_override=None):
        nivel = nivel_override if nivel_override is not None else tema.nivel_actual
        porcentaje = int((nivel / tema.nivel_maximo) * 100)
        barra_llena = int((nivel / tema.nivel_maximo) * 10)
        barra = "█" * barra_llena + "░" * (10 - barra_llena)

        arte_escapado = (
            tema.renderizar()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        return f"""
        <div style="
            font-family: monospace;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-left: 4px solid #2d9e75;
            border-radius: 8px;
            padding: 14px 18px;
            display: inline-block;
            min-width: 280px;
        ">
            <div style="color:#2d9e75;font-weight:bold;font-size:13px;margin-bottom:8px;">
                🪴 {tema.nombre}
            </div>
            <pre style="margin:0 0 10px;font-size:14px;line-height:1.4;
                        color:#212529;background:transparent;">{arte_escapado}</pre>
            <div style="font-size:12px;color:#6c757d;">
                Nivel <strong>{nivel}</strong> / {tema.nivel_maximo}
                &nbsp; <span style="color:#2d9e75;">{barra}</span>
                &nbsp; {porcentaje}%
            </div>
        </div>
        """

    # ── widgets ───────────────────────────────────────────────────────────

    salida = widgets.Output()

    slider = widgets.IntSlider(
        value=1,
        min=1,
        max=tema.nivel_maximo,
        step=1,
        description="Nivel:",
        continuous_update=False,
        style={"description_width": "50px"},
        layout=widgets.Layout(width="280px"),
    )

    btn_evolucionar = widgets.Button(
        description="Evolucionar +",
        button_style="success",
        icon="arrow-up",
        layout=widgets.Layout(width="140px"),
    )

    btn_penalizar = widgets.Button(
        description="Penalizar −",
        button_style="warning",
        icon="arrow-down",
        layout=widgets.Layout(width="140px"),
    )

    btn_reset = widgets.Button(
        description="Reset",
        button_style="danger",
        icon="refresh",
        layout=widgets.Layout(width="100px"),
    )

    etiqueta_clase = widgets.HTML(
        value=_html_badge(tema),
    )

    # ── lógica ────────────────────────────────────────────────────────────

    def _refrescar():
        slider.value = tema.nivel_actual
        with salida:
            from IPython.display import clear_output, display, HTML
            clear_output(wait=True)
            display(HTML(_html_arte()))

    def on_slider(change):
        objetivo = change["new"]
        if objetivo > tema.nivel_actual:
            for _ in range(objetivo - tema.nivel_actual):
                tema.evolucionar()
        elif objetivo < tema.nivel_actual:
            for _ in range(tema.nivel_actual - objetivo):
                tema.penalizar()
        _refrescar()

    def on_evolucionar(_):
        if tema.nivel_actual < tema.nivel_maximo:
            tema.evolucionar()
        _refrescar()

    def on_penalizar(_):
        if tema.nivel_actual > 1:
            tema.penalizar()
        _refrescar()

    def on_reset(_):
        tema.nivel_actual = 1
        _refrescar()

    slider.observe(on_slider, names="value")
    btn_evolucionar.on_click(on_evolucionar)
    btn_penalizar.on_click(on_penalizar)
    btn_reset.on_click(on_reset)

    # ── inicializar output ────────────────────────────────────────────────
    with salida:
        display(HTML(_html_arte()))

    # ── layout ────────────────────────────────────────────────────────────
    controles = widgets.HBox(
        [btn_evolucionar, btn_penalizar, btn_reset],
        layout=widgets.Layout(gap="8px", margin="8px 0"),
    )

    encabezado = widgets.HTML(
        "<div style='font-family:sans-serif;font-size:13px;"
        "color:#495057;margin-bottom:4px;'>"
        f"<strong>TemaWidget</strong> — <code>{type(tema).__name__}</code>"
        "</div>"
    )

    return widgets.VBox(
        [encabezado, etiqueta_clase, slider, controles, salida],
        layout=widgets.Layout(padding="4px"),
    )


# ── utilidad interna ──────────────────────────────────────────────────────

def _html_badge(tema):
    mro = [c.__name__ for c in type(tema).__mro__ if c.__name__ not in ("object",)]
    cadena = " → ".join(
        f'<code style="background:#e9ecef;padding:2px 6px;border-radius:4px;">{n}</code>'
        for n in mro
    )
    return f"<div style='font-size:12px;margin-bottom:8px;'>{cadena}</div>"
