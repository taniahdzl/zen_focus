import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

class SesionZen:
    def __init__(self, minutos: int, escudo, tema):
        self.minutos = minutos
        self.segundos_totales = int(minutos * 60)
        self.escudo = escudo
        self.tema = tema

    def _generar_display(self, progreso_relativo: float):
        """
        Calcula qué fase del tema mostrar basándose en el porcentaje de tiempo 
        y devuelve un panel estético.
        """
        # Calcular nivel (1 a 5) proporcional al progreso (0.0 a 1.0)
        nuevo_nivel = int(progreso_relativo * (self.tema.nivel_maximo - 1)) + 1
        
        # Solo actualizamos si el nivel ha subido
        if nuevo_nivel > self.tema.nivel_actual:
            for _ in range(nuevo_nivel - self.tema.nivel_actual):
                self.tema.evolucionar()

        # Creamos un panel que contiene el arte ASCII y una mini-info debajo
        return Panel(
            f"{self.tema.renderizar()}\n\n[bold cyan]Misión:[/bold cyan] {self.tema.nombre}",
            title="[bold green]Zen Focus Mode[/bold green]",
            subtitle=f"[bold white]{int(progreso_relativo * 100)}% Completado[/bold white]",
            border_style="green",
            padding=(1, 2)
        )

    def iniciar(self):
        console.print(f"\n[bold yellow]Entrando en estado de flujo por {self.minutos} min...[/bold yellow]")
        
        # La magia de 'Live' permite refrescar el panel sin llenar la pantalla de texto
        with Live(self._generar_display(0), refresh_per_second=4, console=console) as live:
            try:
                for segundo in range(self.segundos_totales + 1):
                    # Calculamos el progreso de 0.0 a 1.0
                    progreso = segundo / self.segundos_totales
                    
                    # Actualizamos el dibujo en pantalla
                    live.update(self._generar_display(progreso))
                    
                    if segundo < self.segundos_totales:
                        time.sleep(1)
                
                console.print("\n[bold gold1] ¡Felicidades! Has mantenido el enfoque. [/bold gold1]")
            
            except KeyboardInterrupt:
                self.tema.penalizar()
                live.update(self._generar_display(0))
                console.print("\n[bold red] Sesión abortada. El progreso se ha perdido.[/bold red]")