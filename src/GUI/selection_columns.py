"""
Módulo de preprocesamiento y selección de datos.

Este módulo proporciona componentes GUI para el preprocesamiento de datos
y la selección de columnas de entrada/salida en un DataFrame de pandas.
Utiliza customtkinter para crear una interfaz de usuario moderna.
"""

import customtkinter as ctk
import pandas as pd

from .components import (
    NotificationWindow, Panel, AppTheme
)


# ============================
# Panel Preprocesado
# ============================


class RadioButtonFrame(ctk.CTkFrame):
    """
    Frame con radiobuttons y cajas de entrada opcionales.

    Crea un frame con un título y una lista de radiobuttons. Permite añadir
    cajas de entrada de texto junto a radiobuttons específicos según los
    índices proporcionados.

    Attributes
    ----------
    master : ctk.CTk o ctk.CTkFrame
        Widget padre que contiene este frame.
    title : str o None
        Título del frame. Si es None, no se muestra título.
    values : list[str]
        Lista de valores para crear los radiobuttons.
    input_box : list[int]
        Índices de los radiobuttons que deben tener cajas de entrada.
    variable : ctk.StringVar
        Variable que almacena el valor del radiobutton seleccionado.
    radiobuttons : list[ctk.CTkRadioButton]
        Lista de todos los radiobuttons creados.
    entries : list[ctk.CTkEntry]
        Lista de las cajas de entrada creadas.
    """

    def __init__(self, master, title, values, input_box):
        """
        Inicializa el RadioButtonFrame.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre que contiene este frame.
        title : str o None
            Título del frame.
        values : list[str]
            Lista de valores para los radiobuttons.
        input_box : list[int]
            Índices de radiobuttons que requieren cajas de entrada.
        """
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.values = values
        self.title = title
        self.input_box = input_box
        self.radiobuttons = []
        self.entries = []
        self.variable = ctk.StringVar(value="")

        if title is not None:
            self.title = ctk.CTkLabel(
                self,
                text=self.title,
                fg_color=AppTheme.TERTIARY_BACKGROUND,
                corner_radius=6
            )
            self.title.grid(
                row=0, column=0,
                padx=10, pady=(10, 0),
                sticky="ew"
            )

        for i, value in enumerate(self.values):
            if i in self.input_box:
                # Añade entrada a los botones marcados
                input_button_frame = ctk.CTkFrame(
                    self, fg_color="transparent"
                )
                input_button_frame.grid(row=i + 1, column=0, sticky="w")

                radiobutton = ctk.CTkRadioButton(
                    input_button_frame,
                    text=value,
                    value=value,
                    variable=self.variable
                )
                radiobutton.grid(
                    row=i + 1, column=0,
                    padx=10, pady=(10, 0),
                    sticky="w"
                )
                self.radiobuttons.append(radiobutton)

                entry = ctk.CTkEntry(input_button_frame, placeholder_text="")
                entry.grid(
                    row=i+1, column=1,
                    padx=10, pady=(10, 0),
                    sticky="w"
                )
                self.entries.append(entry)
            else:
                radiobutton = ctk.CTkRadioButton(
                    self,
                    text=value,
                    value=value,
                    variable=self.variable
                )
                radiobutton.grid(
                    row=i + 1, column=0,
                    padx=10, pady=(10, 0),
                    sticky="w"
                )
                self.radiobuttons.append(radiobutton)

    def get_button(self):
        """
        Obtiene el valor del radiobutton seleccionado.

        Returns
        -------
        str
            Valor del radiobutton seleccionado, o cadena vacía si ninguno
            está seleccionado.
        """
        return self.variable.get()

    def set_button(self, value):
        """
        Establece el radiobutton seleccionado.

        Parameters
        ----------
        value : str
            Valor del radiobutton a seleccionar.
        """
        self.variable.set(value)

    def get_entry(self, index):
        """
        Obtiene el texto de una caja de entrada específica.

        Parameters
        ----------
        index : int
            Índice de la caja de entrada en la lista de entries.

        Returns
        -------
        str
            Texto contenido en la caja de entrada.
        """
        return self.entries[index].get()

    def del_entry(self, index):
        """
        Borra el contenido de una caja de entrada específica.

        Parameters
        ----------
        index : int
            Índice de la caja de entrada a limpiar.
        """
        last_index = len(self.entries[index].get())
        self.entries[index].delete(0, last_index)


