"""
Componentes reutilizables para la interfaz gráfica.

Este módulo contiene:
- AppTheme: colores de la interfaz grafica
- AppConfig: configuraciones generales
- UploadButton: botón personalizado
- Panel: contenedor con titulo
- LoadingIndicator: indicador de carga animado
- NotificationWindow: ventana de notificación
"""

import customtkinter as ctk


# ============================================================================
# COLORES Y CONFIGURACION
# ============================================================================

class AppTheme:
    """
    Paleta de colores y constantes visuales de la interfaz grafica.

    Centraliza todos los colores utilizados en la interfaz para mantener
    consistencia visual y facilitar cambios de tema futuros.

    Atributos
    ---------
    BG_PRIMARY : str
        Color de fondo principal (negro suave).
    BG_SECONDARY : str
        Color de fondo secundario (gris oscuro).
    BG_TERTIARY : str
        Color de fondo terciario (gris medio).
    ACCENT_PRIMARY : str
        Color de acento principal (azul).
    ACCENT_HOVER : str
        Color de acento en hover (azul oscuro).
    ACCENT_LIGHT : str
        Color de acento claro (azul claro).
    TEXT_PRIMARY : str
        Color de texto principal (blanco).
    TEXT_SECONDARY : str
        Color de texto secundario (gris claro).
    TEXT_DIM : str
        Color de texto atenuado (gris medio).
    SUCCESS : str
        Color para estados de éxito (verde azulado).
    ERROR : str
        Color para estados de error (rojo suave).
    WARNING : str
        Color para advertencias (amarillo suave).
    BORDER : str
        Color de bordes (gris).

    Notas
    -----
    Todos los colores están en formato hexadecimal (#RRGGBB).
    """

    # Fondos (Colores principales)
    PRIMARY_BACKGROUND = "#1e1e1e"
    SECONDARY_BACKGROUND = "#2d2d30"
    TERTIARY_BACKGROUND = "#3e3e42"

    # Acentos (colores destacados)
    PRIMARY_ACCENT = "#007acc"
    HOVER_ACCENT = "#005a9e"
    LIGHT_ACCENT = "#4da6ff"

    # Textos
    PRIMARY_TEXT = "#ffffff"
    SECONDARY_TEXT = "#cccccc"
    DIM_TEXT = "#858585"

    # Estados
    SUCCES = "#4ec9b0"
    ERROR = "#f48771"
    WARNING = "#f48771"

    # Bordes
    BORDER = "#3e3e42"


class AppConfig:
    """
    Configuraciones globales de la interfaz grafica.

    Aqui están las fuentes, tamaños de ventana,
    y extensiones de archivo permitidas.

    Atributos
    ---------
    FAMILY_FONT : str
        Familia de fuente principal.
    TITLE_FONT : tuple
        Configuración de fuente para titulos (familia, tamaño, peso).
    SUBTITLE_FONT : tuple
        Configuración de fuente para subtitulos.
    BODY_FONT : tuple
        Configuración de fuente para texto de cuerpo.
    SMALL_FONT  : tuple
        Configuración de fuente para texto pequeño.
    MONO_FONT : tuple
        Configuración de fuente monoespaciada.
    WINDOW_WIDTH : int
        Ancho predeterminado de la ventana en pixeles.
    WINDOW_HEIGHT : int
        Alto predeterminado de la ventana en pixeles.
    PADDING : int
        Padding estándar en pixeles.
    BUTTON_HEIGHT : int
        Altura estándar de botones en pixeles.
    ALLOWED_EXTENSIONS : list
        Lista de tuplas con extensiones de archivo permitidas.
    """
    # Fuentes
    FAMILY_FONT = "Segoe UI"
    TITLE_FONT = ("Orbitron", 35, "bold")
    SUBTITLE_FONT = ("Segoe UI", 13)
    BODY_FONT = ("Segoe UI", 15)
    SMALL_FONT = ("Segoe UI", 10)
    MONO_FONT = ("Consolas", 14)

    # Tamaños de ventana
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 700
    PADDING = 20
    BUTTON_HEIGHT = 40

    # Archivos permitidos
    ALLOWED_EXTENTIONS = [
        ("Datasets soportados", "*.csv *.xlsx *.xls *.sqlite *.db")
    ]


# ============================================================================
# COMPONENTES DE INTERFAZ
# ============================================================================

class UploadButton(ctk.CTkButton):
    """
    Botón con estilo personalizado.

    Uso:
        button = UploadButton(parent, text = "Cargar", command = mi_funcion)
    """

    def __init__(self, master, text, command=None, **kwargs):
        super().__init__(
            master,
            text=text,
            command=command,
            font=AppConfig.BODY_FONT,
            height=AppConfig.BUTTON_HEIGHT,
            corner_radius=6,
            fg_color=AppTheme.PRIMARY_ACCENT,
            hover_color=AppTheme.HOVER_ACCENT,
            text_color="#ffffff",
            border_width=0,
            **kwargs
        )


