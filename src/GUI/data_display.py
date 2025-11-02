"""
Gestor de visualización de datos en tabla.
Este módulo se encarga de mostrar los datos en una tabla Treeview.
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd

from .components import AppTheme


class DataDisplayManager:
    """
    Gestor que muestra datos en una tabla Treeview.

    Esta clase hace todo lo relacionado con la tabla:
    - Crear el Treeview
    - Aplicar estilos
    - Insertar datos
    - Configurar scrollbars
    - Manejar scroll con rueda del ratón
    """

    def __init__(self, container, dataframe):

        self.container = container
        self.dataframe = dataframe
        self.tree = None

    def display(self):
        """
        Método principal: muestra los datos en la tabla.

        Este método hace todo el proceso:
        1. Crear el Treeview
        2. Configurar columnas y estilos
        3. Insertar los datos
        4. Configurar scroll
        """
        self.tree = self._create_treeview_widget()
        self._configure_treeview()
        self._populate_treeview()
        self._setup_mouse_wheel_scroll()

    # ================================================================
    # CREAR TREEVIEW : Tabla con scrollbars
    # ================================================================

    def _create_treeview_widget(self):
        """Crear el widget Treeview con sus scrollbars"""
        # Frame contenedor
        tree_frame = tk.Frame(
            self.container,
            bg=AppTheme.PRIMARY_BACKGROUND
        )
        tree_frame.pack(fill="both", expand=True, padx=8, pady=8)

        # Crear scrollbars (barras de desplazamiento)
        vertical_scroll_bar, horizontal_scroll_bar = self._create_scrollbars(
            tree_frame)

        # Crear Treeview (la tabla)
        tree = self._create_tree(
            tree_frame, vertical_scroll_bar, horizontal_scroll_bar)

        # Organizar todo con grid (sistema de cuadricula)
        self._layout_tree_and_scrollbars(
            tree_frame, tree, vertical_scroll_bar, horizontal_scroll_bar)

        return tree

    def _create_scrollbars(self, parent):
        """Crear las barras de desplazamiento (vertical y horizontal)"""
        vertical_scroll_bar = tk.Scrollbar(parent, orient="vertical")
        horizontal_scroll_bar = tk.Scrollbar(parent, orient="horizontal")
        return vertical_scroll_bar, horizontal_scroll_bar

    def _create_tree(self, parent, vertical_scroll_bar, horizontal_scroll_bar):
        """Crear el Treeview y conectarlo con las scrollbars"""
        tree = ttk.Treeview(
            parent,
            columns=list(self.dataframe.columns),
            # Mostrar indice y encabezados
            show="tree headings",
            # Conectar con scrollbar vertical
            yscrollcommand=vertical_scroll_bar.set,
            # Conectar con scrollbar horizontal
            xscrollcommand=horizontal_scroll_bar.set,
            # Solo puedes seleccionar una fila a la vez
            selectmode="browse"
        )

        # Conectar scrollbars con el Treeview (bidireccional)
        vertical_scroll_bar.config(command=tree.yview)
        horizontal_scroll_bar.config(command=tree.xview)

        return tree

    def _layout_tree_and_scrollbars(self,
                                    parent,
                                    tree,
                                    vertical_scroll_bar,
                                    horizontal_scroll_bar):
        """
        Organizar el Treeview y scrollbars en el layout.

        Usa grid para posicionar:
        - Treeview en (0,0)
        - Scrollbar vertical en (0,1)
        - Scrollbar horizontal en (1,0)
        """
        tree.grid(row=0, column=0,
                  sticky="nsew")  # sticky = se pega a todos los lados
        # ns = norte-sur (vertical)
        vertical_scroll_bar.grid(row=0, column=1, sticky="ns")
        # ew = este-oeste (horizontal)
        horizontal_scroll_bar.grid(row=1, column=0, sticky="ew")

        # Configurar que se expandan (weight = 1 significa "puede crecer")
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    # ================================================================
    # CONFIGURAR TREEVIEW : Columnas y estilos
    # ================================================================

    def _configure_treeview(self):
        """Configurar columnas y aplicar estilos al Treeview"""
        self._apply_treeview_style()
        self._configure_index_column()
        self._configure_data_columns()

    def _apply_treeview_style(self):
        """Aplicar colores y fuentes al Treeview"""
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo base del Treeview
        style.configure(
            "Treeview",
            background=AppTheme.SECONDERY_BACKGROUND,
            foreground=AppTheme.PRIMARY_TEXT,
            fieldbackground=AppTheme.SECONDERY_BACKGROUND,
            borderwidth=0,
            font=("Segoe UI", 14),
            rowheight=30
        )

        # Estilo de los encabezados
        style.configure(
            "Treeview.Heading",
            background=AppTheme.TERTIARY_BACKGROUND,
            foreground=AppTheme.PRIMARY_TEXT,
            borderwidth=1,
            relief="flat",  # Sin efecto 3D
            font=("Segoe UI", 15, "bold")
        )

        # Colores cuando seleccionas una fila (style.map = estilos dinamicos)
        style.map(
            "Treeview",
            # Lista de tuplas (estado, color)
            background=[("selected", AppTheme.PRIMARY_ACCENT)],
            foreground=[("selected", "#ffffff")]
        )

    def _configure_index_column(self):
        """Configurar la columna del indice (primera columna)"""
        self.tree.column(
            # "#0" es la columna especial del indice
            "#0", width=60, anchor="center")
        self.tree.heading("#0", text="INDEX", anchor="center")

    def _configure_data_columns(self):
        """Configurar las columnas de datos del DataFrame"""
        for column in self.dataframe.columns:
            self.tree.column(column, width=150, anchor="center", minwidth=100)
            self.tree.heading(column, text=str(
                column).upper(), anchor="center")

    # ================================================================
    # INSERTAR DATOS : Llenar el Treeview con los datos
    # ================================================================

    def _populate_treeview(self):
        """
        Insertar todos los datos en el Treeview.

        Recorre todas las filas del DataFrame y las inserta
        con colores alternados (pares e impares).
        """
        for index in range(len(self.dataframe)):  # Recorrer todas las filas
            # Formatear los valores de la fila
            values = self._format_row_values(index)

            # Determinar color (par o impar)
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            # Insertar fila en el Treeview
            self.tree.insert("", "end", text=str(index),
                             values=values, tags=(tag,))

        # Configurar colores alternados.
        self.tree.tag_configure(
            "evenrow", background=AppTheme.SECONDERY_BACKGROUND)
        self.tree.tag_configure(
            "oddrow", background=AppTheme.PRIMARY_BACKGROUND)
    

    def _format_row_values(self, row_index):
        """
        Formatear los valores de una fila.

        Convierte cada valor:
        - NaN -> "N/A"
        - Float -> 4 decimales
        - Otros -> texto
        """
        values = []
        for column in self.dataframe.columns:
            # iloc = acceso por indice de posición
            val = self.dataframe.iloc[row_index][column]
            formatted_val = self._format_cell_value(val)
            values.append(formatted_val)
        return values

    def _format_cell_value(self, value):
        """Formatear un valor individual de una celda"""
        # pd.isna() verifica si es NaN (Not a Number / dato faltante)
        if pd.isna(value):
            return "N/A"
        elif isinstance(value, float):
            return f"{value:.4f}"
        else:
            return str(value)

    # ================================================================
    # SCROLL CON RUEDA DEL RATON
    # ================================================================

    def _setup_mouse_wheel_scroll(self):
        """
        Configurar scroll inteligente con la rueda del ratón.

        El scroll solo afecta al Treeview si puede seguir scrolleando.
        En caso de llegar al límte:
        Permitir que el scroll se propague a la ventana principal.

        Compatible con:
        - Windows (event.delta)
        - macOS (event.delta)
        - Linux (event.num con botones 4 y 5)
        """
        def on_mousewheel(event):
            # Obtener posición actual del scroll (tupla con [inicio, fin])
            yview = self.tree.yview()
            current_top = yview[0]
            current_bottom = yview[1]

            # Determinar dirección del scroll
            if hasattr(event, 'delta'):
                scroll_up = event.delta > 0
            else:
                scroll_up = event.num == 4

            # Verificar si podemos seguir scrolleando
            can_scroll_up = current_top > 0.0
            can_scroll_down = current_bottom < 1.0

            # Solo bloquear propagación si podemos seguir scrolleando
            if scroll_up and can_scroll_up:
                # Podemos scrollear arriba
                self.tree.yview_scroll(-1, "units")
                return "break"
            elif not scroll_up and can_scroll_down:
                # Podemos scrollear abajo
                self.tree.yview_scroll(1, "units")
                return "break"
            else:
                # Llegamos al límite, permitir propagación
                return

        # Vincular eventos (bind = conectar evento con función)
        self.tree.bind("<MouseWheel>", on_mousewheel)  # Windows/Mac
        self.tree.bind("<Button-4>", on_mousewheel)    # Linux scroll arriba
        self.tree.bind("<Button-5>", on_mousewheel)    # Linux scroll abajo