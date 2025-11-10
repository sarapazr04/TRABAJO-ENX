"""
Módulo de selección de columnas y preprocesamiento.

Proporciona interfaz para seleccionar columnas de entrada/salida
y preprocesar datos con valores faltantes.
"""

import customtkinter as ctk
import pandas as pd
from pandas.api.types import is_numeric_dtype
import threading
from .components import (
    NotificationWindow, Panel, AppTheme, AppConfig, UploadButton, LoadingIndicator
)


# ================================================================
# FRAME DE CHECKBOXES SCROLLABLE
# ================================================================

class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    """
    Frame scrollable con checkboxes para selección múltiple de columnas.

    Parámetros
    ----------
    master : widget
        Widget padre
    title : str
        Título del frame
    dataframe : pd.DataFrame
        DataFrame del que extraer las columnas
    """

    def __init__(self, master, title, dataframe):
        super().__init__(
            master,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )

        self.checkboxes = {}
        self.dataframe = dataframe
        self.has_title = bool(title)

        # Título (opcional)
        if title:
            title_label = ctk.CTkLabel(
                self,
                text=title,
                font=("Orbitron", 13, "bold"),
                text_color=AppTheme.PRIMARY_TEXT
            )
            title_label.pack(pady=(15, 10), padx=15, anchor="w")

        # Crear checkboxes para cada columna
        for i, column in enumerate(dataframe.columns):
            # Si no hay título, agregar padding extra al primer checkbox
            pady_top = 15 if (not self.has_title and i == 0) else 5
            self._create_checkbox(column, pady_top)

    def _create_checkbox(self, column, pady_top=5):
        """Crear un checkbox para una columna"""
        var = ctk.BooleanVar(value=False)

        checkbox = ctk.CTkCheckBox(
            self,
            text=column,
            variable=var,
            font=AppConfig.BODY_FONT,
            fg_color=AppTheme.PRIMARY_ACCENT,
            hover_color=AppTheme.HOVER_ACCENT,
            border_color=AppTheme.BORDER
        )
        checkbox.pack(pady=(pady_top, 5), padx=20, anchor="w")

        self.checkboxes[column] = var

    def get(self):
        """
        Obtener lista de columnas seleccionadas.

        Returns
        -------
        list
            Lista con nombres de columnas seleccionadas
        """
        return [col for col, var in self.checkboxes.items() if var.get()]

    def set(self, columns):
        """
        Establecer columnas seleccionadas.

        Parameters
        ----------
        columns : list
            Lista de columnas a seleccionar
        """
        for col, var in self.checkboxes.items():
            var.set(col in columns)


# ================================================================
# FRAME DE SELECCIÓN SIMPLE DE COLUMNA
# ================================================================

class ColumnFrame(ctk.CTkFrame):
    """
    Frame con menú desplegable para seleccionar una columna.

    Parámetros
    ----------
    master : widget
        Widget padre
    title : str
        Título del frame
    dataframe : pd.DataFrame
        DataFrame del que extraer las columnas
    command : callable, opcional
        Función callback cuando se selecciona una columna
    """

    def __init__(self, master, title, dataframe, command=None):
        super().__init__(
            master,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )

        # Título (opcional)
        if title:
            self.label = ctk.CTkLabel(
                self,
                text=title,
                font=("Orbitron", 13, "bold"),
                text_color=AppTheme.PRIMARY_TEXT
            )
            self.label.pack(padx=15, pady=(15, 10), anchor="w")

        # Menú desplegable
        columnas = list(dataframe.columns)
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=columnas,
            command=command,
            font=AppConfig.BODY_FONT,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            button_color=AppTheme.PRIMARY_ACCENT,
            button_hover_color=AppTheme.HOVER_ACCENT,
            dropdown_fg_color=AppTheme.SECONDARY_BACKGROUND,
            dropdown_hover_color=AppTheme.TERTIARY_BACKGROUND
        )
        # Si no hay título, agregar padding arriba
        pady_top = 0 if title else 15
        self.option_menu.pack(padx=15, pady=(pady_top, 15), fill="x")

    def get(self):
        """Obtener la columna seleccionada"""
        return self.option_menu.get()

    def set(self, value):
        """Establecer la columna seleccionada"""
        self.option_menu.set(value)


