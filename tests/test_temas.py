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