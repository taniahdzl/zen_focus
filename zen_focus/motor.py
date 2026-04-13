import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

console = Console()


class SesionZen:
    def __init__(self, minutos: float, escudo=None, tema=None):
        self.minutos = minutos
        self.segundos_totales = int(minutos * 60)
        self.escudo = escudo
        self.tema = tema

    # ── helpers ────────────────────────────────────────────────────────────

    def _generar_display(self, progreso_relativo: float):
        """
        Calcula qué fase del tema mostrar basándose en el porcentaje de
        tiempo transcurrido y devuelve un Panel de rich.
        """
        nuevo_nivel = int(progreso_relativo * (self.tema.nivel_maximo - 1)) + 1
        if nuevo_nivel > self.tema.nivel_actual:
            for _ in range(nuevo_nivel - self.tema.nivel_actual):
                self.tema.evolucionar()

        return Panel(
            f"{self.tema.renderizar()}\n\n[bold cyan]Misión:[/bold cyan] {self.tema.nombre}",
            title="[bold green]Zen Focus Mode[/bold green]",
            subtitle=f"[bold white]{int(progreso_relativo * 100)}% Completado[/bold white]",
            border_style="green",
            padding=(1, 2),
        )

    def _resetear_tema(self):
        """Devuelve el tema al nivel 1 para poder reutilizarlo."""
        self.tema.nivel_actual = 1

    # ── método original ────────────────────────────────────────────────────

    def iniciar(self):
        """Inicia la sesión en tiempo real (uso en terminal)."""
        console.print(
            f"\n[bold yellow]Entrando en estado de flujo por {self.minutos} min...[/bold yellow]"
        )
        with Live(self._generar_display(0), refresh_per_second=4, console=console) as live:
            try:
                for segundo in range(self.segundos_totales + 1):
                    progreso = segundo / self.segundos_totales
                    live.update(self._generar_display(progreso))
                    if segundo < self.segundos_totales:
                        time.sleep(1)
                console.print("\n[bold gold1]¡Felicidades! Has mantenido el enfoque.[/bold gold1]")
            except KeyboardInterrupt:
                self.tema.penalizar()
                live.update(self._generar_display(0))
                console.print("\n[bold red]Sesión abortada. El progreso se ha perdido.[/bold red]")

    # ── NUEVO #2: demo() ───────────────────────────────────────────────────

    def demo(self, pasos: int = 5, retardo: float = 0.6):
        """
        Simula la sesión completa en *pasos* frames sin esperar tiempo real.
        Pensado para demostraciones en clase o Jupyter Notebooks.

        Parámetros
        ----------
        pasos : int
            Número de frames a mostrar (1 … nivel_maximo).  Default: 5.
        retardo : float
            Segundos entre frames cuando se corre en terminal.  Default: 0.6.

        Uso en notebook:
            sesion = SesionZen(minutos=25, tema=cohete)
            sesion.demo(pasos=5)
        """
        self._resetear_tema()

        en_notebook = _es_notebook()

        if en_notebook:
            self._demo_notebook(pasos)
        else:
            self._demo_terminal(pasos, retardo)

    def _demo_notebook(self, pasos: int):
        """Versión notebook de demo: muestra cada frame como HTML con IPython."""
        try:
            from IPython.display import display, HTML, clear_output
            import time as _time
        except ImportError:
            self._demo_terminal(pasos, retardo=0.6)
            return

        self._resetear_tema()

        for paso in range(pasos):
            progreso = paso / (pasos - 1) if pasos > 1 else 1.0
            # Avanzar el tema al nivel correcto
            nivel_objetivo = int(progreso * (self.tema.nivel_maximo - 1)) + 1
            while self.tema.nivel_actual < nivel_objetivo:
                self.tema.evolucionar()

            porcentaje = int(progreso * 100)
            barra_llena = int(progreso * 20)
            barra = "█" * barra_llena + "░" * (20 - barra_llena)

            arte_escapado = (
                self.tema.renderizar()
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            html = f"""
            <div style="
                font-family: monospace;
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-left: 4px solid #2d9e75;
                border-radius: 8px;
                padding: 16px 20px;
                display: inline-block;
                min-width: 340px;
            ">
                <div style="color:#2d9e75;font-weight:bold;font-size:13px;margin-bottom:8px;">
                    🪴 ZEN FOCUS DEMO — {self.tema.nombre}
                </div>
                <pre style="margin:0 0 12px;font-size:14px;line-height:1.4;
                            color:#212529;background:transparent;">{arte_escapado}</pre>
                <div style="font-size:12px;color:#6c757d;margin-bottom:6px;">
                    Nivel {self.tema.nivel_actual}/{self.tema.nivel_maximo}
                    &nbsp; <span style="color:#2d9e75;">{barra}</span>
                    &nbsp; {porcentaje}%
                </div>
                <div style="font-size:11px;color:#adb5bd;">
                    Frame {paso + 1} / {pasos} &nbsp;·&nbsp;
                    Sesión simulada de {self.minutos} min
                </div>
            </div>
            """
            clear_output(wait=True)
            display(HTML(html))

            if paso < pasos - 1:
                _time.sleep(0.6)

        # Mensaje final
        display(HTML("""
        <div style="font-family:sans-serif;font-size:13px;color:#2d9e75;
                    margin-top:8px;">
            ✅ Demo completada — en producción la sesión dura
            <strong>{} min</strong> en tiempo real.
        </div>""".format(self.minutos)))

    def _demo_terminal(self, pasos: int, retardo: float):
        """Versión terminal de demo: imprime cada frame con rich."""
        self._resetear_tema()
        console.print(
            f"\n[bold yellow]▶ Demo: {pasos} frames de una sesión de {self.minutos} min[/bold yellow]\n"
        )
        for paso in range(pasos):
            progreso = paso / (pasos - 1) if pasos > 1 else 1.0
            nivel_objetivo = int(progreso * (self.tema.nivel_maximo - 1)) + 1
            while self.tema.nivel_actual < nivel_objetivo:
                self.tema.evolucionar()
            console.print(self._generar_display(progreso))
            if paso < pasos - 1:
                time.sleep(retardo)
        console.print("\n[bold green]✓ Demo finalizada.[/bold green]")


# ── utilidad interna ────────────────────────────────────────────────────────

def _es_notebook() -> bool:
    """Detecta si el código corre dentro de un Jupyter/Colab Notebook."""
    import builtins
    get_ipython = getattr(builtins, "get_ipython", None)
    if get_ipython is None:
        return False
    shell = get_ipython().__class__.__name__
    return shell in ("ZMQInteractiveShell", "Shell") 