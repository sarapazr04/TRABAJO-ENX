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

sys.path.append(str(Path(__file__).parent.parent / "data_import"))
from data_import.importer import import_data


class DataLoaderApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self._configure_window()
        self._initialize_state()
        self._setup_user_interface()
    
    def _configure_window(self) -> None:
        self.title("LUNEX DATASETS LOADER")
        self.geometry(
            f"{AppConfig.WINDOW_WIDTH}x{AppConfig.WINDOW_HEIGHT}"
        )
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def _initialize_state(self) -> None:
        self.current_file_path: Optional[str] = None
        self.current_dataframe: Optional[pd.DataFrame] = None
        self.loading_indicator: Optional[LoadingIndicator] = None
    
    def _setup_user_interface(self) -> None:
        self.configure(fg_color = AppTheme.PRIMARY_BACKGROUND)
        
        self._create_header()
        self._create_control_panel()
        self._create_data_panel()
    
