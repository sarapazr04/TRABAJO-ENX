"""
Componentes para la interfaz gráfica.
Autor: youssef-nabaha

Clases
------
AppTheme
    Paleta de colores y constantes visuales.
AppConfig
    Configuraciones globales de la aplicación.
UploadButton
    Botón con estilo consistente.
Panel
    Contenedor con título integrado.
LoadingIndicator
    Indicador de carga animado.
NotificationWindow
    Ventana modal de notificación.
"""

import customtkinter as ctk
from typing import Optional, Callable


class AppTheme:
    """
    Paleta de colores y constantes visuales de la GUI.
    
    Centralizar todos los colores utilizados en la interfaz para mantener
    consistencia visual y facilitar cambios de tema futuros.
    
    Atributos
    ---------
    PRIMARY_BACKGROUND : str
        Color de fondo principal (negro suave).
    SECONDARY_BACKGROUND : str
        Color de fondo secundario (gris oscuro).
    TERTIARY_BACKGROUD : str
        Color de fondo terciario (gris medio).
    PRIMARY_ACCENT: str
        Color de acento principal (azul).
    HOVER_ACCENT : str
        Color de acento en hover (azul oscuro).
    LIGHT_ACCENT : str
        Color de acento claro (azul claro).
    PRIMARY_TEXT : str
        Color de texto principal (blanco).
    ECONDARY_TEXT: str
        Color de texto secundario (gris claro).
    DIM_TEXT: str
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
    La paleta sigue un esquema de tema oscuro.
    """

    # Colores principales
    PRIMARY_BACKGROUND = "#1e1e1e"
    SECONDERY_BACKGROUND= "#2d2d30"
    TERTIARY_BACKGROUND = "#3e3e42"

    # Acentos
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
    Configuraciones globales de la GUI.
    
    Centralizar constantes de configuración como fuentes, dimensiones
    y extensiones de archivo permitidas.
    
    Atributos
    ---------
    FAMILY_FONT: str
        Fuente de Familia principal.
    TITLE_FONT : tuple
        Configuración de fuente para títulos (familia, tamaño, peso).
    SUBTITLE_FONT : tuple
        Configuración de fuente para subtítulos.
    BODY_FONT : tuple
        Configuración de fuente para texto de cuerpo.
    SMALL_FONT : tuple
        Configuración de fuente para texto pequeño.
    MONO_FONT : tuple
        Configuración de fuente monoespaciada.
    WINDOW_WIDTH : int
        Ancho predeterminado de la ventana en píxeles.
    WINDOW_HEIGHT : int
        Alto predeterminado de la ventana en píxeles.
    PADDING : int
        Padding estándar en píxeles.
    BUTTON_HEIGHT : int
        Altura estándar de botones en píxeles.
    ALLOWED_EXTENSIONS : list
        Lista de tuplas con extensiones de archivo permitidas.
    
    Ejemplos
    --------
    >>> AppConfig.WINDOW_WIDTH
    1400
    >>> AppConfig.TITLE_FONT
    ("Orbitron", 35, "bold")
    """

    # Tipografia
    FAMILY_FONT= "Segoe UI"
    TITLE_FONT = ("Orbitron", 35, "bold")
    SUBTITLE_FONT = ("Segoe UI", 13)
    BODY_FONT = ("Segoe UI", 13)
    SMALL_FONT = ("Segoe UI", 9)
    MONO_FONT = ("Consolas", 10)

    # Demensiones de ventana
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    PADDING = 20
    BUTTON_HEIGHT = 40

    # Extensiones permitidas de archivos
    ALLOWED_EXTENTIONS = [
        ("Datasets soportados", "*.csv *.xlsx *.xls *.sqlite *.db")
        ]


class UploadButton(ctk.CTkButton):
    """
    Botón con estilo consistente del software.
    
    Hereda de CTkButton y aplica automáticamente el estilo visual
    definido en AppTheme, garantizando consistencia en toda la GUI.
    
    Parámetros
    ----------
    master : ctk.CTkBaseClass
        Widget padre donde se colocará el botón.
    text : str
        Texto a mostrar en el botón.
    command : callable, opcional
        Función a ejecutar al hacer clic. Por defecto None.
    **kwargs
        Argumentos adicionales para CTkButton.
    
    Ejemplos
    --------
    >>> button = UploadButton(
    ...     parent_frame,
    ...     text="CARGAR",
    ...     command=load_file_function
    ... )
    
    Notas
    -----
    Los colores y dimensiones se toman automáticamente de AppTheme
    y AppConfig, facilitando cambios globales de estilo.
    """

    def __init__(
            self, 
            master: ctk.CTkBaseClass, 
            text: str, 
            command: Optional[Callable] = None, 
            **kwargs # Permitir pasar parametros adicionales
            ):
        
        # Llama al constructor del padre (CTkButton) con estilo predefinido
        super().__init__(
            master, 
            text = text, 
            command = command, 
            font = ("Orbitron", 11, "bold"), 
            height = AppConfig.BUTTON_HEIGHT, 
            corner_radius = 6, 
            fg_color = AppTheme.PRIMARY_ACCENT, 
            hover_color = AppTheme.HOVER_ACCENT, # Color a pasar raton
            text_color = "#ffffff", 
            border_width = 0, 
            **kwargs # Sobrescribir parametros si es necesario 
            )


class Panel(ctk.CTkFrame):
    """
    Contenedor con barra de título integrada.
    
    Proporciona un frame con una barra de título consistente,
    
    Parámetros
    ----------
    master : ctk.CTkBaseClass
        Widget padre donde se colocará el panel.
    title : str
        Texto del título a mostrar en la barra superior.
    **kwargs
        Argumentos adicionales para CTkFrame.
    
    Atributos
    ---------
    title_label : ctk.CTkLabel
        Label con el título del panel (accesible para modificación).
    
    Ejemplos
    --------
    >>> panel = Panel(window, "Configuración")
    >>> button = ctk.CTkButton(panel, text="OK")
    >>> button.pack()
    
    Notas
    -----
    El título se crea automáticamente en una barra superior con
    estilo consistente. Los widgets hijos deben añadirse después
    de la creación.
    """

    def __init__(self, master: ctk.CTkBaseClass, title: str, **kwargs):

        # Crear el frame con estilo predefenido
        super().__init__(
            master, 
            corner_radius = 8, 
            fg_color = AppTheme.SECONDERY_BACKGROUND, 
            border_width = 1, 
            border_color = AppTheme.BORDER, 
            **kwargs
            )
        
        # Crear la barra del titulo automaticamente
        self._create_title_bar(title)
    
    def _create_title_bar(self, title: str) -> None:
        """
        Crear la barra del título del panel.

        Parámetros
        ----------
        title: str
            Texto del título a mostrar.
        
        Notas
        -----
        La barra tiene altura fija.
        """

        # Frame de la barra de título
        title_bar = ctk.CTkFrame(
            self, 
            g_color = AppTheme.PRIMARY_BACKGROUND, 
            corner_radius = 6, 
            height = 38
            )
        
        title_bar.pack(fill = "x", padx = 2, pady = 2)

        # Mantiene altura fija (no se ajusta al contenido)
        title_bar.propagate(False)

        # Label del título (guardado en self para poder modificarlo después)
        self.title_label  = ctk.CTkLabel(
            title_bar, 
            text = title, 
            font = ("Orbitron", 12, "bold"), 
            text_color = AppTheme.PRIMARY_TEXT)

        # anchor="w" = alinea a la izquierda (west)
        self.title_label.pack(pady = 10, padx = 15, anchor = "w")


class LoadingIndicator(ctk.CTkFrame):
    """
    Indicador de carga con barra de progreso animada.
    
    Proporciona feedback visual durante operaciones largas mediante
    una barra de progreso en modo indeterminado y etiquetas informativas.
    
    Parámetros
    ----------
    master : ctk.CTkBaseClass
        Widget padre donde se colocará el indicador.
    **kwargs
        Argumentos adicionales para CTkFrame.
    
    Atributos
    ---------
    label : ctk.CTkLabel
        Label principal con texto "Cargando datos...".
    progress : ctk.CTkProgressBar
        Barra de progreso en modo indeterminado.
    status_label : ctk.CTkLabel
        Label de estado con texto adicional.
    
    Métodos
    -------
    stop()
        Detiene la animación de la barra de progreso.
    
    Ejemplos
    --------
    >>> indicator = LoadingIndicator(window)
    >>> indicator.place(relx=0.5, rely=0.5, anchor="center")
    >>> # ... operación larga ...
    >>> indicator.stop()
    >>> indicator.destroy()
    
    Notas
    -----
    La animación se inicia automáticamente al crear el widget.
    """

    def __init__(self, master : ctk.CTkBaseClass, **kwargs):

        # Crear el frame contenedor con borde de color
        super().__init__(
            master, 
            fg_color = AppTheme.SECONDERY_BACKGROUND, 
            corner_radius = 8, 
            border_width = 2, 
            border_color = AppTheme.PRIMARY_ACCENT, 
            **kwargs
            )
        
        # Crear todos los elementos visuales
        self._create_user_interface()

        # Inicializar la animacion de la barra de progresso
        self.progress_bar.start()

    def _create_user_interface(self) -> None:
        """
        Crear los elementos visuales del indicador.
        
        Organizar la creación de label, barra de progreso y label de estado
        mediante métodos especializados.
        """

        self._create_label()
        self._create_progress_bar()
        self._create_status_label()

    def _create_label(self) -> None:
        """
        Crear la etiqueta principal.

        Mostrar el texto "Cargando datos..." en la parte superior
        del indicador.
        """

        self.label = ctk.CTkLabel(
            self, 
            text = "Cargando datos...", 
            font = ("Orbitron", 12, "bold"), 
            text_color = AppTheme.PRIMARY_TEXT
            )
        
        # pady=(20, 10) = 20px arriba, 10px abajo
        self.label.pack(pady = (20, 10))

    def _create_progress_bar(self) -> None:
        """
        Crear la barra de progreso.
        
        Configurar una barra en modo indeterminado (animación continua).
        """

        self.progress_bar = ctk.CTkProgressBar(
            self, 
            mode = "indeterminate", 
            progress_color = AppTheme.PRIMARY_ACCENT, 
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            height = 6, 
            corner_radius = 6
            )
        
        self.progress_bar.pack(fill = "x", padx = 30, pady = (0,20))
    
    def _create_status_label(self) -> None:
        """
        Crear la etiqueta de estado.
        
        Mostrar información adicional sobre el proceso en curso.
        """

        self.status_label = ctk.CTkLabel(
            self, 
            text = "Prcesando datos...", 
            font = AppConfig.SMALL_FONT, 
            text_color = AppTheme.SECONDARY_TEXT
            )
        
        self.status_label.pack(pady=(0,15))

    def stop(self) -> None:
        """
        Detener la animación de la barra de progreso.
        
        Ejemplos
        --------
        >>> indicator.stop()
        >>> indicator.destroy()

        Notas
        -----
        Debe llamarse antes de destruir el widget para evitar
        errores de referencia a widgets destruidos.
        """
        self.progress_bar.stop()
    

class NotificationWindow(ctk.CTkToplevel):
    """
    Ventana modal de notificación.
    
    Proporcionar una ventana de diálogo personalizada con diseño consistente,
    diferentes estilos según el tipo de notificación.
    
    Parámetros
    ----------
    parent : ctk.CTk
        Ventana padre sobre la que se mostrará la notificación.
    title : str
        Título de la notificación.
    message : str
        Mensaje descriptivo a mostrar.
    notification_type : str, opcional
        Tipo de notificación: 'success', 'error', 'warning' o 'info'.
        Por defecto 'info'.
    
    Atributos de clase
    ------------------
    WINDOW_WIDTH : int
        Ancho de la ventana de notificación (450 px).
    WINDOW_HEIGHT : int
        Alto de la ventana de notificación (180 px).
    NOTIFICATION_CONFIGS : dict
        Mapeo de tipos a configuración visual (color e icono).
    
    Métodos
    -------
    _configure_window()
        Configura propiedades básicas de la ventana.
    _center_window()
        Centra la ventana en la pantalla.
    _get_notification_config(notification_type)
        Obtiene la configuración visual según el tipo.
    _create_notification_interface(title, message, config)
        Crea todos los elementos de la interfaz.
    
    Ejemplos
    --------
    >>> NotificationWindow(
    ...     parent=app,
    ...     title="Operación Exitosa",
    ...     message="El archivo se cargó correctamente",
    ...     notification_type="success"
    ... )
    
    Notas
    -----
    La ventana es modal (bloquea interacción con la ventana padre).
    Se destruye automáticamente al hacer clic en el botón "ACEPTAR".
    """
    # Constantes de configuracion
    WINDOW_WIDTH = 450
    WINDOW_HIGHT = 180

    # Mapeo de tipos a configuracion visual
    NOTIFICATION_CONFIG = {
        "success": {"color": AppTheme.SUCCES, "icon": "✓"},
        "error": {"color": AppTheme.ERROR, "icon": "✗"},
        "waring": {"color": AppTheme.WARNING, "icon": "⚠"}, 
        "info": {"color": AppTheme.PRIMARY_ACCENT, "icono": "i"}
        }
    
    
    def __init__(
        self, 
        parent: ctk.CTk, 
        title: str, 
        message: str, 
        notification_type: str = "info"
        ):

    # Llamar al constructor de CTkToplevel para crear la ventana base   
        super.__init__(parent)

    # Configurar tamaño, titulo, etc
        self._configure_notification_window()

    # Calcular la posicion centrada en pantalla
        self._center_notification_window()
    
    # Obtener colores/icono según el tipo (success/error/etc)
        config = self._get_notification_config(notification_type)
    
    # Crear todo el contenido visual (header, mensaje, boton)
        self._create_user_interface(title, message, config)
    
    # Bloquear la ventana padre (modal)
        self._make_modal(parent) 

    def _configure_notification_window(self) -> None:
        """
        Configurar las propiedades básicas de la ventana.
        
        Establecer el título vacío, dimensiones fijas y deshabilita
        el redimensionamiento.
        """
        # Titulo vacío (no mostrar titulo en la barra)
        self.title("")

        # Establecer tamño fijo para la ventana
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HIGHT}")

        # Desactivar redimensionar la ventana (False, False) = no horizontal, no vertical
        self.resizable(False, False)

    def _center_notification_window(self) -> None:
        """
        Centrar la ventana en la pantalla.
        
        Calcular la posición x,y para que la ventana aparezca centrada
        en la pantalla del usuario.
        """
        # Forcar actualizacíon de geometria para obtener valores correctos
        self.update_idletasks()

        # Calcular la posicion X: (ancho_pantalla / 2) - (ancho_ventana / 2)
        x = (self.winfo_screenwidth() // 2) - (self.WINDOW_WIDTH // 2)

        # Calcular la posicion Y: (alto_pantalla / 2) - (alto_ventana / 2)
        y = (self.winfo_screenheight() // 2) - (self.WINDOW_HIGHT // 2)

        # Aplicar geometria: "ANCHOxALTO+X+Y"
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HIGHT}+{x}+{y}")
    
    def _get_notification_config(self, notification_type: str) -> dict:
        """
        Obtiener la configuración visual según el tipo de notificación.
    
        Parámetros
        ----------
        notification_type : str
            Tipo de notificación.
        
        Devuelve
        --------
        dict
            Diccionario con 'color' e 'icon' para el tipo especificado.
            Si el tipo no existe, devuelve la configuración de 'info'.
        
        Ejemplos
        --------
        >>> config = self._get_notification_config('success')
        >>> config['icon']
        '✓'
        """

        return self.NOTIFICATION_CONFIG.get(notification_type, self.NOTIFICATION_CONFIG["info"])
    
    def _create_notification_interface(self, title: str, message: str, config: dict) -> None:
        """
        Crear la interfaz completa de la notificación.
        
        Parámetros
        ----------
        title : str
            Título a mostrar.
        message : str
            Mensaje descriptivo.
        config : dict
            Configuración visual con 'color' e 'icon'.
        
        Notas
        -----
        Delega la creación a submétodos especializados para mantener
        responsabilidad única y facilitar mantenimiento.
        """
        # Extraer color e icono del diccionario de configuración
        accent_color = config["color"]

        # Crer frame principal (caja contenedora con borde de color)
        icon = config["icon"]

        # Crear header (barra superior con icono y título)
        main_frame = self._create_main_frame(accent_color)

        # Crear header (barra superior con icono y título)
        self._create_header(main_frame, title, icon, accent_color)

        # Crear area de mensaje (texto central)
        self._create_message_area(main_frame, message)
        
        # Crear botón de cerrar la ventana (botón "ACEPTAR")
        self._create_button(main_frame, accent_color)
    
    def _create_main_frame(self, border_color: str) -> ctk.CTkFrame:
        """
        Crear el frame principal con borde coloreado.
        
        Parámetros
        ----------
        border_color : str
            Color del borde en formato hexadecimal.
        
        Devuelve
        --------
        ctk.CTkFrame
            Frame principal configurado.
        """
        # Crear un frame (contenedor) dentro la ventana (self)
        frame = ctk.CTkFrame(
            self, # Padre = la ventana de notificacion
            fg_color = AppTheme.SECONDERY_BACKGROUND, 
            border_width = 2, 
            border_color = border_color
            )
        
        # .pack() posiciona el frame dentro de la ventana
        # fill = "both" -> rellena horizontal y vertical
        # expand = True -> toma espacio extra si existe
        # padx/pady -> margenes de 2px
        frame.pack(fill = "both", expand = True, padx = 2, pady = 2)

        return frame
    
    def _create_header(self, parent: ctk.CTkFrame, title: str, icon: str, color: str) -> None:
        """
        Crear la barra de título con icono.
        
        Parámetros
        ----------
        parent : ctk.CTkFrame
            Widget padre donde se añadirá el header.
        title : str
            Texto del título.
        icon : str
            Carácter Unicode del icono.
        color : str
            Color del texto en formato hexadecimal.
        """
        # Frame que contiene el header
        header_frame = ctk.CTkFrame(
            master = parent, 
            fg_color = AppTheme.PRIMARY_BACKGROUND, 
            height = 45
            )
        # fill = "x" = solo horizontal
        header_frame.pack(fill = "x") 

        # pack_propagate(False) = mantiene altura fija de 45px
        # Sin esto, el frame se ajustara al contenido
        header_frame.pack_propagate(False)

        # Label con icono + título
        # f"{icon}  {title}" = combina icono y título con 2 espacios
        title_label = ctk.CTkLabel(
            master = header_frame, 
            text = f"{icon} {title}", 
            font = ("Segoe UI", 13, "bold"), 
            text_color = color
            )
        
        # anchor="w" = alinea a la izquierda (west)
        title_label.pack(pady = 12, padx = 20, anchor = "w")

    def _create_message_area(self, parent: ctk.CTkFrame, message: str) -> None:
        """
        Crear el área de mensaje.
        
        Parámetros
        ----------
        parent : ctk.CTkFrame
            Widget padre donde se añadirá el área de mensaje.
        message : str
            Texto del mensaje a mostrar.
        """
        # Frame contenedor del mensaje (transparente)
        message_frame  = ctk.CTkFrame(parent, fg_color = "transparent")

        # pady=(15, 10) = 15px arriba, 10px abajo
        message_frame.pack(fill = "both", expand = True, padx = 20, pady = (15, 10))

        # Label con el mensaje
        message_label = ctk.CTkLabel(
            message_frame, 
            text = message, 
            font = AppConfig.BODY_FONT, 
            text_color = AppTheme.PRIMARY_TEXT, 
            wraplength = 400, 
            justify = "left"
            )
        message_label.pack()
    
    def _create_button(self, parent: ctk.CTkFrame, color: str) -> None:
        """
        Crear el botón de cierre.
        
        Parámetros
        ----------
        parent : ctk.CTkFrame
            Widget padre donde se añadirá el botón.
        color : str
            Color del botón en formato hexadecimal.
        """
        # Frame contenedor del boton
        button_frame = ctk.CTkFrame(parent, fg_color = "transparent")

        # pady=(0, 15) = 0px arriba, 15px abajo
        button_frame.pack(fill = "both", padx = 20, pady = (0, 15))

        # Botón de cierre
        close_button = ctk.CTkButton(
            button_frame, 
            text = "ACEPTAR", 
            font = ("Orbitron", 10, "bold"), 
            fg_color = color, 
            hover_color = color, 
            text_color = "#ffffff", 
            height = 32, 
            corner_radius = 6, 
            command = self.destroy
            )
        
        # side="right" = alinea botón a la derecha
        close_button.pack(side = "right")
    
    def _make_modal(self, parent: ctk.CTk) -> None:
        """
        Hace la ventana modal.
        
        Bloquea la interacción con la ventana padre hasta que
        se cierre esta notificación.
        
        Parámetros
        ----------
        parent : ctk.CTk
            Ventana padre que será bloqueada.
        """
        # Establecer relación padre-hijo (siempre encima, se minimizan juntos)
        self.transient(parent)

        # Bloquear interacción con otras ventanas (MODAL)
        self.grab_set()