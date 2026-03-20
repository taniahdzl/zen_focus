from abc import ABC, abstractmethod

class TemaBase(ABC):
    """
    Clase base abstracta para todos los temas visuales de zen_focus.
    Cualquier tema nuevo (Bonsai, Cohete, etc.) debe heredar de esta clase
    e implementar obligatoriamente estos métodos.
    """
    
    def __init__(self, nombre: str, nivel_maximo: int = 5):
        self.nombre = nombre
        self.nivel_actual = 1
        self.nivel_maximo = nivel_maximo

    @abstractmethod
    def evolucionar(self):
        """Sube el nivel del artefacto visual."""
        pass

    @abstractmethod
    def penalizar(self):
        """Baja el nivel del artefacto visual si la sesión se rompe."""
        pass

    @abstractmethod
    def renderizar(self) -> str:
        """Devuelve el string con el arte ASCII correspondiente al nivel actual."""
        pass