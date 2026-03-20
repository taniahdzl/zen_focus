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

# En test_temas.py
def test_max_level_boundary():
    # Cambia max_level por nivel_maximo
    planta = PlantaFlor(nivel_maximo=5) 
    for _ in range(10): 
        planta.evolucionar()
    assert planta.nivel_actual == 5

# En test_temas.py
def test_tema_custom_name():
    nombre_especial = "Bonsai Milenario"
    planta = PlantaFlor(nombre=nombre_especial)
    
    # Llevamos la planta al nivel 5 para que el nombre aparezca en el render
    for _ in range(4):
        planta.evolucionar()
        
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