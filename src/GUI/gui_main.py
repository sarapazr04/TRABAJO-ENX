"""
Aplicación principal para la carga y visualización de datasets.

Autor: youssef-nabaha

Archivo principal con la logica de la aplicación.
"""

import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
import sys
from pathlib import Path
from typing import Optional
import pandas as pd
import threading
from tkinter import ttk

from gui_components import (
    AppTheme, AppConfig, NotificationWindow,
    UploadButton, Panel, LoadingIndicator
)

# Importar el modulo de importacion datos 
sys.path.append(str(Path(__file__).parent.parent / "data_import"))
from data_import.importer import import_data


class DataLoaderApp(ctk.CTk):
    """Aplicación principal para importación y visualización de datos."""
    
    def __init__(self):
        """Inicializar la aplicación y configura el estado inicial."""
        super().__init__()
        
        self._configure_window()
        self._initialize_state()
        self._setup_user_interface()
    
    def _configure_window(self) -> None:
        """Configurar las propiedades de la ventana principal."""

        self.title("LUNEX v1.0")
        self.geometry(
            f"{AppConfig.WINDOW_WIDTH}x{AppConfig.WINDOW_HEIGHT}"
        )
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def _initialize_state(self) -> None:
        """
        Inicializar el estado de la aplicación.
        
        Variables de instancia que mantienen el estado actual.
        """
        self.current_file_path: Optional[str] = None
        self.current_dataframe: Optional[pd.DataFrame] = None
        self.loading_indicator: Optional[LoadingIndicator] = None
    
    def _setup_user_interface(self) -> None:
        """Configurar todos los componentes de la GUI."""

        self.configure(fg_color = AppTheme.PRIMARY_BACKGROUND)
        
        self._create_header()
        self._create_control_panel()
        self._create_data_panel()

    def _create_header(self) -> None:
        """Crear el header superior con información de la GUI."""
        header_frame = self._create_header_frame()
        self._add_header_content(header_frame)

    def _create_header_frame(self) -> ctk.CTkFrame:
        """Crear y configurar el frame del header."""
        header_frame = ctk.CTkFrame(
            self,
            height = 100,
            corner_radius = 0,
            fg_color = AppTheme.SECONDERY_BACKGROUND
        )    
        header_frame.pack(fill = "x")
        header_frame.pack_propagate(False)

        return header_frame

    def _add_header_content(self, parent: ctk.CTkFrame) -> None:
        """Añadir el contenido textual al header."""
        title_label = ctk.CTkLabel(
            parent,
            text = "LUNEX DATASETS LOADER",
            font = AppConfig.TITLE_FONT,
            text_color = AppTheme.PRIMARY_TEXT
        )
        title_label.pack(pady = (25, 5))

        subtitle_label = ctk.CTkLabel(
            parent,
            text = "Sprint 1 - Historia #14 | Visualización de datasets",
            font = AppConfig.SMALL_FONT,
            text_color = AppTheme.SECONDARY_TEXT
        )
        subtitle_label.pack()