# ================================================================
# PANEL DE PREPROCESAMIENTO
# ================================================================

class PreprocessingPanel:
    """
    Panel para preprocesar datos con valores faltantes.

    Parámetros
    ----------
    master : widget
        Widget padre
    selected_columns : list
        Lista de columnas seleccionadas para preprocesar
    app : DataLoaderApp
        Referencia a la aplicación principal
    master_panel : SelectionPanel
        Panel padre con acceso al DataFrame
    """

    def __init__(self, master, selected_columns, app, master_panel):
        self.master = master
        self.selected_columns = selected_columns
        self.app = app
        self.master_panel = master_panel
        self.elements = []
        self.nas_stats = None

    def _create_preprocessing_panel(self):
        """Crear el panel principal de preprocesamiento"""
        preprocessing_panel = Panel(self.master, "Preprocesamiento de Datos")

        # Primero crear la sección de estadísticas (esto calcula self.nas_stats)
        self._create_na_stats_section(preprocessing_panel)

        # AHORA verificar si hay valores faltantes (después de calcular)
        nas_total = self._sum_nan(self.nas_stats) if self.nas_stats else 0

        # Solo mostrar opciones y botones de preprocesamiento si hay NaN
        if nas_total > 0:
            self._create_options_section(preprocessing_panel)
            self._create_action_buttons(preprocessing_panel)
        else:
            # Si no hay NaN, mostrar botón para continuar directamente
            self._continue_without_preprocessing()

        return preprocessing_panel

    def _create_na_stats_section(self, master):
        """Crear sección con estadísticas de valores faltantes"""
        stats_frame = ctk.CTkFrame(
            master,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        stats_frame.pack(fill="x", padx=15, pady=(10, 10))

        # Calcular estadísticas
        self.nas_stats = self._count_nan_df(
            self.master_panel.df[self.selected_columns]
        )
        nas_total = self._sum_nan(self.nas_stats)
        nas_columns = self._nan_columns(self.nas_stats)

        # Título
        title_label = ctk.CTkLabel(
            stats_frame,
            text="Estadísticas de Valores Faltantes",
            font=("Orbitron", 13, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        title_label.pack(pady=(12, 8), padx=15, anchor="w")

        # Información
        if nas_total > 0:
            info_text = (
                f"Total de N/A: {nas_total}\n"
                f"Columnas afectadas: {', '.join(nas_columns)}"
            )
            color = AppTheme.WARNING
        else:
            info_text = "✓ No hay valores faltantes en las columnas seleccionadas"
            color = AppTheme.SUCCES

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text=info_text,
            font=AppConfig.BODY_FONT,
            text_color=color,
            justify="left"
        )
        self.stats_label.pack(pady=(0, 12), padx=15, anchor="w")
        self.elements.append(self.stats_label)

    def _create_options_section(self, master):
        """Crear sección con opciones de preprocesamiento"""
        options_frame = ctk.CTkFrame(
            master,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        options_frame.pack(fill="x", padx=15, pady=(0, 10))

        # Título
        title_label = ctk.CTkLabel(
            options_frame,
            text="⚙️ Seleccione una opción",
            font=("Orbitron", 13, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        title_label.pack(pady=(15, 10), padx=15, anchor="w")

        # Variable para radio buttons
        self.option_var = ctk.StringVar(value="")

        # Opciones
        optiones = [
            ("Eliminar filas", "drop"),
            ("Rellenar con Media", "mean"),
            ("Rellenar con Mediana", "median"),
            ("Rellenar con Constante", "constant")
        ]

        for text, value in optiones:
            radio = ctk.CTkRadioButton(
                options_frame,
                text=text,
                value=value,
                variable=self.option_var,
                font=AppConfig.BODY_FONT,
                fg_color=AppTheme.PRIMARY_ACCENT,
                hover_color=AppTheme.HOVER_ACCENT,
                border_color=AppTheme.BORDER
            )
            radio.pack(pady=5, padx=20, anchor="w")

        # Campo de entrada para constante
        self.constant_entry = ctk.CTkEntry(
            options_frame,
            placeholder_text="Valor constante (ej: 0)",
            font=AppConfig.BODY_FONT,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_color=AppTheme.BORDER,
            height=32
        )
        self.constant_entry.pack(pady=(5, 15), padx=40, fill="x")

    def _create_action_buttons(self, master):
        """Crear botones de acción"""
        button_frame = ctk.CTkFrame(master, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Botón Aplicar
        self.apply_button = UploadButton(
            button_frame,
            text="Aplicar",
            command=self._apply_preprocessing
        )
        self.apply_button.pack(side="right", padx=(10, 0))

        # Botón Resetear
        reset_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self._cancel_preprocessing,
            font=("Orbitron", 11, "bold"),
            height=AppConfig.BUTTON_HEIGHT,
            corner_radius=6,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            hover_color=AppTheme.HOVER_ACCENT,
            text_color=AppTheme.PRIMARY_TEXT
        )
        reset_button.pack(side="right")

    def _continue_without_preprocessing(self):
        """Continuar cuando no hay valores faltantes e ir directo a división"""
        # Registrar el dataframe como preprocesado (aunque no se modificó)
        self.app.set_preprocessed_df(self.master_panel.df)

        NotificationWindow(
            self.app,
            "Datos Listos",
            "No se detectaron valores faltantes.\n"
            "Los datos están listos para dividir en entrenamiento y test.",
            "success"
        )

    def _apply_preprocessing(self):
        self.apply_button.configure(state="disabled")

        # Crear indicador con texto personalizado
        self.loading_indicator = LoadingIndicator(self.app)
        self.loading_indicator.label.configure(text="Procesando datos...")
        self.loading_indicator.status_label.configure(text="Por favor espere mientras se aplican los cambios.")
        self.loading_indicator.place(relx=0.5, rely=0.5, anchor="center")
         
        # Forzar actualización de GUI antes de bloquear
        self.app.update_idletasks()

         # Ejecutar en un hilo secundario
        thread = threading.Thread(
            # Función a ejecutar en segundo plano
            target=self._apply_preprocessing_thread,
            args=(),
            daemon=True
        )
        thread.start()

    def _apply_preprocessing_thread(self):
        """Aplicar el preprocesamiento según la opción seleccionada (en hilo)."""
        option = self.option_var.get()

        # Validar selección
        # Validar selección
        if not option:
            self.app.after(0, lambda: NotificationWindow(
                self.app,
                "Error de Validación",
                "Debe seleccionar una opción de preprocesamiento.",
                "warning"
            ))
            self.app.after(0, self._hide_loading_indicator)
            self.app.after(0, lambda: self.apply_button.configure(state="normal"))
            return
        

        # Verificar valores faltantes
        df_subset = self.master_panel.df[self.selected_columns]
        if not df_subset.isnull().any().any():
            self.app.after(0, lambda: NotificationWindow(
                self.app,
                "Sin Valores Faltantes",
                "Las columnas seleccionadas no contienen valores faltantes.",
                "info"
            ))
            self.app.after(0, self._hide_loading_indicator)
            self.app.after(0, lambda: self.apply_button.configure(state="normal"))
            return
        
         #  Ejecutar la lógica del preprocesado en el hilo principal
        self.app.after(0, lambda: self._apply_preprocessing_logic(option))

        #  Al terminar, cerrar el indicador y reactivar botón
        self.app.after(0, self._hide_loading_indicator)
        self.app.after(0, lambda: self.apply_button.configure(state="normal"))
    
    def _hide_loading_indicator(self):
        if hasattr(self, "loading_indicator") and self.loading_indicator:
            try:
                self.loading_indicator.stop()
                self.loading_indicator.destroy()
            except Exception:
                pass
            self.loading_indicator = None
    
    def _apply_preprocessing_logic(self, option):
        """Aplica el preprocesamiento sin modificar la GUI directamente."""
        if option == "drop":
            self._drop_na()
        elif option == "mean":
            self._fill_with_mean()
        elif option == "median":
            self._fill_with_median()
        elif option == "constant":
            self._fill_with_constant()


    def _drop_na(self):
        """Eliminar filas con valores faltantes"""
        rows_before = len(self.master_panel.df)
        self.master_panel.df = self.master_panel.df.dropna(
            subset=self.selected_columns
        )
        rows_after = len(self.master_panel.df)
        rows_deleted = rows_before - rows_after

        # Actualizar aplicación principal
        self.app.current_dataframe = self.master_panel.df
        self.app._display_data(self.master_panel.df)
        self.app._update_statistics(self.master_panel.df)

        NotificationWindow(
            self.app,
            "Preprocesado Completado",
            f"Se eliminaron {rows_deleted} fila(s) con valores faltantes.\n\n"
            f"Filas restantes: {rows_after:,}",
            "success"
        )

        # Actualizar estadísticas
        self._update_stats()
        self.app.set_preprocessed_df(self.master_panel.df)

    def _fill_with_mean(self):
        """Rellenar valores faltantes con la media"""
        df = self.master_panel.df
        numeric_cols = df[self.selected_columns].select_dtypes(
            include=['number']
        ).columns.tolist()

        if not numeric_cols:
            NotificationWindow(
                self.app,
                "Error",
                "No hay columnas numéricas en la selección para calcular la media.",
                "warning"
            )
            return

        for col in numeric_cols:
            if df[col].isnull().any():
                mean_value = df[col].mean()
                df[col] = df[col].fillna(mean_value)

        # Actualizar aplicación principal
        self.app.current_dataframe = df
        self.app._display_data(df)
        self.app._update_statistics(df)

        NotificationWindow(
            self.app,
            "Preprocesado Completado",
            f"Se rellenaron valores faltantes con la media en {len(numeric_cols)} columna(s).",
            "success"
        )

        # Actualizar estadísticas
        self._update_stats()
        self.app.set_preprocessed_df(self.master_panel.df)

    def _fill_with_median(self):
        """Rellenar valores faltantes con la mediana"""
        df = self.master_panel.df
        numeric_cols = df[self.selected_columns].select_dtypes(
            include=['number']
        ).columns.tolist()

        if not numeric_cols:
            NotificationWindow(
                self.app,
                "Error",
                "No hay columnas numéricas en la selección para calcular la mediana.",
                "warning"
            )
            return

        for col in numeric_cols:
            if df[col].isnull().any():
                median_value = df[col].median()
                df[col] = df[col].fillna(median_value)

        # Actualizar aplicación principal
        self.app.current_dataframe = df
        self.app._display_data(df)
        self.app._update_statistics(df)

        NotificationWindow(
            self.app,
            "Preprocesado Completado",
            f"Se rellenaron valores faltantes con la mediana en {len(numeric_cols)} columna(s).",
            "success"
        )

        # Actualizar estadísticas
        self._update_stats()
        self.app.set_preprocessed_df(self.master_panel.df)

    def _fill_with_constant(self):
        """Rellenar valores faltantes con una constante"""
        constant = self.constant_entry.get().strip()

        if not constant:
            NotificationWindow(
                self.app,
                "Error de Validación",
                "Debe introducir un valor constante.",
                "warning"
            )
            return

        df = self.master_panel.df

        # Intentar convertir a número
        try:
            constant = float(constant)
        except ValueError:
            pass  # Usar como string

        # Rellenar solo columnas seleccionadas
        for col in self.selected_columns:
            if df[col].isnull().any():
                df[col] = df[col].fillna(constant)

        # Actualizar aplicación principal
        self.app.current_dataframe = df
        self.app._display_data(df)
        self.app._update_statistics(df)

        NotificationWindow(
            self.app,
            "Preprocesado Completado",
            f"Se rellenaron valores faltantes con: '{constant}'",
            "success"
        )

        # Actualizar estadísticas
        self._update_stats()
        self.app.set_preprocessed_df(self.master_panel.df)

    def _cancel_preprocessing(self):
        """Cancelar el preprocesamiento"""
        self.option_var.set("")
        self.constant_entry.delete(0, 'end')

    def _update_stats(self):
        """Actualizar las estadísticas mostradas"""
        self.nas_stats = self._count_nan_df(
            self.master_panel.df[self.selected_columns]
        )
        nas_total = self._sum_nan(self.nas_stats)
        nas_columns = self._nan_columns(self.nas_stats)

        if nas_total > 0:
            info_text = (
                f"Total de N/A: {nas_total}\n"
                f"Columnas afectadas: {', '.join(nas_columns)}"
            )
            color = AppTheme.WARNING
        else:
            info_text = "✓ No hay valores faltantes en las columnas seleccionadas"
            color = AppTheme.SUCCES

        self.stats_label.configure(text=info_text, text_color=color)

    def _detect_nan(self, df):
        """Detectar y notificar valores NaN"""
        nas_columns = self._count_nan_df(df)
        nas_total = self._sum_nan(nas_columns)

        if nas_columns:
            NotificationWindow(
                self.app,
                "Valores NaN Detectados",
                f"Hay {len(nas_columns)} columna(s) con valores NaN.\n"
                f"Total de NaNs: {nas_total}",
                "warning"
            )

    # Métodos auxiliares
    def _count_nan_df(self, df):
        """Contar valores NaN por columna"""
        nas_columns = []
        columns_with_nas = df.columns[df.isna().any()].tolist()

        for column in columns_with_nas:
            nan_count = df[column].isna().sum()
            nas_columns.append([nan_count, column])

        return nas_columns

    def _sum_nan(self, nan_list):
        """Sumar total de NaN"""
        return sum(item[0] for item in nan_list)

    def _nan_columns(self, nan_list):
        """Obtener nombres de columnas con NaN"""
        return [item[1] for item in nan_list]


# ================================================================
# PANEL DE SELECCIÓN
# ================================================================

class SelectionPanel:
    """
    Panel principal para selección de columnas y preprocesamiento.

    Parámetros
    ----------
    master : widget
        Widget padre
    df : pd.DataFrame
        DataFrame a procesar
    app : DataLoaderApp
        Referencia a la aplicación principal
    """

    def __init__(self, master, df, app):
        self.master = master
        self.df = df
        self.app = app
        self.col_entrada = []
        self.processed_df = None

    def _crear_interfaz(self):
        """Crear la interfaz de selección de datos"""
        select_panel = Panel(self.master, "Selección de Datos")

        # Contenedor principal con altura fija
        main_container = ctk.CTkFrame(
            select_panel,
            fg_color="transparent",
            height=350
        )
        main_container.pack(fill="x", padx=10, pady=10)
        main_container.pack_propagate(False)

        # Contenedor para paneles lado a lado
        frame_in_out = ctk.CTkFrame(main_container, fg_color="transparent")
        frame_in_out.pack(expand=True, fill="both")
        frame_in_out.grid_columnconfigure(0, weight=1)
        frame_in_out.grid_columnconfigure(1, weight=1)

        # ═══════════════════════════════════════════════════════════
        # PANEL IZQUIERDO: Datos de Entrada
        # ═══════════════════════════════════════════════════════════
        entrada_container = ctk.CTkFrame(
            frame_in_out,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        entrada_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Título del panel de entrada
        entrada_title = ctk.CTkLabel(
            entrada_container,
            text="Datos de Entrada",
            font=("Orbitron", 14, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        entrada_title.pack(fill="x", padx=8, pady=8)

        # Frame scrollable de checkboxes (con aislamiento de scroll)
        self.frame_entrada = ScrollableCheckboxFrame(
            entrada_container,
            "",  # Sin título porque ya lo tiene el contenedor
            self.df
        )
        self.frame_entrada.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # ═══════════════════════════════════════════════════════════
        # PANEL DERECHO: Datos de Salida
        # ═══════════════════════════════════════════════════════════
        salida_container = ctk.CTkFrame(
            frame_in_out,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        salida_container.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Título del panel de salida
        salida_title = ctk.CTkLabel(
            salida_container,
            text="Datos de Salida",
            font=("Orbitron", 14, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        salida_title.pack(fill="x", padx=8, pady=8)

        # Selector de columna de salida
        self.frame_salida = ColumnFrame(
            salida_container,
            "",  # Sin título porque ya lo tiene el contenedor
            self.df
        )
        self.frame_salida.pack(fill="x", padx=8, pady=(0, 8))

        # ═══════════════════════════════════════════════════════════
        # BOTÓN DE CONFIRMACIÓN
        # ═══════════════════════════════════════════════════════════

        button_container = ctk.CTkFrame(
            salida_container,
            fg_color="transparent"
        )
        button_container.pack(fill="both", expand=True, padx=6, pady=(0, 8))

        self.button = UploadButton(
            button_container,
            text="Confirmar",
            command=self.button_callback
        )
        self.button.place(relx=0.5, rely=0.6, anchor="center")

        return select_panel

    def button_callback(self):
        """Callback del botón de procesar datos"""
        columnas_entrada = self.frame_entrada.get()

        if not columnas_entrada:
            NotificationWindow(
                self.app,
                "Error de Selección",
                "Debe seleccionar al menos una columna de entrada.",
                "warning"
            )
            return

        self.columnas_entrada = columnas_entrada
        self.columna_salida = self.frame_salida.get()

        # Validar que todas las columnas sean numéricas
        columnas_invalidas = [
            col for col in self.columnas_entrada + [self.columna_salida]
            if not is_numeric_dtype(self.df[col])
        ]

        if columnas_invalidas:
            NotificationWindow(
                self.app,
                "Error de Tipo de Datos",
                f"Las siguientes columnas contienen valores no numéricos:\n\n"
                f"{', '.join(columnas_invalidas)}\n\n"
                "Solo se permiten columnas numéricas para crear el modelo lineal.",
                "error"
            )
            return

        # Reiniciar paneles previos si existen
        if hasattr(self.app, "reset_panels"):
            self.app.reset_panels()

        self._display_data()

    def _create_empty_panel(self):
        """Crear panel vacío con mensaje de estado inicial"""
        self.table_outer_frame = ctk.CTkFrame(
            self.master, fg_color="transparent"
        )
        self.table_outer_frame.pack(fill="both", expand=True, padx=(10, 0))

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
            text="Seleccione columnas \n para Procesar Datos",
            font=("Segoe UI", 13),
            text_color=AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx=0.5, rely=0.5, anchor="center")

    def _display_data(self):
        """Mostrar panel de preprocesamiento con las columnas seleccionadas"""
        # Ocultar mensaje
        try:
            if self.empty_state_label.winfo_exists():
                self.empty_state_label.place_forget()
        except Exception:
            pass

        # Destruir contenedor anterior
        self.table_container.destroy()

        # Destruir panel de preprocesamiento anterior si existe
        try:
            if hasattr(self, 'pre_options') and self.pre_options.winfo_exists():
                self.pre_options.pack_forget()
                self.pre_options.destroy()
        except Exception:
            pass

        # Preparar columnas a procesar
        columnas_procesar = self.columnas_entrada.copy()
        if self.columna_salida not in columnas_procesar:
            columnas_procesar.append(self.columna_salida)

        # Crear panel de preprocesamiento
        self.pre_panel = PreprocessingPanel(
            self.table_outer_frame,
            columnas_procesar,
            self.app,
            self
        )

        # Detectar NaN y crear panel
        self.pre_panel._detect_nan(self.df[columnas_procesar])
        self.pre_options = self.pre_panel._create_preprocessing_panel()
        self.pre_options.pack(fill="both", expand=True)


# ================================================================
# TESTING
# ================================================================

if __name__ == "__main__":
    # DataFrame de prueba
    df = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Nombre': ['Azúcar', 'Café', None, 'Té', 'Sal'],
        'Precio': [28.5, 45.0, 32.0, None, 20.0],
        'Cantidad': [34, 12, None, 20, 15]
    })

    app = ctk.CTk()
    app.title("Selector de Datos")
    app.geometry("1200x700")
    ctk.set_appearance_mode("dark")

    panel = SelectionPanel(app, df, app)
    interface = panel._crear_interfaz()
    interface.pack(fill="both", expand=True, side="left", padx=20, pady=20)
    panel._create_empty_panel()

    app.mainloop()
