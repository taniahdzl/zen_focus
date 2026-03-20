from .base import TemaBase

class PlantaFlor(TemaBase):
    """
    Tema visual: Una Planta con Flores.
    El esfuerzo de la sesión se traduce en el crecimiento de un tallo
    hasta que florece una flor detallada.
    """
    
    def __init__(self, nombre: str = "Girasol", nivel_maximo: int = 5):
        super().__init__(nombre=nombre, nivel_maximo=nivel_maximo)
        
        # Diccionario con el arte ASCII para cada nivel (fase de crecimiento)
        self.fases_ascii = {
            1: """
               
               
               
               
             __[_🌱_]__
            (Brote inicial)
            """,
            2: """
               
               
                |
              \\|//
              //|\\
             _[___]__
            (Creciendo tallo)
            """,
            3: """
                  ,.-.
                 (    )
                 '._.'
                   |
                 \\|//
                _[___]__
            (Aparece el capullo)
            """,
            4: """
                 _|_
               _(   )_
              (       )
               (_ _ _)
                  |
                \\|/
               _[___]__
            (Comienza a florecer)
            """,
            5: f"""
                 _|_
               _(:::)_
              (:::::::)
               (_:::_)
                  |  
                \\|/ 
                  | 
              _[_____]__
            (¡Tu {self.nombre} ha florecido!)
            """
        }

    def evolucionar(self):
        """Sube el nivel de la planta si no ha llegado al máximo."""
        if self.nivel_actual < self.nivel_maximo:
            self.nivel_actual += 1

    def penalizar(self):
        """Si la sesión se rompe, la planta vuelve a ser un brote."""
        self.nivel_actual = 1

    def renderizar(self) -> str:
        """Devuelve el dibujo correspondiente al nivel actual."""
        return self.fases_ascii.get(self.nivel_actual, "Error: Fase desconocida")