# prueba.py
from zen_focus import Escudo, SesionZen
from zen_focus.temas import PlantaFlor

# Creamos el escudo (puedes poner dominios reales que te distraigan)
mi_escudo = Escudo(bloquear=["youtube.com", "reddit.com"])

# Elegimos la planta de flores
mi_planta = PlantaFlor(nombre="Girasol")

# Hacemos una sesión MUY corta (ej. 0.1 minutos = 6 segundos) solo para probar
sesion = SesionZen(minutos=0.1, escudo=mi_escudo, tema=mi_planta)

try:
    with mi_escudo:
        sesion.iniciar()
except PermissionError:
    print("Recuerda correr el script con 'sudo' para probar el Escudo real.")