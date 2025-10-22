import customtkinter as ctk
import pandas as pd

from .components import (
    NotificationWindow, Panel, AppTheme
)

# ============================
# Panel Preprocesado
# ============================


class RadioButtonFrame(ctk.CTkFrame):
    '''
    Crea un frame con radiobuttons con posibilidad para cajas de input.

    Crea un frame con un título y con la lista values crea radiobuttons y con
    el índice del botón en values que requiere input se les añade la caja a la
    derecha.

    Atributos
    ---------
    master: 
    title : 
    values : 
    input_box

    '''

    def __init__(self, master, title, values, input_box):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.values = values
        self.title = title
        self.input_box = input_box
        self.radiobuttons = []
        self.entries = []
        self.variable = ctk.StringVar(value="")

        if title is not None:
            self.title = ctk.CTkLabel(self,
                                      text=self.title,
                                      fg_color=AppTheme.TERTIARY_BACKGROUND,
                                      corner_radius=6)
            self.title.grid(row=0, column=0,
                            padx=10, pady=(10, 0),
                            sticky="ew")

        for i, value in enumerate(self.values):  # Crea los botones con values
            if i in self.input_box:  # Añade entradas a las botones marcados
                input_button_frame = ctk.CTkFrame(self, fg_color="transparent")
                input_button_frame.grid(row=i + 1, column=0,
                                        sticky="w")

                radiobutton = ctk.CTkRadioButton(input_button_frame,
                                                 text=value, value=value,
                                                 variable=self.variable)
                radiobutton.grid(row=i + 1, column=0,
                                 padx=10, pady=(10, 0),
                                 sticky="w")
                self.radiobuttons.append(radiobutton)

                entry = ctk.CTkEntry(input_button_frame, placeholder_text="")
                entry.grid(row=i+1, column=1,
                           padx=10, pady=(10, 0),
                           sticky="w")
                self.entries.append(entry)
            else:
                radiobutton = ctk.CTkRadioButton(self,
                                                 text=value, value=value,
                                                 variable=self.variable)
                radiobutton.grid(row=i + 1, column=0,
                                 padx=10, pady=(10, 0),
                                 sticky="w")
                self.radiobuttons.append(radiobutton)

    def get_button(self):
        return self.variable.get()

    def set_button(self, value):
        self.variable.set(value)

    def get_entry(self, index):
        return self.entries[index].get()

    def del_entry(self, index):
        last_index = len(self.entries[index].get())
        self.entries[index].delete(0, last_index)


