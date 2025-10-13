"""
Estructura general para la interfaz gráfica.
Autor: youssef-nabaha

Clases
------
DataLoaderApp
    Lógica principal para la carga y visualización de datasets
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

from .components import (
    AppTheme, AppConfig, NotificationWindow,
    UploadButton, Panel, LoadingIndicator
)


sys.path.append(str(Path(__file__).resolve().parent.parent))
from data_import.importer import import_data

# ============================================================================
# APLICACIÓN PRINCIPAL
# ============================================================================

class DataLoaderApp(ctk.CTk):
    """Lógica para importación y visualización de datos."""
    
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

# ============================================================================
# HEADER
# ============================================================================

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

# ============================================================================
# SISTEMA DE CARGA CON THREADING
# ============================================================================
    
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
        ----
            dataframe: DataFrame con los datos
            
        Returns:
        -------
            Cadena formateada con las estadísticas
        """
        rows, cols = dataframe.shape
        memory_mb = dataframe.memory_usage(deep = True).sum() / 1024**2
        
        return (
            f"Filas: {rows:,}  |  Columnas: {cols}  |  "
            f"Memoria: {memory_mb:.2f} MB"
        )
    
# ============================================================================
# PANEL DE VISUALIZACIÓN DE DATOS
# ============================================================================

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

