import pytest
from zen_focus.temas import PlantaFlor

def test_evolucion_planta():
    """Prueba que la planta suba de nivel correctamente."""
    planta = PlantaFlor(nombre="Girasol Test")
    assert planta.nivel_actual == 1
    
    planta.evolucionar()
    assert planta.nivel_actual == 2

def test_penalizacion_planta():
    """Prueba que la planta se reinicie al nivel 1 si se penaliza."""
    planta = PlantaFlor()
    planta.evolucionar() # Sube a 2
    planta.evolucionar() # Sube a 3
    
    planta.penalizar()
    assert planta.nivel_actual == 1

def test_max_level_boundary():
    """Verifica que el nivel no exceda el máximo permitido."""
    planta = PlantaFlor(max_level=5)
    # Forzamos a que llegue al máximo
    for _ in range(10): 
        planta.evolucionar()
    
    assert planta.nivel_actual == 5  # No debe ser 11

def test_tema_custom_name():
    """Verifica que el nombre personalizado se guarde y renderice."""
    nombre_especial = "Bonsai Milenario"
    planta = PlantaFlor(nombre=nombre_especial)
    assert planta.nombre == nombre_especial
    assert nombre_especial in planta.renderizar()

def test_escudo_sin_permisos(monkeypatch):
    """Verifica que el escudo maneje errores de permisos."""
    from zen_focus import Escudo
    import builtins

    # Simulamos que no tenemos permisos de escritura
    def mock_open(*args, **kwargs):
        raise PermissionError("Acceso denegado")
    
    monkeypatch.setattr(builtins, "open", mock_open)
    
    escudo = Escudo(bloquear=["test.com"])
    with pytest.raises(PermissionError):
        escudo.activar()