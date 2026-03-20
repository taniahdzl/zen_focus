from .base import TemaBase

class Edificio(TemaBase):
    """
    Tema visual: Un Rascacielos.
    El esfuerzo de la sesión se traduce en la construcción de un edificio,
    desde los cimientos hasta la antena superior.
    """
    
    def __init__(self, nombre: str = "Torre de Control", nivel_maximo: int = 5):
        super().__init__(nombre=nombre, nivel_maximo=nivel_maximo)
        
        self.fases_ascii = {
            1: """
               
               
               
               
             _[_______]_
            (Cimientos colocados)
            """,
            2: """
               
               
               
               |_____|
             _[_______]_
            (Primer piso construido)
            """,
            3: """
               
               
               |_____|
               |_____|
             _[_______]_
            (Elevando la estructura)
            """,
            4: """
               
                 _|_
               |_____|
               |_____|
             _[_______]_
            (Últimos pisos listos)
            """,
            5: f"""
                  |
                 _|_
               |_____|
               |_____|
             _[_______]_
            (¡Rascacielos {self.nombre} terminado!)
            """
        }

    def evolucionar(self):
        if self.nivel_actual < self.nivel_maximo:
            self.nivel_actual += 1

    def penalizar(self):
        """Si la sesión se rompe, el edificio colapsa a los cimientos."""
        self.nivel_actual = 1

    def renderizar(self) -> str:
        return self.fases_ascii.get(self.nivel_actual, "Error: Fase desconocida")