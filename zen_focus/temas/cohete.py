from .base import TemaBase

class Cohete(TemaBase):
    """
    Tema visual: Una misión espacial.
    El esfuerzo de la sesión se traduce en el ensamblaje y despegue de un cohete.
    """
    
    def __init__(self, mision: str = "Marte", nivel_maximo: int = 5):
        # Llamamos al constructor de la clase base usando super()
        super().__init__(nombre=mision, nivel_maximo=nivel_maximo)
        
        # Diccionario con el arte ASCII para cada nivel
        self.fases_ascii = {
            1: """
               
               
               
               
             _[_____]_
            (Plataforma lista)
            """,
            2: """
               
               
               |___|
              /  |  \\
             _[__|__]_
            (Ensamblando propulsores)
            """,
            3: """
                / \\
                | |
               /___\\
               |___|
              /  |  \\
             _[__|__]_
            (Cohete en posición)
            """,
            4: """
                / \\
                | |
               /___\\
               |___|
              /  |  \\
             _[__|__]_
              * vvv *
            (¡Ignición de motores!)
            """,
            5: f"""
                 * .
                / \\      *
              . | |  .
               /___\\
               |___|   *
              /  |  \\
               *vvv* .
                 *
            (¡Despegue exitoso hacia {self.nombre}!)
            """
        }

    def evolucionar(self):
        """Sube el nivel del cohete si no ha llegado al máximo."""
        if self.nivel_actual < self.nivel_maximo:
            self.nivel_actual += 1

    def penalizar(self):
        """Si la sesión se rompe, el cohete vuelve a la plataforma vacía."""
        self.nivel_actual = 1

    def renderizar(self) -> str:
        """Devuelve el dibujo correspondiente al nivel actual."""
        return self.fases_ascii.get(self.nivel_actual, "Error: Fase desconocida")