class PreprocessingPanel(ctk.CTkFrame):

    def __init__(self, master, df, app, master_panel):
        self.master = master
        self.elements = []
        self.df = df
        self.app = app
        self.master_panel = master_panel

    def _create_preprocessing_panel(self):
        preprocessing_panel = Panel(self.master, "Preprocesamiento de datos")

        self._create_NA_stats(preprocessing_panel)
        self._create_substitute_options(preprocessing_panel)

        return preprocessing_panel

    def _create_NA_stats(self, master):
        nas_stats = self._count_nan_df(self.df)
        nas_total = self._sum_nan(nas_stats)
        nas_columns = self._nan_columns(nas_stats)

        label = ctk.CTkLabel(
            master,
            text=f"Nº total de N/As: {nas_total}\nColumnas: {nas_columns}",
            fg_color="transparent"
        )
        self.elements.append(label)
        label.pack(expand=True)

    def _create_substitute_options(self, master):
        radiobutton_frame = RadioButtonFrame(
            master,
            title="Opciones",
            values=["Eliminar", "Media", "Mediana", "Constante"],
            input_box=[3]
        )
        self.elements.append(radiobutton_frame)
        radiobutton_frame.entries[0].configure(
            placeholder_text="Introduzca constante")
        radiobutton_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        button = ctk.CTkButton(
            master,
            text="Confirmar",
            command=self._confirm_button_callback
        )
        self.elements.append(button)
        button.pack(side="left", expand=False, padx=10, pady=10)

    def _confirm_button_callback(self):
        choice = self.elements[1].get_button()
        # Los 5 casos posibles según el estado de selección al confirmar
        if choice == "":
            NotificationWindow(
                self.app,
                "Error de confirmación",
                "Tiene que eligir una opción.",
                "warning")

        elif choice == "Constante":
            entry_val = self.elements[1].get_entry(0)

            try:
                float(entry_val)

                self.master_panel.df = self.df.fillna(entry_val)
                NotificationWindow(
                    self.app,
                    "Preprocesado terminado",
                    "El preprocesado se ha llevado a cabo sin problemas.",
                    "success")
                print(self.master_panel.df)

            except ValueError:
                self.elements[1].del_entry(0)  # Borra lo introducido

                NotificationWindow(
                    self.app,
                    "Error de confirmación",
                    "La constante debe de ser un número! Ej: 4.25",
                    "warning")

        elif choice == "Eliminar":
            self.master_panel.df = self.df.dropna()

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print(self.master_panel.df)

        elif choice == "Media":
            result = pd.DataFrame()

            for col in self.df.columns:
                avg = self.df.loc[:, col].mean()
                result = pd.concat([result, self.df[col].fillna(avg)], axis=1)
            self.master_panel.df = result

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print("Result:", self. master_panel.df)

        elif choice == "Mediana":
            result = pd.DataFrame()

            for col in self.df.columns:
                median = self.df.loc[:, col].median()
                result = pd.concat([
                    result,
                    self.df[col].fillna(median)],
                    axis=1)
            self.master_panel.df = result

            NotificationWindow(
                self.app,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print("Result:", self.master_panel.df)

    def _count_nan_df(self, datos):
        nas_columns = []
        columns_indices = datos.columns[datos.isna().any()].tolist()

        for column in columns_indices:  # Recorre columnas para contar NAs
            nas_column = [0, column]

            for row in datos[column].isna():
                if row:
                    nas_column[0] += 1
            nas_columns.append(nas_column)

        return nas_columns

    def _detect_nan(self, datos):
        nas_columns = self._count_nan_df(datos)
        nas_total = self._sum_nan(nas_columns)

        if nas_columns != []:
            NotificationWindow(
                self.app,
                "Valores NaN detectados",
                f"Hay {len(nas_columns)} columna(s) con valores NaN con un total de {nas_total} NaNs.",
                "warning")

    def _sum_nan(self, nan_list: list):
        total = 0
        for i in nan_list:
            total += i[0]
        return total

    def _nan_columns(self, nan_list: list):
        total = []
        for i in nan_list:
            total.append(i[1])
        return total

# ============================
# Panel Selección
# ============================


class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):

    def __init__(self, master, title, dataframe):
        super().__init__(master, label_text=title)

        self.dataframe = dataframe
        self.checkboxes = []

        self._crear_checkboxes_desde_columnas()

    def _crear_checkboxes_desde_columnas(self):
        for i, columna in enumerate(self.dataframe.columns):
            checkbox = ctk.CTkCheckBox(self, text=columna)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class ColumnFrame(ctk.CTkFrame):

    def __init__(self, master, title, dataframe, command=None):
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
        # Retorna la columna seleccionada.
        return self.option_menu.get()

    def set(self, value):
        # Establece el valor del OptionMenu.
        self.option_menu.set(value)


class SelectionPanel(ctk.CTkFrame):
    def __init__(self, master, df, app):
        self.master = master
        self.col_entrada = []
        self.df = df
        self.app = app
        self.processed_df = None

    def _crear_interfaz(self):
        # Crea las cosas de la interfaz.
        select_panel = Panel(self.master, "Selección de datos")

        frame_in_out = ctk.CTkFrame(select_panel, fg_color="transparent")
        frame_in_out.pack(expand=True, fill="x")
        # Frame izquierdo: Datos de Entrada
        self.frame_entrada = ScrollableCheckboxFrame(
            frame_in_out,
            "Datos de Entrada",
            self.df
        )
        self.frame_entrada.pack(side="left", fill="both",
                                expand=True, padx=10, pady=10)

        # Frame derecho: Datos de Salida
        self.frame_salida = ColumnFrame(
            frame_in_out,
            "Datos de Salida",
            self.df

        )
        self.frame_salida.pack(side="right", fill="both",
                               expand=True, padx=20, pady=10)

        # Botón
        self.button = ctk.CTkButton(
            select_panel,
            text="Procesar Datos",
            command=self.button_callback
        )
        self.button.pack(fill="x", expand=True, padx=10, pady=10)
        return select_panel

    def button_callback(self):
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
            columna_salida = self.frame_salida.get()
            self._display_data()
            print(f"\n--- Procesando Datos ---")
            print(f"Datos de Entrada: {self.columnas_entrada}")
            print(f"Datos de Salida: {columna_salida}")

    def _create_empty_panel(self):

        # Frame exterior (transparente, no se toca)
        self.table_outer_frame = ctk.CTkFrame(
            self.master, fg_color="transparent")
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
        try:
            if self.preprocessing_options.winfo_exists():  # winfo_exists() verifica si el widget existe
                self.preprocessing_options.pack_forget()  # Ocultar (quitar del layout)
        except:
            pass
        # Crear gestor de visualización y mostrar datos
        self.preprocessing_panel = PreprocessingPanel(self.table_outer_frame,
                                                      self.df[self.columnas_entrada],
                                                      self.app, self)
        self.preprocessing_options = self.preprocessing_panel._create_preprocessing_panel()
        self.preprocessing_options.pack(
            fill="both", expand=True, padx=10, pady=10)


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
