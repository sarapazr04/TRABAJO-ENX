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

        self.title("LUNEX DATASETS LOADER")
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
    
