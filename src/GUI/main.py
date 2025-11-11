"""
GUI principal para cargar y visualizar datasets.
Este archivo controla la ventana principal y la carga de archivos.
"""

import customtkinter as ctk
from tkinter import filedialog
import threading  # Para ejecutar código en segundo plano
from .components import (
    AppTheme, AppConfig, NotificationWindow,
    UploadButton, Panel, LoadingIndicator
)
from .selection_columns import SelectionPanel
from .data_display import DataDisplayManager
from data_import.importer import import_data
from .data_split import DataSplitPanel
from .desc_model import DescriptBox
from .model_linear import LinearModelPanel
from .welcome_message import WelcomeMessage
from .load_model import LoadModelPanel


class DataLoaderApp(ctk.CTk):
    """
    Ventana principal de la GUI.

    Esta clase crea la interfaz y gestiona la carga de archivos.
    """

    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.title("LUNEX DATASETS LOADER")
        self.geometry("1400x800")
        ctk.set_appearance_mode("dark")

        self.current_file_path = None    # Ruta del archivo cargado
        self.current_dataframe = None    # Los datos (DataFrame)
        self.loading_indicator = None    # Círculo de carga
        self.display_manager = None      # Gestor de la tabla
        self.is_preprocessed = False
        self.preprocessed_df = None
        self.train_df = None
        self.test_df = None
        self._split_panel_frame = None  # contenedor para recrear el panel
        self.selection_panel = None
        self.selection_frame = None  # Frame exterior del panel de seleccion
        self.description_frame = None

        # Crear la interfaz
        self.configure(fg_color=AppTheme.PRIMARY_BACKGROUND)
        self.welcome_window = WelcomeMessage(self)
        self.ext_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.ext_frame.pack(fill="both", expand=True)

        # Esto reduce el lag cuando hay graficos de matplotlib
        self.ext_frame._parent_canvas.configure(scrollregion=(0, 0, 0, 2000))

        # Pestañas: Crear Modelo / Cargar Modelo
        self._create_tabs()

        self._create_control_panel()
        self._create_data_panel()
        self._create_status_bar()

        # Configurar protocolo de cierre para limpiar recursos
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    # ================================================================
    # PESTAÑAS SUPERIORES: Crear modelo / Cargar modelo
    # ================================================================
    def _create_tabs(self):
        """
        Crea la barra de pestañas tipo navegador (Crear modelo / Cargar modelo)
        y los contenedores de contenido para cada pestaña.
        """
        # Barra de pestañas
        self.tab_bar = ctk.CTkFrame(
            self.ext_frame,
            fg_color="transparent"
        )
        self.tab_bar.pack(fill="x", padx=20, pady=(10, 0))

        # Botón-pestaña: Crear modelo (activa por defecto)
        self.tab_create_button = ctk.CTkButton(
            self.tab_bar,
            text="Crear Modelo",
            command=self._show_create_tab,
            font=("Orbitron", 12, "bold"),
            height=32,
            corner_radius=6,
            fg_color=AppTheme.PRIMARY_ACCENT,
            hover_color=AppTheme.HOVER_ACCENT,
            text_color="#ffffff",
            border_width=0
        )
        self.tab_create_button.pack(side="left", padx=(0, 5))

        # Botón-pestaña: Cargar modelo
        self.tab_load_button = ctk.CTkButton(
            self.tab_bar,
            text="Cargar Modelo",
            command=self._show_load_tab,
            font=("Orbitron", 12, "bold"),
            height=32,
            corner_radius=6,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            hover_color=AppTheme.TERTIARY_BACKGROUND,
            text_color=AppTheme.PRIMARY_TEXT,
            border_width=0
        )
        self.tab_load_button.pack(side="left")

        # Contenedor de contenido para "Crear modelo"
        self.create_mode_frame = ctk.CTkFrame(
            self.ext_frame,
            fg_color="transparent"
        )
        self.create_mode_frame.pack(
            fill="both", expand=True, padx=0, pady=(5, 0)
        )

        # Contenedor de contenido para "Cargar modelo" (de momento oculto)
        self.load_mode_frame = ctk.CTkFrame(
            self.ext_frame,
            fg_color="transparent"
        )

    # ================================================================
    # CAMBIO DE PESTAÑA
    # ================================================================
    def _show_create_tab(self):
        """Mostrar la pestaña 'Crear modelo' y ocultar 'Cargar modelo'."""
        # Activar colores de pestañas
        self.tab_create_button.configure(
            fg_color=AppTheme.PRIMARY_ACCENT,
            text_color="#ffffff"
        )
        self.tab_load_button.configure(
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            text_color=AppTheme.PRIMARY_TEXT
        )

        #  Mostrar frame de 'Crear modelo' (sin reconstruir nada)
        if not self.create_mode_frame.winfo_ismapped():
            self.create_mode_frame.pack(
                fill="both", expand=True, padx=0, pady=(5, 0))

        #  Ocultar frame de 'Cargar modelo' (sin destruir)
        if self.load_mode_frame.winfo_ismapped():
            self.load_mode_frame.pack_forget()

    def _show_load_tab(self):
        """Mostrar la pestaña 'Cargar modelo' y ocultar 'Crear modelo'."""
        # Activar colores de pestañas
        self.tab_load_button.configure(
            fg_color=AppTheme.PRIMARY_ACCENT,
            text_color="#ffffff"
        )
        self.tab_create_button.configure(
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            text_color=AppTheme.PRIMARY_TEXT
        )

        #  Ocultar 'Crear modelo' (solo ocultar)
        if self.create_mode_frame.winfo_ismapped():
            self.create_mode_frame.pack_forget()

        #  Mostrar 'Cargar modelo' (solo crear una vez)
        if not hasattr(self, "_load_model_panel_created"):
            from .load_model import LoadModelPanel
            load_panel = LoadModelPanel(self.load_mode_frame, self)
            load_panel.pack(fill="both", expand=True, padx=20, pady=(10, 20))
            self._load_model_panel_created = True

        if not self.load_mode_frame.winfo_ismapped():
            self.load_mode_frame.pack(
                fill="both", expand=True, padx=0, pady=(5, 0))

    def _create_load_tab_placeholder(self):

        # Limpiar contenido anterior (por si se vuelve a entrar a la pestaña)
        for w in self.load_mode_frame.winfo_children():
            w.destroy()

        # Crear y empaquetar el panel de carga de modelo
        load_panel = LoadModelPanel(self.load_mode_frame, self)
        load_panel.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    # ================================================================
    # PANEL DE CONTROLES : Botón de carga y estadísticas
    # ================================================================

    def _create_control_panel(self):
        """Crear el panel con el botón de cargar y las estadísticas"""
        control_panel = ctk.CTkFrame(
            self.create_mode_frame,
            corner_radius=8,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        control_panel.pack(fill="x", padx=20, pady=(20, 10))

        self._create_button_section(control_panel)

    def _create_button_section(self, parent):
        """Crear el botón de carga y mostrar la ruta del archivo"""
        # Frame contenedor
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(15, 15))

        # Botón de cargar
        self.upload_button = UploadButton(
            button_frame,
            text="Cargar Datos",
            command=self._load_file  # Función a ejecutar al hacer clic
        )
        self.upload_button.pack(side="right", padx=(15, 0))

        # Label de la etiqueta "RUTA:"
        self.tag_label = ctk.CTkLabel(
            button_frame,
            text="RUTA :",
            font=("Orbitron", 15, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.tag_label.pack(side="left", padx=(0, 10))

        # Frame para mostrar la ruta
        self.path_frame = ctk.CTkFrame(
            button_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        # expand = True = toma espacio extra
        self.path_frame.pack(side="left", fill="x", expand=True)

        # Label con la ruta
        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="Ningún archivo seleccionado",
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.DIM_TEXT
        )
        self.path_label.pack(pady=10, padx=15)

    def _create_status_bar(self):
        """Crear el área de estadísticas del dataset"""
        self.status_bar = ctk.CTkFrame(
            self,
            height=35,
            corner_radius=0,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_color=AppTheme.BORDER,
            border_width=1
        )

        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)

        self.stats_label = ctk.CTkLabel(
            self.status_bar,
            text="Ningún archivo cargado",
            font=("Segoe UI", 11),
            text_color=AppTheme.SECONDARY_TEXT,
            anchor="w"
        )
        self.stats_label.pack(side="left", pady=0, padx=15)

    # ================================================================
    # CARGAR DATOS : Con threading para no bloquear la ventana
    # ================================================================

    def _load_file(self):
        """
        Se ejecuta cuando haces clic en 'Cargar Datos'.
        Usa threading para no congelar la ventana mientras carga.
        """
        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=AppConfig.ALLOWED_EXTENTIONS
        )

        if not file_path:
            return

        self._show_loading_indicator()
        self.upload_button.configure(state="disabled", text="Cargando...")

        # Crear hilo para cargar en segundo plano
        thread = threading.Thread(
            # Función a ejecutar en segundo plano
            target=self._load_file_thread,
            # Argumentos (IMPORTANTE: tupla con coma)
            args=(file_path,),
            daemon=True
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
            # No puedes modificar la GUI desde un thread.
            # Poara eso usamos .after()
            self.after(0, self._on_load_success, file_path, df)

        except Exception as e:
            # Si falla, llamar función de error en el hilo principal
            self.after(0, self._on_load_error, str(e))

    def _on_load_success(self, file_path, dataframe):
        """
        Se ejecuta cuando el archivo se carga correctamente.
        Actualiza toda la interfaz con los nuevos datos.
        """
        # Limpiar paneles antiguos (split y modelo) si existen
        if hasattr(self, "_split_panel_frame") and self._split_panel_frame:
            try:
                self._split_panel_frame.destroy()
            except Exception:
                pass
            self._split_panel_frame = None

        if hasattr(self, "_model_panel_frame") and self._model_panel_frame:
            try:
                self._model_panel_frame.destroy()
            except Exception:
                pass
            self._model_panel_frame = None

        # Guardar los datos en variables de instancia
        self.current_file_path = file_path
        self.current_dataframe = dataframe

        # Reset de estado de procesamiento y split
        self.is_preprocessed = False
        self.preprocessed_df = None
        self.train_df = None
        self.test_df = None
        if self._split_panel_frame is not None and self._split_panel_frame.winfo_exists():
            self._split_panel_frame.destroy()
            self._split_panel_frame = None

        # Actualizar interfaz
        self._hide_loading_indicator()
        self._update_file_path_display(file_path)
        self._update_statistics(dataframe)
        self._display_data(dataframe)
        self._create_selection_panel(dataframe)
        self.upload_button.configure(state="normal", text="Cargar Datos")

        rows, cols = dataframe.shape
        self.after(100, lambda: self._show_success_notification(rows, cols))

    def _show_success_notification(self, rows, cols):
        """Muestra la notificación de éxito de carga"""
        try:
            NotificationWindow(
                self,
                "Carga Exitosa",
                f"Archivo cargado correctamente\n\n{rows:,} filas x {cols} columnas",
                "success"
            )
        except Exception as e:
            # Si falla la notificación, solo imprimir el error
            print(f"Error mostrando notificación: {e}")

    def _on_load_error(self, error_message):
        """Se ejecuta cuando hay un error al cargar el archivo"""
        self._hide_loading_indicator()
        self.upload_button.configure(state="normal", text="Cargar Datos")

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
        # Si ya existe, destruirlo primero
        if self.loading_indicator is not None:
            self.loading_indicator.destroy()

        self.loading_indicator = LoadingIndicator(self)

        # relx/rely = posición relativa (0.5 = 50% = centro)
        self.loading_indicator.place(relx=0.5, rely=0.5, anchor="center")

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
        display_text = f"{file_path}"

        self.path_label.configure(
            text=display_text,
            text_color=AppTheme.PRIMARY_ACCENT
        )

    def _update_statistics(self, dataframe):
        """Actualizar las estadísticas (filas, columnas, memoria)"""
        rows, cols = dataframe.shape  # Obtener dimensiones
        memory_mb = dataframe.memory_usage(
            deep=True).sum() / 1024**2  # Calcular memoria en MB

        stats_text = f"Filas: {rows:,}  |  Columnas: {cols}  |  Memoria: {memory_mb:.2f} MB"
        self.stats_label.configure(text=stats_text)

    # ================================================================
    # PANEL DE CONTROLES : Botón de carga y estadísticas
    # ================================================================

    def _create_selection_panel(self, dataframe):
        """
        Crea el panel de seleccion de columnas.

        Si ya existe un panel previo, lo destruye para evitar duplicados.

        Parameters
        ----------
        dataframe : pd.DataFrame
            DataFrame con los datos cargados.
        """
        # Destruir frame anterior completo si existe
        if self.selection_frame is not None:
            try:
                self.selection_frame.destroy()
            except Exception:
                pass

        # Crear nuevo frame exterior
        self.selection_frame = ctk.CTkFrame(
            self.create_mode_frame, fg_color="transparent")
        self.selection_frame.pack(fill="x", expand=True, padx=20, pady=(0, 20))

        # Crear panel de seleccion con orden correcto de parametros
        # Nota: SelectionPanel espera (master, df, app) en el archivo original
        self.selection_panel = SelectionPanel(
            self.selection_frame, dataframe, self)

        # Crear y mostrar interfaz usando el metodo original _crear_interfaz()
        selection_interface = self.selection_panel._crear_interfaz()
        selection_interface.pack(
            fill="both", expand=True, side="left", padx=0, pady=0)

        # Crear panel vacio inicial
        self.selection_panel._create_empty_panel()

    def set_preprocessed_df(self, df):
        """Registrar el dataframe preprocesado y mostrar el panel"""
        self.is_preprocessed = True
        self.preprocessed_df = df

        # IMPORTANTE: Destruir el panel del modelo si existe
        # (porque al cambiar el preprocesamiento, el modelo anterior ya no es válido)
        if hasattr(self, '_model_panel_frame') and self._model_panel_frame:
            try:
                if self._model_panel_frame.winfo_exists():
                    self._model_panel_frame.destroy()
                    self._model_panel_frame = None
            except Exception:
                pass

        self._create_split_panel()

    def _create_split_panel(self):
        """Crear y mostrar el panel para dividir el dataset en train/test."""
        # Destruir/recrear si ya existe (por si se vuelve a preprocesar)
        if self._split_panel_frame is not None and self._split_panel_frame.winfo_exists():
            self._split_panel_frame.destroy()

        self._split_panel_frame = ctk.CTkFrame(
            self.create_mode_frame, fg_color="transparent")
        self._split_panel_frame.pack(
            fill="x", expand=True, padx=20, pady=(0, 20))

        split_panel = DataSplitPanel(self._split_panel_frame, self)
        split_panel.pack(fill="both", expand=True, padx=10, pady=10)

    # ================================================================
    # PANEL DE DESCRIPCIÓN : Cuadro de texto
    # ================================================================
    def _create_description_panel(self):
        """
        Crea el panel de descripción del modelo.

        Si ya existe un panel previo, lo destruye para evitar duplicados.

        Parameters
        ----------

        """
        # Destruir frame anterior completo si existe
        if self.description_frame is not None:
            try:
                self.description_frame.destroy()
            except Exception:
                pass
        self.description_panel = ctk.CTkFrame(
            self.create_mode_frame, fg_color="transparent")
        self.description_panel.pack(fill="x",
                                    expand=True,
                                    padx=20,
                                    pady=(0, 20))
        # Crear y obtener el panel
        self.description_panel = DescriptBox(self.description_panel)

        interface = self.description_panel._create_description_panel()

        # Empaquetar el panel para que sea visible
        interface.pack(fill="both", expand=True, padx=10, pady=10)

    # ================================================================
    # PANEL DE DATOS : Donde se muestra la tabla
    # ================================================================

    def _create_data_panel(self):
        """Crear el panel donde se mostrará la tabla de datos"""
        data_panel = Panel(self.create_mode_frame, "Visualización de Datos")
        data_panel.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Frame exterior (transparente, no se toca)
        self.table_outer_frame = ctk.CTkFrame(
            data_panel, fg_color="transparent")
        self.table_outer_frame.pack(
            fill="both", expand=True, padx=15, pady=(10, 15))

        # Contenedor de la tabla (este se puede destruir y recrear)
        self.table_container = ctk.CTkFrame(
            self.table_outer_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        self.table_container.pack(fill="both", expand=True)

        self.empty_state_label = ctk.CTkLabel(
            self.table_container,
            text="Selecciona un archivo para visualizar los datos",
            font=("Segoe UI", 13),
            text_color=AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx=0.5, rely=0.5, anchor="center")

    def _display_data(self, dataframe):
        """
        Mostrar los datos en la tabla.
        Delega todo el trabajo al DataDisplayManager.
        """
        # Ocultar mensaje de "sin datos"
        try:
            # winfo_exists() verifica si el widget existe
            if self.empty_state_label.winfo_exists():
                # Ocultar (quitar del layout)
                self.empty_state_label.place_forget()
        except Exception:
            pass

        # Recrear el contenedor (limpieza completa)
        self.table_container.destroy()  # Destruir el anterior
        # Crear uno nuevo
        self.table_container = ctk.CTkFrame(
            self.table_outer_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        self.table_container.pack(fill="both", expand=True)

        # Crear gestor de visualización y mostrar datos
        self.display_manager = DataDisplayManager(
            self.table_container,
            dataframe
        )
        # Este método hace todo el trabajo
        self.display_manager.display()

    # ================================================================
    # PANEL DEL MODELO LINEAL
    # ================================================================

    def set_split_completed(self):
        """Llamado tras dividir datos para habilitar creación del modelo."""
        self._create_model_panel()

    def _create_model_panel(self):
        """Crear el panel para entrenar y evaluar modelo lineal."""
        # IMPORTANTE: Destruir panel anterior si existe para evitar duplicados
        if hasattr(self, '_model_panel_frame') and self._model_panel_frame:
            try:
                if self._model_panel_frame.winfo_exists():
                    self._model_panel_frame.destroy()
            except Exception:
                pass

        # Crear nuevo panel
        self._model_panel_frame = ctk.CTkFrame(
            self.create_mode_frame, fg_color="transparent")
        self._model_panel_frame.pack(
            fill="x", expand=True, padx=20, pady=(0, 20))
        model_panel = LinearModelPanel(self._model_panel_frame, self)
        model_panel.pack(fill="both", expand=True, padx=10, pady=10)

    # ================================================================
    # REINICIAR ESTADO: Eliminar paneles previos
    # ================================================================

    def reset_panels(self):
        """
        Reiniciar el estado interno de la aplicación y eliminar paneles previos.
        Se usa cuando el usuario quiere procesar un nuevo modelo desde cero.
        """
        #  Destruir el panel de división (train/test) si existe
        if hasattr(self, "_split_panel_frame") and self._split_panel_frame:
            try:
                self._split_panel_frame.destroy()
            except Exception:
                pass
            self._split_panel_frame = None

        #  Destruir el panel del modelo lineal si existe
        if hasattr(self, "_model_panel_frame") and self._model_panel_frame:
            try:
                self._model_panel_frame.destroy()
            except Exception:
                pass
            self._model_panel_frame = None

        #  Reiniciar estado interno
        self.train_df = None
        self.test_df = None
        self.is_preprocessed = False
        self.preprocessed_df = None

    # ================================================================
    # LIMPIEZA AL CERRAR LA GUI
    # ================================================================

    def _on_closing(self):
        """
        Limpia los recursos antes de cerrar la aplicación.
        """
        try:
            # Cerrar todas las figuras de matplotlib
            import matplotlib.pyplot as plt
            plt.close('all')
        except Exception:
            pass

        try:
            # Destruir paneles específicos que pueden tener recursos
            if hasattr(self, '_split_panel_frame') and self._split_panel_frame:
                self._split_panel_frame.destroy()

            if hasattr(self, '_model_panel_frame') and self._model_panel_frame:
                self._model_panel_frame.destroy()

            if hasattr(self, 'selection_frame') and self.selection_frame:
                self.selection_frame.destroy()
        except Exception:
            pass

        try:
            # Limpiar referencias a dataframes
            self.current_dataframe = None
            self.preprocessed_df = None
            self.train_df = None
            self.test_df = None
        except Exception:
            pass

        try:
            # Forzar recolección de basura antes de cerrar
            import gc
            gc.collect()
        except Exception:
            pass

        try:
            self.quit()
        except Exception:
            pass

        try:
            # Destruir la ventana después de salir del mainloop
            self.destroy()
        except Exception:
            pass


def main():
    app = DataLoaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()
