import customtkinter as ctk
from typing import Optional, Callable

class AppTheme:

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
    