# ============================================================================
# VISUALIZACIÓN CON TREEVIEW
# ============================================================================
    
    def _format_cell_value(self, value) -> str:
        """
        Formatear un valor de celda individual.
        
        Args:
        ----
            value: Valor a formatear
            
        Returns:
        -------
            Cadena formateada
        """
        # Verificar si el valor es NaN (Not a Number / dato faltante)
        if pd.isna(value):
            return "N/A"
      
        elif isinstance(value, float):
            return f"{value:.4f}"
        
        else:
            return str(value)


    def _get_row_tag(self, index: int) -> str:
        """
        Determina la etiqueta de fila para alternar colores.
        
        Args:
        ----
            index: Indice de la fila
            
        Returns:
        -------
            Nombre de la etiqueta
        """
        # Alternar etiquetas: pares son "evenrow", impares son "oddrow"
        # Esto permite colorear filas alternadas en la tabla
        return "evenrow" if index % 2 == 0 else "oddrow"


    def _format_row_values(self, dataframe: pd.DataFrame, row_index: int) -> list:
        """
        Formatear los valores de una fila para mostrar.
        
        Args:
        ----
            dataframe: DataFrame fuente
            row_index: Índice de la fila
            
        Returns:
        -------
            Lista de valores formateados
        """
        
        values = []

        
        for col in dataframe.columns:
            # Obtener el valor de la celda en la fila y columna actual
            val = dataframe.iloc[row_index][col]

            formatted_val = self._format_cell_value(val)

            values.append(formatted_val)

        return values


    def _configure_row_tags(self, tree: ttk.Treeview) -> None:
        """Configurar los colores alternados de las filas."""

        # Configurar color de fondo para filas pares (gris medio)
        tree.tag_configure("evenrow", background = AppTheme.SECONDERY_BACKGROUND)

        # Configurar color de fondo para filas impares (gris oscuro)
        tree.tag_configure("oddrow", background = AppTheme.PRIMARY_BACKGROUND)


    def _configure_treeview_base_style(self, style: ttk.Style) -> None:
        """Configurar el estilo base del Treeview."""

        # Aplicar estilos base al widget Treeview
        style.configure(
            "Treeview",
            background = AppTheme.SECONDERY_BACKGROUND,     
            foreground = AppTheme.PRIMARY_TEXT,    
            fieldbackground = AppTheme.SECONDERY_BACKGROUND,
            borderwidth = 0,                  
            font = ("Segoe UI", 12),               
            rowheight = 24                                    
        )


    def _configure_treeview_heading_style(self, style: ttk.Style) -> None:
        """Configura el estilo de los encabezados."""

        # Aplicar estilos a los encabezados de columna
        style.configure(
            "Treeview.Heading",
            background = AppTheme.TERTIARY_BACKGROUND, 
            foreground = AppTheme.PRIMARY_TEXT,        
            borderwidth = 1,                            
            relief = "flat", # Sin efecto 3D (plano)
            font = ("Segoe UI", 13, "bold")            
        )


    def _configure_treeview_selection(self, style: ttk.Style) -> None:
        """Configurar los colores de selección y hover."""

        # Configurar colores cuando se selecciona una fila
        style.map(
            "Treeview",
            # Cuando una fila esta seleccionada: fondo azul
            background = [("selected", AppTheme.PRIMARY_ACCENT)],
            # Cuando una fila esta seleccionada: texto blanco
            foreground = [("selected", "#ffffff")]
        )


    def _configure_index_column(self, tree: ttk.Treeview) -> None:
        """Configurar la columna del indice."""

        # Configurar la columna del indice (primera columna "#0")
        tree.column("#0", width = 60, anchor = "center")  # Ancho 60px, texto centrado

        # Configurar el encabezado de la columna del indice
        tree.heading("#0", text = "INDEX", anchor = "center")  # Texto "INDEX" centrado


    def _configure_data_columns(self, tree: ttk.Treeview, dataframe: pd.DataFrame) -> None:
        """Configurar las columnas de datos."""

        for col in dataframe.columns:
            # Configurar propiedades de la columna
            tree.column(
                col,
                width = 150,      
                anchor = "center", 
                minwidth = 100    
            )

            # Configurar el encabezado de la columna
            tree.heading(
                col,
                text = str(col).upper(), 
                anchor = "center"         
            )


    def _apply_treeview_style(self) -> None:
        """
        Aplicar el estilo visual al Treeview.
        
        Configurar colores, fuentes y comportamiento de selección.
        """
        
        style = ttk.Style()

        # Usar tema "clam" (tema moderno y personalizable)
        style.theme_use("clam")

        # Aplicar los tres tipos de estilos configurados
        self._configure_treeview_base_style(style)      
        self._configure_treeview_heading_style(style) 
        self._configure_treeview_selection(style)    


    def _populate_treeview(self, tree: ttk.Treeview, dataframe: pd.DataFrame) -> None:
        """
        Insertar los datos en el Treeview.
        
        Args:
        ----
            tree: Widget Treeview
            dataframe: DataFrame con los datos
        """
       
        for idx in range(len(dataframe)):
            # Obtener los valores formateados de la fila actual
            values = self._format_row_values(dataframe, idx)

            # Determinar la etiqueta (par/impar) para colorear
            tag = self._get_row_tag(idx)

            
            tree.insert(
                "",              # Padre: "" significa nivel raiz
                "end",           
                text = str(idx),   
                values = values,  
                tags = (tag,)      # Etiqueta para aplicar color
            )

        # Configurar los colores de las etiquetas (pares/impares)
        self._configure_row_tags(tree)


    def _create_scrollbars(self, parent: tk.Frame) -> tuple[tk.Scrollbar, tk.Scrollbar]:
        """
        Crear las scrollbars vertical y horizontal.
        
        Returns:
        -------
            Tupla con (scrollbar_vertical, scrollbar_horizontal)
        """

        # Crear scrollbar vertical (orientacion vertical)
        vsb = tk.Scrollbar(parent, orient = "vertical")

        # Crear scrollbar horizontal (orientacion horizontal)
        hsb = tk.Scrollbar(parent, orient = "horizontal")

        return vsb, hsb


    def _layout_tree_and_scrollbars(
        self,
        parent: tk.Frame,
        tree: ttk.Treeview,
        vsb: tk.Scrollbar,
        hsb: tk.Scrollbar
    ) -> None:
        """Organizar el Treeview y scrollbars en el layout."""

        # Colocar el Treeview en la posicióon (0,0) del grid
        # sticky = "nsew" hace que se expanda en todas direcciones
        tree.grid(row = 0, column = 0, sticky = "nsew")

        # Colocar scrollbar vertical a la derecha del Treeview
        # sticky = "ns" hace que se expanda verticalmente (Norte-Sur)
        vsb.grid(row = 0, column = 1, sticky = "ns")

        # Colocar scrollbar horizontal debajo del Treeview
        # sticky = "ew" hace que se expanda horizontalmente (Este-Oeste)
        hsb.grid(row = 1, column = 0, sticky = "ew")

        # Configurar la fila 0 para que se expanda 
        parent.grid_rowconfigure(0, weight = 1)

        # Configurar la columna 0 para que se expanda 
        parent.grid_columnconfigure(0, weight = 1)


    def _create_tree(
        self,
        parent: tk.Frame,
        dataframe: pd.DataFrame,
        vsb: tk.Scrollbar,
        hsb: tk.Scrollbar
    ) -> ttk.Treeview:
        """Crear el Treeview y conectarlo con las scrollbars."""

        # Crear el widget Treeview con configuracion completa
        tree = ttk.Treeview(
            parent,                         
            columns = list(dataframe.columns), 
            show = "tree headings",            
            yscrollcommand = vsb.set,         # Conectar con scrollbar vertical
            xscrollcommand = hsb.set,         # Conectar con scrollbar horizontal
            selectmode = "browse"              # Modo: seleccionar una fila a la vez
        )

        # Configurar scrollbar vertical para controlar el Treeview
        vsb.config(command = tree.yview)

        # Configurar scrollbar horizontal para controlar el Treeview
        hsb.config(command = tree.xview)

        return tree


    def _setup_mouse_wheel_scroll(self, tree: ttk.Treeview) -> None:
        """
        Configurar el scroll con rueda del ratón.
        
        Compatible con Windows, macOS y Linux.
        
        Args:
        ----
            tree: Widget Treeview
        """
        
        def on_mousewheel(event):
            # Detectar scroll hacia abajo:
            # - event.num == 5: Linux (botón 5)
            # - event.delta < 0: Windows/macOS (delta negativo)
            if event.num == 5 or event.delta < 0:
                tree.yview_scroll(1, "units")  # Scroll 1 unidad hacia abajo

            # Detectar scroll hacia arriba:
            # - event.num == 4: Linux (botón 4)
            # - event.delta > 0: Windows/macOS (delta positivo)
            elif event.num == 4 or event.delta > 0:
                tree.yview_scroll(-1, "units")  # Scroll 1 unidad hacia arriba

        # Vincular evento de rueda del raton (Windows/macOS)
        tree.bind("<MouseWheel>", on_mousewheel)

        # Vincular evento de boton 4 del ratón (Linux - scroll arriba)
        tree.bind("<Button-4>", on_mousewheel)

        # Vincular evento de boton 5 del ratón (Linux - scroll abajo)
        tree.bind("<Button-5>", on_mousewheel)


    def _configure_treeview(self, tree: ttk.Treeview, dataframe: pd.DataFrame) -> None:
        """
        Configurar columnas y estilo del Treeview.
        
        Args:
        ----
            tree: Widget Treeview
            dataframe: DataFrame para extraer nombres de columnas
        """
        self._apply_treeview_style()

        self._configure_index_column(tree)

        self._configure_data_columns(tree, dataframe)


    def _create_treeview_widget(self, dataframe: pd.DataFrame) -> ttk.Treeview:
        """
        Crear el widget Treeview con scrollbars.
        
        Args:
        ----
            dataframe: DataFrame para configurar columnas
            
        Returns:
        -------
            Widget Treeview configurado
        """
        # Crear un Frame contenedor para el Treeview y scrollbars
        tree_frame = tk.Frame(
            self.table_container,              
            bg = AppTheme.PRIMARY_BACKGROUND     
        )

        # Colocar el frame y hacerlo expandible
        tree_frame.pack(fill = "both", expand = True, padx = 8, pady = 8)

        # Crear las scrollbars vertical y horizontal
        vsb, hsb = self._create_scrollbars(tree_frame)

        # Crear el Treeview y conectarlo con las scrollbars
        tree = self._create_tree(tree_frame, dataframe, vsb, hsb)

        # Organizar el Treeview y scrollbars en el layout grid
        self._layout_tree_and_scrollbars(tree_frame, tree, vsb, hsb)

        return tree


    def _hide_empty_state(self) -> None:
        """Ocultar el mensaje de estado vacio si existe."""
        try:
            # Verificar si el label de estado vacoo existe
            if self.empty_state_label.winfo_exists():
                # Ocultar el label (quitar del layout)
                self.empty_state_label.place_forget()

        except Exception:
            pass  


    def _recreate_table_container(self) -> None:
        """
        Destruir y recrear el contenedor de la tabla.
        
        Refactorización: limpieza completa para evitar widgets huérfanos.
        """
        # Destruir el contenedor actual de la tabla
        # Esto elimina todos los widgets hijos también
        self.table_container.destroy()

        # Crear un nuevo contenedor de tabla limpio
        self.table_container = ctk.CTkFrame(
            self.table_outer_frame,                
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,                       
            border_width = 1,                        
            border_color = AppTheme.BORDER          
        )

        # Colocar el nuevo contenedor en el layout
        self.table_container.pack(fill = "both", expand = True)


    def _display_data(self, dataframe: pd.DataFrame) -> None:
        """
        Mostrar los datos en un Treeview optimizado.
        
        Utilizar virtualizacion para manejar datasets grandes eficientemente.
        
        Args:
        ----
            dataframe: DataFrame a visualizar
        """

        self._hide_empty_state()
        self._recreate_table_container()
        tree = self._create_treeview_widget(dataframe)
        self._configure_treeview(tree, dataframe)
        self._populate_treeview(tree, dataframe)
        self._setup_mouse_wheel_scroll(tree)
    
def main():
    """
    Función principal de la GUI.
    """
    app = DataLoaderApp()
    app.mainloop()


if __name__ == "__main__":
    main()