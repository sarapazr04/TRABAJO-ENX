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

    def _create_control_panel(self) -> None:
        """Crear el panel de control con botones y estadisticas."""
        control_panel = Panel(self, "Carga de datasets")
        control_panel.pack(
            fill = "x",
            padx = AppConfig.PADDING,
            pady=(AppConfig.PADDING, 10)
        )
        
        self._create_button_section(control_panel)
        self._create_stats_section(control_panel)

    def _create_button_section(self, parent: Panel) -> None:
        """Crear la sección de botón y visualización de ruta."""
        button_frame = ctk.CTkFrame(parent, fg_color = "transparent")
        button_frame.pack(fill = "x", padx = 20, pady = (15, 10))
        
        self._create_upload_button(button_frame)
        self._create_path_display(button_frame)
    
    def _create_upload_button(self, parent: ctk.CTkFrame) -> None:
        """Crear el botón de carga de archivos."""
        self.upload_button = UploadButton(
            parent,
            text = "Cargar Archivo",
            command = self._load_file
        )
        self.upload_button.pack(side = "left", padx = (0, 15))
    
    def _create_path_display(self, parent: ctk.CTkFrame) -> None:
        """Crear el frame de visualización de ruta del archivo."""
        self.path_frame = ctk.CTkFrame(
            parent,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        self.path_frame.pack(side = "left", fill = "x", expand = True)
        
        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text = "Ningún archivo seleccionado",
            font = AppConfig.BODY_FONT,
            text_color = AppTheme.DIM_TEXT,
            anchor = "center",
            justify = "center"
        )
        self.path_label.pack(pady = 10, padx = 15, fill = "x", expand = True)
    
    def _create_stats_section(self, parent: Panel) -> None:
        """Crear la sección de estadísticas del dataset."""
        self.stats_frame = ctk.CTkFrame(
            parent,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6
        )
        self.stats_frame.pack(fill = "x", padx = 20, pady = (5, 15))
        
        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text = "",
            font = AppConfig.MONO_FONT,
            text_color = AppTheme.SECONDARY_TEXT
        )
        self.stats_label.pack(pady = 8, padx = 15)

    def _load_file(self) -> None:
        """
        Iniciar el proceso de carga de archivo.
        
        Delega la carga pesada a un thread separado para no bloquear la GUI.
        """
        file_path = self._select_file()
        
        if file_path is None:
            return
        
        self._prepare_for_loading()
        self._start_loading_thread(file_path)
    
    def _select_file(self) -> Optional[str]:
        """
        Abrir el diálogo de selección de archivo.
        
        Returns:
            Ruta del archivo seleccionado o None si se cancela.
        """
        return filedialog.askopenfilename(
            title = "Seleccionar archivo de datos",
            filetypes = AppConfig.ALLOWED_EXTENTIONS
        )
    
    def _prepare_for_loading(self) -> None:
        """Preparar la interfaz para el proceso de carga."""
        self._show_loading_indicator()
        self._disable_load_button()

    def _disable_load_button(self) -> None:
        """Deshabilitar el botón de carga durante el proceso."""
        self.upload_button.configure(state = "disabled", text = "Cargando...")
    
    def _enable_load_button(self) -> None:
        """Rehabilitar el botón de carga."""
        self.upload_button.configure(state = "normal", text = "Cargar Archivo")
    
    def _start_loading_thread(self, file_path: str) -> None:
        """
        Iniciar un thread para la carga del archivo.
        
        Args:
            file_path: Ruta del archivo a cargar
        """
        thread = threading.Thread(
            target = self._load_file_thread,
            args = (file_path,),
            daemon = True
        )
        thread.start()
    
    def _load_file_thread(self, file_path: str) -> None:
        """
        Thread worker para la importación de datos.
        
        Ejecutar la operación pesada en segundo plano y notifica
        al hilo principal mediante callbacks.
        
        Args:
            file_path: Ruta del archivo a importar
        """
        try:
            df, preview = import_data(file_path)
            self.after(0, self._on_load_success, file_path, df)

        except Exception as e:
            self.after(0, self._on_load_error, str(e))
    
    def _on_load_success(self, file_path: str, dataframe: pd.DataFrame) -> None:
        """
        Callback ejecutado tras carga exitosa.
        
        Args:
            file_path: Ruta del archivo cargado
            dataframe: DataFrame con los datos
        """
        self._update_application_state(file_path, dataframe)
        self._update_user_interface_after_load(file_path, dataframe)
        self._show_success_notification(dataframe)
    
    def _update_application_state(self,file_path: str,dataframe: pd.DataFrame) -> None:
        """Actualizar el estado interno del software."""
        self.current_file_path = file_path
        self.current_dataframe = dataframe
    
    def _update_user_interface_after_load(self, file_path: str, dataframe: pd.DataFrame) -> None:
        """Actualizar todos los elementos de la interfaz tras la carga."""
        self._hide_loading_indicator()
        self._update_file_path_display(file_path)
        self._update_statistics(dataframe)
        self._display_data(dataframe)
        self._enable_load_button()
    
    def _show_success_notification(self, dataframe: pd.DataFrame) -> None:
        """Mostrar notificación de carga exitosa."""    
        rows, cols = dataframe.shape
        NotificationWindow(
            self,
            "Carga Exitosa",
            f"Archivo cargado correctamente\n\n{rows:,} filas × {cols} columnas",
            "success"
        )
    
    def _on_load_error(self, error_message: str) -> None:
        """
        Callback ejecutado si hay error en la carga.
        
        Args:
            error_message: Descripción del error
        """
        self._hide_loading_indicator()
        self._enable_load_button()
        
        NotificationWindow(
            self,
            "Error de Carga",
            f"No se puede cargar el archivo:\n\n{error_message}",
            "error"
        )
    
    def _show_loading_indicator(self) -> None:
        """Mostrar el indicador de carga centrado."""
        if self.loading_indicator is not None:
            self.loading_indicator.destroy()
        
        self.loading_indicator = LoadingIndicator(self)
        self.loading_indicator.place(relx = 0.5, rely = 0.5, anchor = "center")
    
    def _hide_loading_indicator(self) -> None:
        """Ocultar y destruir el indicador de carga."""
        if self.loading_indicator is not None:
            self.loading_indicator.stop()
            self.loading_indicator.destroy()
            self.loading_indicator = None

    def _update_file_path_display(self, file_path: str) -> None:
        """
        Actualizar la visualización de la ruta del archivo.
        
        Args:
            file_path: Ruta completa del archivo
        """
        file_name = Path(file_path).name
        display_text = f"ARCHIVO: {file_name}\nRUTA: {file_path}"
        
        self.path_label.configure(
            text = display_text,
            text_color = AppTheme.PRIMARY_ACCENT,
            justify = "center"
        )
    
    def _update_statistics(self, dataframe: pd.DataFrame) -> None:
        """
        Actualizar las estadísticas del dataset.
        
        Args:
            dataframe: DataFrame con los datos cargados
        """
        stats_text = self._format_statistics(dataframe)
        self.stats_label.configure(text = stats_text)
    
    def _format_statistics(self, dataframe: pd.DataFrame) -> str:
        """
        Formatear las estadísticas del dataset.
        
        Args:
            dataframe: DataFrame con los datos
            
        Returns:
            Cadena formateada con las estadísticas
        """
        rows, cols = dataframe.shape
        memory_mb = dataframe.memory_usage(deep = True).sum() / 1024**2
        
        return (
            f"Filas: {rows:,}  |  Columnas: {cols}  |  "
            f"Memoria: {memory_mb:.2f} MB"
        )

    def _create_data_panel(self) -> None:
        """Crear el panel principal de visualización de datos."""
        data_panel = Panel(self, "Visualización de Datos")
        data_panel.pack(
            fill = "both",
            expand = True,
            padx = AppConfig.PADDING,
            pady = (0, AppConfig.PADDING)
        )
        
        self._create_table_container(data_panel)
        self._create_empty_state()
    
    def _create_table_container(self, parent: Panel) -> None:
        """Crear los contenedores para la tabla de datos."""
        self.table_outer_frame = ctk.CTkFrame(
            parent,
            fg_color = "transparent"
        )
        self.table_outer_frame.pack(
            fill = "both",
            expand = True,
            padx = 15,
            pady = (10, 15)
        )
        
        self.table_container = ctk.CTkFrame(
            self.table_outer_frame,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        self.table_container.pack(fill = "both", expand = True)
    
    def _create_empty_state(self) -> None:
        """Crear el mensaje de estado vacío."""
        self.empty_state_label = ctk.CTkLabel(
            self.table_container,
            text = "Selecciona un archivo para visualizar los datos",
            font = ("Segoe UI", 13),
            text_color = AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx = 0.5, rely = 0.5, anchor = "center")