import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

# Instanciamos la consola de rich para imprimir con colores
console = Console()

class SesionZen:
    """
    Motor principal que coordina el tiempo de concentración,
    el escudo bloqueador de distracciones y la evolución del tema visual.
    """
    
    def __init__(self, minutos: int, escudo, tema):
        self.minutos = minutos
        self.segundos_totales = minutos * 60
        self.escudo = escudo
        self.tema = tema

    def iniciar(self):
        """Inicia la cuenta regresiva y la barra de progreso."""
        console.print(f"\n[bold green]Iniciando sesión de {self.minutos} minutos...[/bold green]")
        console.print(f"[cyan]Tema elegido: {self.tema.nombre}[/cyan]")
        console.print(self.tema.renderizar())

        try:
            # Creamos una barra de progreso visualmente atractiva
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("• Tiempo restante: {task.remaining}s"),
                console=console
            ) as progress:
                
                # Agregamos la tarea a la barra
                tarea = progress.add_task("[cyan]Concentración en curso...", total=self.segundos_totales)
                
                # Bucle principal del temporizador
                for _ in range(self.segundos_totales):
                    time.sleep(1)
                    progress.update(tarea, advance=1)
            
            # Si el bucle termina sin ser interrumpido, ¡fue un éxito!
            self.completar_exito()

        except KeyboardInterrupt:
            # Atrapa cuando el usuario presiona Ctrl+C para rendirse
            self.interrumpir()

    def completar_exito(self):
        """Se ejecuta cuando el tiempo termina correctamente."""
        self.tema.evolucionar()
        console.print("\n[bold gold1]✨ ¡Sesión completada con éxito! ✨[/bold gold1]")
        console.print(self.tema.renderizar())

    def interrumpir(self):
        """Se ejecuta si el usuario rompe la sesión prematuramente."""
        self.tema.penalizar()
        console.print("\n[bold red]❌ ¡Sesión interrumpida![/bold red]")
        console.print("Has perdido la concentración. El progreso visual se reinició.")
        console.print(self.tema.renderizar())