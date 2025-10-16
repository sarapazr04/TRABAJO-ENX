"""
GUI principal para cargar y visualizar datasets.
Este archivo controla la ventana principal y la carga de archivos.
"""

import customtkinter as ctk
from tkinter import filedialog
import threading  # Para ejecutar código en segundo plano
from pathlib import Path  # Para trabajar con rutas de archivos

from .components import (
    AppTheme, AppConfig, NotificationWindow,
    UploadButton, Panel, LoadingIndicator
)
from .data_display import DataDisplayManager
from data_import.importer import import_data


class DataLoaderApp(ctk.CTk):
    """
    Ventana principal de la GUI.
    
    Esta clase crea la interfaz y gestiona la carga de archivos.
    """

    def __init__(self):
        super().__init__()  

        # Configurar la ventana
        self.title("LUNEX v0.1.0")
        self.geometry("1400x800")
        ctk.set_appearance_mode("dark")

        self.current_file_path = None    # Ruta del archivo cargado
        self.current_dataframe = None    # Los datos (DataFrame)
        self.loading_indicator = None    # Círculo de carga
        self.display_manager = None      # Gestor de la tabla

        # Crear la interfaz
        self.configure(fg_color = AppTheme.PRIMARY_BACKGROUND)
        self._create_header()
        self._create_control_panel()
        self._create_data_panel()


    # ================================================================
    # HEADER : Barra superior con título
    # ================================================================

    def _create_header(self):
        """Crear la barra superior con el título"""
        # Frame del header
        header_frame = ctk.CTkFrame(
            self,
            height = 100,
            corner_radius = 0,
            fg_color = AppTheme.SECONDERY_BACKGROUND
        )
        header_frame.pack(fill = "x")  # fill = "x" = ocupa todo el ancho
        header_frame.pack_propagate(False)  # Mantener altura fija (no ajustar al contenido)

        # Título grande
        title_label = ctk.CTkLabel(
            header_frame,
            text = "LUNEX DATASETS LOADER",
            font = AppConfig.TITLE_FONT,
            text_color = AppTheme.PRIMARY_TEXT
        )
        title_label.pack(pady = (25, 5))  # pady = (arriba, abajo)

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text = "Sprint 1 - Historia #14 | Visualización de datasets",
            font = AppConfig.SMALL_FONT,
            text_color = AppTheme.SECONDARY_TEXT
        )
        subtitle_label.pack()

    # ================================================================
    # PANEL DE CONTROLES : Botón de carga y estadísticas
    # ================================================================

    def _create_control_panel(self):
        """Crear el panel con el botón de cargar y las estadísticas"""
        control_panel = Panel(self, "Carga de datasets")
        control_panel.pack(fill = "x", padx = 20, pady = (20, 10))

        self._create_button_section(control_panel)
        self._create_stats_section(control_panel)

    def _create_button_section(self, parent):
        """Crear el botón de carga y mostrar la ruta del archivo"""
        # Frame contenedor
        button_frame = ctk.CTkFrame(parent, fg_color = "transparent")
        button_frame.pack(fill = "x", padx = 20, pady = (15, 10))

        # Botón de cargar
        self.upload_button = UploadButton(
            button_frame,
            text = "Cargar Archivo",
            command = self._load_file  # Función a ejecutar al hacer clic
        )
        self.upload_button.pack(side = "left", padx = (0, 15))

        # Frame para mostrar la ruta
        self.path_frame = ctk.CTkFrame(
            button_frame,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        self.path_frame.pack(side = "left", fill = "x", expand = True)  # expand = True = toma espacio extra

        # Label con la ruta
        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text = "Ningún archivo seleccionado",
            font = AppConfig.BODY_FONT,
            text_color = AppTheme.DIM_TEXT
        )
        self.path_label.pack(pady = 10, padx = 15)

    def _create_stats_section(self, parent):
        """Crear el área de estadísticas del dataset"""
        self.stats_frame = ctk.CTkFrame(
            parent,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6
        )
        self.stats_frame.pack(fill = "x", padx = 20, pady = (5, 15))

        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text = "",  # Inicialmente vacio
            font = AppConfig.MONO_FONT,
            text_color = AppTheme.SECONDARY_TEXT
        )
        self.stats_label.pack(pady = 8, padx = 15)

    # ================================================================
    # CARGAR ARCHIVO : Con threading para no bloquear la ventana
    # ================================================================

    def _load_file(self):
        """
        Se ejecuta cuando haces clic en 'Cargar Archivo'.
        Usa threading para no congelar la ventana mientras carga.
        """
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(
            title = "Seleccionar archivo de datos",
            filetypes = AppConfig.ALLOWED_EXTENTIONS
        )

        if not file_path:
            return

        self._show_loading_indicator()
        self.upload_button.configure(state = "disabled", text = "Cargando...")

        # Crear hilo para cargar en segundo plano (daemon = True = se cierra con la app)
        thread = threading.Thread(
            target = self._load_file_thread,  # Función a ejecutar en segundo plano
            args = (file_path,),  # Argumentos (IMPORTANTE: tupla con coma)
            daemon = True
        )
        thread.start()  

    def _load_file_thread(self, file_path):
        """
        Esta función se ejecuta en segundo plano.
        Carga el archivo y avisa si funciona o falla.
        """
        try:
            # Intentar cargar el archivo
            df, preview = import_data(file_path)

            # Si funciona, llamar función de éxito en el hilo principal
            # self.after(0, ...) ejecuta la función en el hilo principal
            # No puedes modificar la GUI desde un thread, por eso usamos .after()
            self.after(0, self._on_load_success, file_path, df)

        except Exception as e:  
            # Si falla, llamar función de error en el hilo principal
            self.after(0, self._on_load_error, str(e))

    def _on_load_success(self, file_path, dataframe):
        """
        Se ejecuta cuando el archivo se carga correctamente.
        Actualiza toda la interfaz con los nuevos datos.
        """
        # Guardar los datos en variables de instancia
        self.current_file_path = file_path
        self.current_dataframe = dataframe

        # Actualizar interfaz
        self._hide_loading_indicator()
        self._update_file_path_display(file_path)
        self._update_statistics(dataframe)
        self._display_data(dataframe)
        self.upload_button.configure(state = "normal", text = "Cargar Archivo")

        # Mostrar notificación de éxito
        rows, cols = dataframe.shape  # .shape devuelve (filas, columnas)
        NotificationWindow(
            self,
            "Carga Exitosa",
            f"Archivo cargado correctamente\n\n{rows:,} filas x {cols} columnas",  # :, = separador de miles
            "success"
        )

    def _on_load_error(self, error_message):
        """Se ejecuta cuando hay un error al cargar el archivo"""
        self._hide_loading_indicator()
        self.upload_button.configure(state = "normal", text = "Cargar Archivo")

        NotificationWindow(
            self,
            "Error de Carga",
            f"No se puede cargar el archivo:\n\n{error_message}",
            "error"
        )

    # ================================================================
    # INDICADOR DE CARGA : Circulo que gira mientras carga
    # ================================================================

    def _show_loading_indicator(self):
        """Mostrar el círculo de carga en el centro"""
        if self.loading_indicator is not None:  # Si ya existe, destruirlo primero
            self.loading_indicator.destroy()

        self.loading_indicator = LoadingIndicator(self) 

        # relx/rely = posición relativa (0.5 = 50% = centro)
        self.loading_indicator.place(relx = 0.5, rely = 0.5, anchor = "center") 

    def _hide_loading_indicator(self):
        """Ocultar y destruir el círculo de carga"""
        if self.loading_indicator is not None:
            self.loading_indicator.stop()  # Detener animación
            self.loading_indicator.destroy()  # Eliminar widget
            self.loading_indicator = None  # Limpiar referencia

    # ================================================================
    # ACTUALIZAR INTERFAZ : Cambiar textos y estadisticas
    # ================================================================

    def _update_file_path_display(self, file_path):
        """Actualizar el texto que muestra la ruta del archivo"""
        file_name = Path(file_path).name  # .name extrae solo el nombre del archivo
        display_text = f"ARCHIVO: {file_name}\nRUTA: {file_path}"

        self.path_label.configure(
            text = display_text,
            text_color = AppTheme.PRIMARY_ACCENT
        )

    def _update_statistics(self, dataframe):
        """Actualizar las estadísticas (filas, columnas, memoria)"""
        rows, cols = dataframe.shape  # Obtener dimensiones
        memory_mb = dataframe.memory_usage(deep = True).sum() / 1024**2  # Calcular memoria en MB

        stats_text = f"Filas: {rows:,}  |  Columnas: {cols}  |  Memoria: {memory_mb:.2f} MB"
        self.stats_label.configure(text = stats_text)

    # ================================================================
    # PANEL DE DATOS : Donde se muestra la tabla
    # ================================================================

    def _create_data_panel(self):
        """Crear el panel donde se mostrará la tabla de datos"""
        data_panel = Panel(self, "Visualización de Datos")
        data_panel.pack(fill = "both", expand = True, padx = 20, pady = (0, 20))

        # Frame exterior (transparente, no se toca)
        self.table_outer_frame = ctk.CTkFrame(data_panel,fg_color = "transparent")
        self.table_outer_frame.pack(fill="both", expand = True, padx = 15, pady = (10, 15))

        # Contenedor de la tabla (este se puede destruir y recrear)
        self.table_container = ctk.CTkFrame(
            self.table_outer_frame,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        self.table_container.pack(fill = "both", expand = True)

        self.empty_state_label = ctk.CTkLabel(
            self.table_container,
            text = "Selecciona un archivo para visualizar los datos",
            font = ("Segoe UI", 13),
            text_color = AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx = 0.5, rely = 0.5, anchor = "center") 

    def _display_data(self, dataframe):
        """
        Mostrar los datos en la tabla.
        Delega todo el trabajo al DataDisplayManager.
        """
        # Ocultar mensaje de "sin datos"
        try:
            if self.empty_state_label.winfo_exists():  # winfo_exists() verifica si el widget existe
                self.empty_state_label.place_forget()  # Ocultar (quitar del layout)
        except:
            pass  

        # Recrear el contenedor (limpieza completa)
        self.table_container.destroy()  # Destruir el anterior
        # Crear uno nuevo
        self.table_container = ctk.CTkFrame(  
            self.table_outer_frame,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        self.table_container.pack(fill = "both", expand = True)

        # Crear gestor de visualización y mostrar datos 
        self.display_manager = DataDisplayManager(
            self.table_container,
            dataframe
        )
        # Este método hace todo el trabajo
        self.display_manager.display()  


def main():
    app = DataLoaderApp()
    app.mainloop()  


if __name__ == "__main__":  
    main()