class PreprocessingPanel(ctk.CTkFrame):
    """
    Panel para el preprocesamiento de datos con valores faltantes.

    Proporciona una interfaz para visualizar estadísticas de valores N/A
    y opciones para su tratamiento (eliminar, media, mediana, constante).

    Attributes
    ----------
    master : ctk.CTk o ctk.CTkFrame
        Widget padre que contiene este panel.
    elements : list
        Lista de elementos GUI del panel.
    df : pd.DataFrame
        DataFrame a preprocesar.
    app : ctk.CTk
        Instancia principal de la aplicación.
    master_panel : object
        Panel padre que contiene el DataFrame procesado.
    """

    def __init__(self, master, selected_columns, app, master_panel):
        """
        Inicializa el PreprocessingPanel.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre.
        df : pd.DataFrame
            DataFrame a preprocesar.
        app : ctk.CTk
            Instancia principal de la aplicación.
        master_panel : object
            Panel padre con acceso al DataFrame.
        """
        self.master = master
        self.elements = []
        self.selected_columns = selected_columns
        self.app = app
        self.master_panel = master_panel

    def _create_preprocessing_panel(self):
        """
        Crea el panel completo de preprocesamiento.

        Returns
        -------
        Panel
            Panel con estadísticas de N/A y opciones de sustitución.
        """
        preprocessing_panel = Panel(self.master, "Preprocesamiento de datos")

        self._create_NA_stats(preprocessing_panel)
        self._create_substitute_options(preprocessing_panel)

        return preprocessing_panel

    def _create_NA_stats(self, master):
        """
        Crea y muestra estadísticas de valores N/A.

        Parameters
        ----------
        master : ctk.CTkFrame
            Frame padre donde mostrar las estadísticas.
        """
        self.nas_stats = self._count_nan_df(self.master_panel.df[self.selected_columns])
        nas_total = self._sum_nan(self.nas_stats)
        nas_columns = self._nan_columns(self.nas_stats)

        label = ctk.CTkLabel(
            master,
            text=f"Nº total de N/As: {nas_total}\nColumnas: {nas_columns}",
            fg_color="transparent"
        )
        self.elements.append(label)
        label.pack(expand=True)

    def _create_substitute_options(self, master):
        """
        Crea opciones para sustituir valores N/A.

        Parameters
        ----------
        master : ctk.CTkFrame
            Frame padre donde mostrar las opciones.
        """
        radiobutton_frame = RadioButtonFrame(
            master,
            title="Opciones",
            values=["Eliminar", "Media", "Mediana", "Constante"],
            input_box=[3]
        )
        self.elements.append(radiobutton_frame)
        radiobutton_frame.entries[0].configure(
            placeholder_text="Introduzca constante"
        )
        radiobutton_frame.pack(
            fill="both", expand=True, padx=10, pady=(10, 0)
        )

        button = ctk.CTkButton(
            master,
            text="Confirmar",
            command=self._confirm_button_callback
        )
        self.elements.append(button)
        button.pack(side="left", expand=False, padx=10, pady=10)

    def _confirm_button_callback(self):
        """
        Callback del botón de confirmación de preprocesamiento.

        Procesa el DataFrame según la opción seleccionada: eliminar filas,
        rellenar con media, mediana o constante. Valida la entrada del
        usuario y muestra notificaciones de éxito o error.
        """
        choice = self.elements[1].get_button()
        if choice == "":

            if self.nas_stats != []:
                NotificationWindow(
                    self.app,
                    "Error de confirmación",
                    "Tiene que eligir una opción.",
                    "warning"
                )

        elif choice == "Constante":
            entry_val = self.elements[1].get_entry(0)

            try:
                float(entry_val)

                for col in self.selected_columns:
                    self.master_panel.df[col] = self.master_panel.df[col].fillna(entry_val)

                NotificationWindow(
                    self.app,
                    "Preprocesado terminado",
                    "El preprocesado se ha llevado a cabo sin problemas.",
                    "success"
                )
                print(self.master_panel.df)

            except ValueError:
                self.elements[1].del_entry(0)

                NotificationWindow(
                    self.app,
                    "Error de confirmación",
                    "La constante debe de ser un número! Ej: 4.25",
                    "warning"
                )

        elif choice == "Eliminar":
            self.master_panel.df = self.master_panel.df.dropna(subset=self.selected_columns)

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success"
            )
            print(self.master_panel.df)

        elif choice == "Media":

            for col in self.selected_columns:
                avg = self.master_panel.df.loc[:, col].mean()
                self.master_panel.df[col] = self.master_panel.df[col].fillna(avg)

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success"
            )
            print("Result:", self.master_panel.df)

        elif choice == "Mediana":
            for col in self.selected_columns:
                median = self.master_panel.df.loc[:, col].median()
                self.master_panel.df[col] = self.master_panel.df[col].fillna(median)

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success"
            )
            print("Result:", self.master_panel.df)
        self.app._display_data(self.master_panel.df)
        self.app.set_preprocessed_df(self.master_panel.df)

    def _count_nan_df(self, datos):
        """
        Cuenta los valores N/A por columna.

        Parameters
        ----------
        datos : pd.DataFrame
            DataFrame a analizar.

        Returns
        -------
        list[list]
            Lista de listas [número_de_NAs, nombre_columna] para cada columna
            con valores faltantes.
        """
        nas_columns = []
        columns_indices = datos.columns[datos.isna().any()].tolist()

        for column in columns_indices:
            nas_column = [0, column]

            for row in datos[column].isna():
                if row:
                    nas_column[0] += 1
            nas_columns.append(nas_column)

        return nas_columns

    def _detect_nan(self, datos):
        """
        Detecta y notifica la presencia de valores N/A.

        Parameters
        ----------
        datos : pd.DataFrame
            DataFrame a analizar.
        """
        nas_columns = self._count_nan_df(datos)
        nas_total = self._sum_nan(nas_columns)

        if nas_columns != []:
            NotificationWindow(
                self.app,
                "Valores NaN detectados",
                f"Hay {len(nas_columns)} columna(s) con valores NaN "
                f"con un total de {nas_total} NaNs.",
                "warning"
            )

    def _sum_nan(self, nan_list):
        """
        Suma el total de valores N/A.

        Parameters
        ----------
        nan_list : list[list]
            Lista de listas [cantidad_NAs, nombre_columna].

        Returns
        -------
        int
            Número total de valores N/A.
        """
        total = 0
        for i in nan_list:
            total += i[0]
        return total

    def _nan_columns(self, nan_list):
        """
        Extrae los nombres de columnas con valores N/A.

        Parameters
        ----------
        nan_list : list[list]
            Lista de listas [cantidad_NAs, nombre_columna].

        Returns
        -------
        list[str]
            Lista con nombres de columnas que contienen N/A.
        """
        total = []
        for i in nan_list:
            total.append(i[1])
        return total


