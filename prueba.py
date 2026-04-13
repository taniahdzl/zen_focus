# prueba.py — verifica que todas las features de zen_focus funcionan en terminal
 
from zen_focus import Escudo, SesionZen
from zen_focus.temas import PlantaFlor, Cohete, TemaBase
from zen_focus.decoradores import con_progreso
import time
 
print("=" * 50)
print("  ZEN FOCUS — prueba de features en terminal")
print("=" * 50)
 
# ── 1. renderizar() básico ─────────────────────────────────────────────────
print("\n[1] renderizar() — estado inicial:")
mi_planta = PlantaFlor(nombre="Girasol")
print(mi_planta.renderizar())
 
# ── 2. evolucionar() ──────────────────────────────────────────────────────
print("\n[2] evolucionar() — nivel 3:")
mi_planta.evolucionar()
mi_planta.evolucionar()
print(mi_planta.renderizar())
 
# ── 3. info_clase() en terminal ────────────────────────────────────────────
print("\n[3] TemaBase.info_clase() — jerarquía de herencia:")
TemaBase.info_clase()
 
# ── 4. SesionZen.demo() en terminal ───────────────────────────────────────
print("\n[4] SesionZen.demo() — 5 frames sin tiempo real:")
cohete = Cohete(mision="Apolo 11")
sesion = SesionZen(minutos=25, tema=cohete)
sesion.demo(pasos=5, retardo=0.3)
 
# ── 5. @con_progreso — modo automático ────────────────────────────────────
print("\n[5] @con_progreso — modo automático:")
 
@con_progreso(tema=PlantaFlor("Limpieza"), retardo=0.5)
def limpiar_datos():
    time.sleep(2)
    return "100 filas procesadas"
 
resultado = limpiar_datos()
print(f"Resultado: {resultado}")
 
# ── 6. @con_progreso — modo con yield ─────────────────────────────────────
print("\n[6] @con_progreso — modo con pasos (yield):")
 
@con_progreso(tema=Cohete("Pipeline"))
def pipeline(pasos):
    for i in range(pasos):
        time.sleep(0.4)
        yield
    return f"{pasos} etapas completadas"
 
resultado = pipeline(4)
print(f"Resultado: {resultado}")
 
# ── 7. Escudo + SesionZen.iniciar() (requiere sudo) ───────────────────────
print("\n[7] Escudo + sesion.iniciar() — sesión de 6 segundos:")
mi_escudo = Escudo(bloquear=["youtube.com", "reddit.com"])
sesion_corta = SesionZen(minutos=0.1, escudo=mi_escudo, tema=PlantaFlor("Girasol"))
 
try:
    with mi_escudo:
        sesion_corta.iniciar()
except PermissionError:
    print("  → Recuerda correr con 'sudo' para activar el Escudo real.")
 
print("\n✓ Todas las pruebas completadas.")