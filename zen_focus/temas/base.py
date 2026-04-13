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

    # Métodos abstractos que son obligatorios en todas las subclases
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

    def renderizar_ipython(self): 
        """ 
        Muestra el arte ASCII del tema como HTML enriquecido dentro de un
        Jupyter Notebook, sin necesidad de rich ni de bloquear el kernel. 

        Uso: 
            planta = PlantaFlor("Girasol")
            planta.evolucionar()
            planta.renderizar_ipython()
        """
        try: 
            from IPython.display import display, HTML
        except ImportError: 
            print(self.renderizar())
            return 
        
        barra_llena = int((self.nivel_actual/self.nivel_maximo) * 10) 
        barra = "█" * barra_llena + "░" * (10 - barra_llena)
        porcentaje = int((self.nivel_actual/self.nivel_maximo) * 100)

        arte_escapado = (
            self.renderizar()
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        html = f"""
        <div style="
            font-family: monospace;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-left: 4px solid #2d9e75;
            border-radius: 8px;
            padding: 16px 20px;
            display: inline-block;
            min-width: 300px;
        ">
            <div style="color:#2d9e75; font-weight:bold; font-size:13px; margin-bottom:8px;">
                🪴 ZEN FOCUS — {self.nombre}
            </div>
            <pre style="
                margin: 0 0 12px 0;
                font-size: 14px;
                line-height: 1.4;
                color: #212529;
                background: transparent;
            ">{arte_escapado}</pre>
            <div style="font-size:12px; color:#6c757d;">
                Nivel {self.nivel_actual}/{self.nivel_maximo} &nbsp;
                <span style="color:#2d9e75;">{barra}</span>
                &nbsp; {porcentaje}%
            </div>
        </div>
        """
        display(HTML(html))

        @classmethod
        def info_clase(cls): 
            """ 
            Imprime la jerarquía de herencia, atributos de instancia y métodos abstractos
            de la clase como una nueva tabla HTML en el notebook. 

            Uso: 
                TemaBase.info_clase()
                PlantaFlor.info_clase()
            """
            import inspect 

            try: 
                from IPython.display import display, HTML
            except ImportError:
                print(f"Clase: {cls.__name__}")
                print(f"MRO:{' → '.join(c.__name__ for c in cls.__mro__)}")
            return

        # Jerarquía (MRO)
        mro_html = " → ".join(
            f'<code style="background:#e9ecef;padding:2px 6px;border-radius:4px;">{c.__name__}</code>'
            for c in cls.__mro__
            if c is not object
        )

        # Métodos abstractos definidos en TemaBase
        abstractos = [
            nombre
            for nombre, _ in inspect.getmembers(TemaBase, predicate=inspect.isfunction)
            if getattr(getattr(TemaBase, nombre), "__isabstractmethod__", False)
        ]

        # Todos los métodos públicos propios de la clase (sin los heredados de object)
        metodos_propios = [
            (nombre, inspect.signature(func))
            for nombre, func in inspect.getmembers(cls, predicate=inspect.isfunction)
            if not nombre.startswith("_") and nombre not in ("evolucionar", "penalizar", "renderizar")
        ]

        # Atributos definidos en __init__ de TemaBase
        attrs = [
            ("nombre", "str", "Identificador del tema"),
            ("nivel_actual", "int", "Nivel presente (1 … nivel_maximo)"),
            ("nivel_maximo", "int", "Número de fases visuales (default: 5)"),
        ]

        def fila_attr(nombre, tipo, desc):
            return f"""
            <tr>
              <td style="padding:6px 12px;font-family:monospace;color:#2d9e75;">{nombre}</td>
              <td style="padding:6px 12px;font-family:monospace;color:#6f42c1;">{tipo}</td>
              <td style="padding:6px 12px;color:#495057;">{desc}</td>
            </tr>"""

        def fila_metodo(nombre, sig, es_abstracto=False):
            badge = (
                '<span style="background:#fff3cd;color:#856404;font-size:10px;'
                'padding:1px 5px;border-radius:3px;margin-left:6px;">abstracto</span>'
                if es_abstracto else ""
            )
            return f"""
            <tr>
              <td style="padding:6px 12px;font-family:monospace;color:#d63384;">{nombre}{badge}</td>
              <td style="padding:6px 12px;font-family:monospace;color:#6c757d;">{sig}</td>
            </tr>"""

        filas_attrs = "".join(fila_attr(*a) for a in attrs)
        filas_abs = "".join(fila_metodo(m, inspect.signature(getattr(cls, m)), True) for m in abstractos)
        filas_extra = "".join(fila_metodo(n, str(s)) for n, s in metodos_propios)

        html = f"""
        <div style="font-family:sans-serif;font-size:13px;max-width:640px;">

          <div style="background:#e9f7ef;border-left:4px solid #2d9e75;
                      padding:10px 14px;border-radius:4px;margin-bottom:16px;">
            <strong>Clase:</strong>
            <code style="font-size:14px;margin-left:6px;">{cls.__name__}</code>
          </div>

          <p style="margin:0 0 6px;font-weight:600;color:#495057;">Jerarquía de herencia (MRO)</p>
          <p style="margin:0 0 16px;">{mro_html}</p>

          <p style="margin:0 0 6px;font-weight:600;color:#495057;">Atributos de instancia</p>
          <table style="border-collapse:collapse;width:100%;margin-bottom:16px;">
            <thead>
              <tr style="background:#f1f3f5;">
                <th style="padding:6px 12px;text-align:left;">atributo</th>
                <th style="padding:6px 12px;text-align:left;">tipo</th>
                <th style="padding:6px 12px;text-align:left;">descripción</th>
              </tr>
            </thead>
            <tbody>{filas_attrs}</tbody>
          </table>

          <p style="margin:0 0 6px;font-weight:600;color:#495057;">Métodos abstractos (deben implementarse)</p>
          <table style="border-collapse:collapse;width:100%;margin-bottom:16px;">
            <thead>
              <tr style="background:#f1f3f5;">
                <th style="padding:6px 12px;text-align:left;">método</th>
                <th style="padding:6px 12px;text-align:left;">firma</th>
              </tr>
            </thead>
            <tbody>{filas_abs}</tbody>
          </table>

          {"" if not filas_extra else f'''
          <p style="margin:0 0 6px;font-weight:600;color:#495057;">Métodos adicionales</p>
          <table style="border-collapse:collapse;width:100%;margin-bottom:8px;">
            <thead>
              <tr style="background:#f1f3f5;">
                <th style="padding:6px 12px;text-align:left;">método</th>
                <th style="padding:6px 12px;text-align:left;">firma</th>
              </tr>
            </thead>
            <tbody>{filas_extra}</tbody>
          </table>'''}

        </div>
        """
        display(HTML(html))