# ============================
# Panel Selección
# ============================


class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    """
    Frame scrollable con checkboxes para cada columna del DataFrame.

    Crea un conjunto de checkboxes basado en las columnas de un DataFrame,
    permitiendo la selección múltiple de columnas.

    Attributes
    ----------
    dataframe : pd.DataFrame
        DataFrame del que se extraen las columnas.
    checkboxes : list[ctk.CTkCheckBox]
        Lista de checkboxes creados.
    """

    def __init__(self, master, title, dataframe):
        """
        Inicializa el ScrollableCheckboxFrame.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre.
        title : str
            Título del frame scrollable.
        dataframe : pd.DataFrame
            DataFrame del que extraer las columnas.
        """
        super().__init__(master, label_text=title)

        self.dataframe = dataframe
        self.checkboxes = []

        self._crear_checkboxes_desde_columnas()

    def _crear_checkboxes_desde_columnas(self):
        """Crea un checkbox por cada columna del DataFrame."""
        for i, columna in enumerate(self.dataframe.columns):
            checkbox = ctk.CTkCheckBox(self, text=columna)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        """
        Obtiene las columnas seleccionadas.

        Returns
        -------
        list[str]
            Lista con los nombres de las columnas seleccionadas.
        """
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class ColumnFrame(ctk.CTkFrame):
    """
    Frame con un menú desplegable de columnas del DataFrame.

    Proporciona un OptionMenu para seleccionar una única columna del
    DataFrame proporcionado.

    Attributes
    ----------
    label : ctk.CTkLabel
        Etiqueta con el título del frame.
    option_menu : ctk.CTkOptionMenu
        Menú desplegable con las columnas.
    """

    def __init__(self, master, title, dataframe, command=None):
        """
        Inicializa el ColumnFrame.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre.
        title : str
            Título del frame.
        dataframe : pd.DataFrame
            DataFrame del que extraer las columnas.
        command : callable, optional
            Función callback cuando se selecciona una columna.
        """
        super().__init__(master)

        self.label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 13, "bold")
        )
        self.label.pack(padx=10, pady=(10, 5))

        columnas = list(dataframe.columns)
        self.option_menu = ctk.CTkOptionMenu(
            self,
            values=columnas,
            command=command
        )
        self.option_menu.pack(padx=10, pady=(0, 10), fill="x")

    def get(self):
        """
        Obtiene la columna seleccionada.

        Returns
        -------
        str
            Nombre de la columna seleccionada.
        """
        return self.option_menu.get()

    def set(self, value):
        """
        Establece la columna seleccionada.

        Parameters
        ----------
        value : str
            Nombre de la columna a seleccionar.
        """
        self.option_menu.set(value)


