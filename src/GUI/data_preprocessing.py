import pandas as pd
import customtkinter as ctk
from components import (
    AppTheme, AppConfig, NotificationWindow,
    Panel
)


class RadioButtonFrame(ctk.CTkFrame):
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


class PreprocessingPanel(Panel):

    def __init__(self, master, df):
        self.master = master
        self.elements = []
        self.df = df

    def _create_preprocessing_panel(self):
        preprocessing_panel = Panel(self.master, "Preprocesamiento de datos")

        self._create_NA_table(preprocessing_panel)
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
        self._detect_nan(self.df[["ID", "Nombre", "Cantidad"]])

        choice = self.elements[1].get_button()
        # Los 5 casos según el estado de selección al confirmar
        if choice == "":
            NotificationWindow(
                self.master,
                "Error de confirmación",
                "Tiene que eligir una opción.",
                "warning")

        elif choice == "Constante":
            entry_val = self.elements[1].get_entry(0)

            try:
                float(entry_val)

                self.df = self.df.fillna(entry_val)
                NotificationWindow(
                    self.master,
                    "Preprocesado terminado",
                    "El preprocesado se ha llevado a cabo sin problemas.",
                    "success")
                print(self.df)

            except ValueError:
                self.elements[1].del_entry(0)  # Borra lo introducido

                NotificationWindow(
                    self.master,
                    "Error de confirmación",
                    "La constante debe de ser un número! Ej: 4.25",
                    "warning")

        elif choice == "Eliminar":
            self.df = self.df.dropna()

            NotificationWindow(
                self.master,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print(self.df)

        elif choice == "Media":
            result = pd.DataFrame()

            for col in self.df.columns:
                avg = self.df.loc[:, col].mean()
                result = pd.concat([result, self.df[col].fillna(avg)], axis=1)
            self.df = result

            NotificationWindow(
                self.master,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print("Result:", result)

        elif choice == "Mediana":
            result = pd.DataFrame()

            for col in self.df.columns:
                median = self.df.loc[:, col].median()
                result = pd.concat([
                    result,
                    self.df[col].fillna(median)],
                    axis=1)
            self.df = result

            NotificationWindow(
                self.master,
                "Preprocesado terminado",
                "El preprocesado se ha llevado a cabo sin problemas.",
                "success")
            print("Result:", result)

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
                    self.master,
                    "Valores NaN detectados",
                    f"Hay {len(nas_columns)} columna(s) con valores NaN con un\
                         total de {nas_total} NaNs.",
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


if __name__ == "__main__":

    app = ctk.CTk()
    app.geometry("400x350")

    df = pd.DataFrame({
            'ID': [1, 2, 3, 4],
            'Nombre': [1, None, 6, 6],
            'Precio': [28.5, 45.0, 32.0, 15.0],
            'Cantidad': [34, None, 8, 8]
    })

    a = PreprocessingPanel(app, df)
    b = a._create_preprocessing_panel()
    b.pack(
                    padx=AppConfig.PADDING,
                    pady=(AppConfig.PADDING, 10))

    app.mainloop()