class Panel(ctk.CTkFrame):
    """
    Contenedor con barra de titulo.

    Uso:
        panel = Panel(parent, "Mi Titulo")
        label = ctk.CTkLabel(panel, text = "Contenido")
        label.pack()
    """

    def __init__(self, master, title, **kwargs):
        # Crear el frame
        super().__init__(
            master,
            corner_radius=8,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_width=1,
            border_color=AppTheme.BORDER,
            **kwargs
        )

        # Crear la barra de titulo
        self._create_title_bar(title)

    def _create_title_bar(self, title):
        """Crear la barra de titulo del panel"""
        title_bar = ctk.CTkFrame(
            self,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            height=38
        )
        title_bar.pack(fill="x", padx=2, pady=2)
        title_bar.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            title_bar,
            text=title,
            font=("Orbitron", 15, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.title_label.pack(pady=10, padx=15, anchor="w")


# ============================================================================
# COMPONENTES DE FEEDBACK
# ============================================================================

class LoadingIndicator(ctk.CTkFrame):
    """
    Indicador de carga con barra de progreso animada.

    Uso:
        indicator = LoadingIndicator(parent)
        indicator.place(relx = 0.5, rely = 0.5, anchor = "center")
        # ...hacer algo...
        indicator.stop()
        indicator.destroy()
    """

    def __init__(self, master, **kwargs):
        # Crear el frame
        super().__init__(
            master,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=2,
            border_color=AppTheme.PRIMARY_ACCENT,
            **kwargs
        )

        # Crear elementos
        self._create_indicator_content()

        # Iniciar animación
        self.progress_bar.start()

    def _create_indicator_content(self):
        """Crear los elementos visuales del indicador"""
        # Label "Cargando datos..."
        self.label = ctk.CTkLabel(
            self,
            text="Cargando datos...",
            font=("Orbitron", 12, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.label.pack(pady=(20, 10))

        # Barra de progreso animada
        self.progress_bar = ctk.CTkProgressBar(
            self,
            mode="indeterminate",
            progress_color=AppTheme.PRIMARY_ACCENT,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            height=6,
            corner_radius=6
        )
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 20))

        # Label de estado
        self.status_label = ctk.CTkLabel(
            self,
            text="Procesando datos...",
            font=AppConfig.SMALL_FONT,
            text_color=AppTheme.SECONDARY_TEXT
        )
        self.status_label.pack(pady=(0, 15))

    def stop(self):
        """Detener la animación"""
        self.progress_bar.stop()


class NotificationWindow(ctk.CTkToplevel):
    """
    Ventana emergente para mostrar mensajes.

    Uso:
        NotificationWindow(
            parent = ventana_principal,
            title = "Éxito",
            message = "Operación completada",
            notification_type = "success" o "error" o "warning" o "info"
        )
    """

    # Tamaño de la ventana
    WINDOW_WIDTH = 450
    WINDOW_HEIGHT = 200

    # Configuración de colores e iconos según el tipo
    NOTIFICATION_CONFIG = {
        "success": {"color": AppTheme.SUCCES, "icon": "✓"},
        "error": {"color": AppTheme.ERROR, "icon": "✗"},
        "warning": {"color": AppTheme.WARNING, "icon": "⚠"},
        "info": {"color": AppTheme.PRIMARY_ACCENT, "icon": "i"}
    }

    def __init__(self, parent, title, message, notification_type="info"):
        super().__init__(parent)

        # Configurar ventana
        self.title("")
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.resizable(False, False)

        self._center_window()

        # Obtener configuración del tipo
        config = self.NOTIFICATION_CONFIG.get(
            notification_type,
            self.NOTIFICATION_CONFIG["info"]
        )

        self._create_notification_content(title, message, config)

        # Hacer modal (bloquear ventana padre)
        self.transient(parent)
        self.grab_set()

    def _center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()

        # Calcular posición
        x = (self.winfo_screenwidth() // 2) - (self.WINDOW_WIDTH // 2)
        y = (self.winfo_screenheight() // 2) - (self.WINDOW_HEIGHT // 2)

        # Aplicar posición
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

    def _create_notification_content(self, title, message, config):
        """Crear el contenido de la notificación"""
        color = config["color"]
        icon = config["icon"]

        main_frame = ctk.CTkFrame(
            self,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_width=2,
            border_color=color
        )
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # HEADER (barra de titulo con icono)
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            height=45
        )
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon}  {title}",
            font=("Segoe UI", 13, "bold"),
            text_color=color
        )
        title_label.pack(pady=12, padx=20, anchor="w")

        message_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        message_frame.pack(fill="both", expand=True, padx=20, pady=(15, 10))

        message_label = ctk.CTkLabel(
            message_frame,
            text=message,
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.PRIMARY_TEXT,
            wraplength=400,
            justify="left"
        )
        message_label.pack()

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="both", padx=20, pady=(0, 15))

        close_button = ctk.CTkButton(
            button_frame,
            text="ACEPTAR",
            font=("Orbitron", 10, "bold"),
            fg_color=color,
            hover_color=AppTheme.TERTIARY_BACKGROUND,
            text_color="#ffffff",
            height=32,
            corner_radius=6,
            command=self.destroy
        )
        close_button.pack(side="right")
