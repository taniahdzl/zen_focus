import os
import platform

class Escudo:
    """
    Context Manager que bloquea el acceso a sitios web modificando
    el archivo hosts del sistema temporalmente.
    """
    
    def __init__(self, bloquear: list[str]):
        self.sitios_a_bloquear = bloquear
        # Detectar el sistema operativo para encontrar el archivo correcto
        if platform.system() == "Windows":
            self.ruta_hosts = r"C:\Windows\System32\drivers\etc\hosts"
        else:
            self.ruta_hosts = "/etc/hosts"
            
        self.ip_redireccion = "127.0.0.1"
        self.marca_inicio = "# --- ZEN_FOCUS_START ---\n"
        self.marca_fin = "# --- ZEN_FOCUS_END ---\n"

    def __enter__(self):
        """Se ejecuta al entrar al bloque 'with'."""
        self.activar()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Se ejecuta al salir del bloque 'with', incluso si hay un error."""
        self.desactivar()
        # Retornar False permite que los errores fluyan si ocurrieron
        return False 

    def activar(self):
        """Escribe las reglas de bloqueo en el archivo hosts."""
        try:
            with open(self.ruta_hosts, 'r') as file:
                contenido = file.read()

            # Evitar duplicados si ya estaba activado
            if self.marca_inicio not in contenido:
                with open(self.ruta_hosts, 'a') as file:
                    file.write("\n" + self.marca_inicio)
                    for sitio in self.sitios_a_bloquear:
                        file.write(f"{self.ip_redireccion} {sitio}\n")
                        file.write(f"{self.ip_redireccion} www.{sitio}\n")
                    file.write(self.marca_fin)
                print(f"Escudo activado: {len(self.sitios_a_bloquear)} sitios bloqueados.")
        except PermissionError:
            print("Error de permisos: Debes ejecutar el script como Administrador/Sudo para activar el escudo.")
            raise

    def desactivar(self):
        """Limpia las reglas de bloqueo del archivo hosts."""
        try:
            with open(self.ruta_hosts, 'r') as file:
                lineas = file.readlines()

            with open(self.ruta_hosts, 'w') as file:
                bloqueando = False
                for linea in lineas:
                    if linea == self.marca_inicio:
                        bloqueando = True
                    
                    if not bloqueando:
                        file.write(linea)
                        
                    if linea == self.marca_fin:
                        bloqueando = False
            print("Escudo desactivado: Conexión restaurada.")
        except PermissionError:
            print("Error de permisos al intentar restaurar el archivo hosts.")