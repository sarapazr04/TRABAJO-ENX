"""
Componentes para la interfaz gráfica.
Autor: youssef-nabaha

Clases
------
AppTheme
    Paleta de colores y constantes visuales.
AppConfig
    Configuraciones globales de la aplicación.
"""

import customtkinter as ctk
from typing import Optional, Callable

class AppTheme:
    """
    Paleta de colores y constantes visuales de la GUI.
    
    Centraliza todos los colores utilizados en la interfaz para mantener
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
    
    Centraliza constantes de configuración como fuentes, dimensiones
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
    