class SelectionPanel(ctk.CTkFrame):
    """
    Panel para la selección de columnas de entrada y salida.

    Permite al usuario seleccionar múltiples columnas de entrada y una
    columna de salida del DataFrame. Incluye funcionalidad para mostrar
    y preprocesar los datos seleccionados.

    Attributes
    ----------
    master : ctk.CTk o ctk.CTkFrame
        Widget padre.
    col_entrada : list
        Lista de columnas de entrada seleccionadas.
    df : pd.DataFrame
        DataFrame original con todos los datos.
    app : ctk.CTk
        Instancia principal de la aplicación.
    processed_df : pd.DataFrame o None
        DataFrame procesado después de aplicar filtros.
    frame_entrada : ScrollableCheckboxFrame
        Frame con checkboxes de columnas de entrada.
    frame_salida : ColumnFrame
        Frame con selector de columna de salida.
    button : ctk.CTkButton
        Botón para procesar los datos.
    """

    def __init__(self, master, df, app):
        """
        Inicializa el SelectionPanel.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre.
        df : pd.DataFrame
            DataFrame a visualizar y procesar.
        app : ctk.CTk
            Instancia principal de la aplicación.
        """
        self.master = master
        self.col_entrada = []
        self.df = df
        self.app = app
        self.processed_df = None

    def _crear_interfaz(self):
        """
        Crea la interfaz de selección de datos.

        Returns
        -------
        Panel
            Panel con la interfaz de selección de entrada/salida.
        """
        select_panel = Panel(self.master, "Selección de datos")

        frame_in_out = ctk.CTkFrame(select_panel, fg_color="transparent")
        frame_in_out.pack(expand=True, fill="x")

        # Frame izquierdo: Datos de Entrada
        self.frame_entrada = ScrollableCheckboxFrame(
            frame_in_out,
            "Datos de Entrada",
            self.df
        )
        self.frame_entrada.pack(
            side="left", fill="both",
            expand=True, padx=10, pady=10
        )

        # Frame derecho: Datos de Salida
        self.frame_salida = ColumnFrame(
            frame_in_out,
            "Datos de Salida",
            self.df
        )
        self.frame_salida.pack(
            side="right", fill="both",
            expand=True, padx=20, pady=10
        )

        # Botón de confirmación
        self.button = ctk.CTkButton(
            select_panel,
            text="Procesar Datos",
            command=self.button_callback
        )
        self.button.pack(fill="x", expand=True, padx=10, pady=10)
        return select_panel

    def button_callback(self):
        """
        Callback del botón de procesar datos.

        Valida que se hayan seleccionado columnas de entrada y procede
        a mostrar los datos seleccionados.
        """
        columnas_entrada_inicial = self.frame_entrada.get()
        if len(columnas_entrada_inicial) == 0:
            NotificationWindow(
                self.app,
                "Error de selección",
                "Debe elegir al menos una columna de entrada",
                "warning"
            )
        else:
            self.columnas_entrada = columnas_entrada_inicial

            self.columna_salida = self.frame_salida.get()
            self._display_data()
            print("\n--- Procesando Datos ---")
            print(f"Datos de Entrada: {self.columnas_entrada}")
            print(f"Datos de Salida: {self.columna_salida}")

    def _create_empty_panel(self):
        """
        Crea un panel vacío con mensaje de estado inicial.

        Muestra un mensaje indicando que se deben seleccionar columnas
        antes de visualizar datos.
        """
        # Frame exterior (transparente, no se toca)
        self.table_outer_frame = ctk.CTkFrame(
            self.master, fg_color="transparent"
        )
        self.table_outer_frame.pack(fill="both", expand=True, padx=15, pady=0)

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
            text="Selecciona columnas con N/As",
            font=("Segoe UI", 13),
            text_color=AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx=0.5, rely=0.5, anchor="center")

    def _display_data(self):
        """
        Muestra los datos seleccionados y el panel de preprocesamiento.

        Oculta el mensaje de estado vacío, destruye el contenedor anterior
        y crea un nuevo panel de preprocesamiento con las columnas
        seleccionadas.
        """

        # Ocultar mensaje de "sin datos"
        if self.empty_state_label.winfo_exists():
            self.empty_state_label.place_forget()

        # Recrear el contenedor (limpieza completa)
        self.table_container.destroy()
        try:
            if self.pre_options.winfo_exists():
                self.pre_options.pack_forget()
        except AttributeError:
            pass
        columnas_procesar = self.columnas_entrada.copy()
        if self.columna_salida not in columnas_procesar:
            columnas_procesar.append(self.columna_salida)
        # Crear gestor de visualización y mostrar datos
        self.pre_panel = PreprocessingPanel(
            self.table_outer_frame,
            columnas_procesar,
            self.app,
            self
        )
        self.pre_panel._detect_nan(self.df[columnas_procesar])
        self.pre_options = self.pre_panel._create_preprocessing_panel()
        self.pre_options.pack(fill="both", expand=True, padx=10, pady=10)


# Ejemplo de uso
if __name__ == "__main__":
    # DataFrame de ejemplo
    df = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Nombre': ['Azúcar', 'Café', 'Leche', 'Té'],
        'Precio': [28.5, 45.0, 32.0, 15.0],
        'Cantidad': [34, 12, 8, 20]
    })

    app = ctk.CTk()
    panel = SelectionPanel(app, df, app)
    a = panel._crear_interfaz()
    a.pack(fill="both", expand=True, side="left", padx=10, pady=10)
    panel._create_empty_panel()
    app.title("Selector de datos")
    app.geometry("800x400")

    app.mainloop()
