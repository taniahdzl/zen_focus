from .base import TemaBase

class Bebida(TemaBase):
    """
    Tema visual: Una taza de café o té.
    El esfuerzo de la sesión representa el tiempo de preparación
    de tu bebida favorita perfecta.
    """
    
    def __init__(self, nombre: str = "Espresso Doble", nivel_maximo: int = 5):
        super().__init__(nombre=nombre, nivel_maximo=nivel_maximo)
        
        self.fases_ascii = {
            1: """
               
               
               
             \\         /
              \\_______/
            (Taza vacía lista)
            """,
            2: """
               
               
               . . . .
             \\         /
              \\_______/
            (Agregando ingredientes)
            """,
            3: """
               
                |   |
               .|...|.
             \\         /
              \\_______/
            (Vertiendo agua caliente)
            """,
            4: """
               
               
             \\~~~~~~~~~/
              \\_______/
            (Bebida servida)
            """,
            5: f"""
                 (  )
                  )(
             \\~~~~~~~~~/
              \\_______/
            (¡Tu {self.nombre} está humeante y listo!)
            """
        }

    def evolucionar(self):
        if self.nivel_actual < self.nivel_maximo:
            self.nivel_actual += 1

    def penalizar(self):
        """Si la sesión se rompe, se tira la bebida y vuelve a empezar."""
        self.nivel_actual = 1

    def renderizar(self) -> str:
        return self.fases_ascii.get(self.nivel_actual, "Error: Fase desconocida")