import customtkinter as ctk
from .components import (AppTheme, AppConfig,
                         Panel,
                         UploadButton,
                         NotificationWindow)
from .predict_model import predict_result


class PredictionSection():

    def __init__(self, app, master, col_entrada, formula):
        self.app = app
        self.master = master
        self.col_entrada = col_entrada
        self.formula = formula

        self._create_predict_panel()
        self._create_empty_panel()

    def _check_entries(self):
        vals_list = []
        warning = False
        print("List of entries:", self.multiple_entries.entries)
        for entry in self.multiple_entries.entries:
            if self._is_entry_num(entry):
                vals_list.append(entry.get())
            else:
                warning = True

        if warning:
            NotificationWindow(self.app,
                               "Valores no numéricos detectados",
                               "Todas las entradas tienen que contener "
                               "valores numéricos\n(Ej: 53.94)",
                               "warning")
        else:
            result_text = predict_result(self.col_entrada,
                                         vals_list,
                                         self.formula)
            self.result_label.configure(text=result_text)

    def _is_entry_num(self, entry):
        try:
            print("Entrada:", entry.get())
            float(entry.get())
        except ValueError:
            entry.delete(0, 'end')
            return False
        else:
            return True

    def _create_predict_panel(self):
        self.predict_section = ctk.CTkFrame(self.master)
        self.predict_section.pack(fill="x", expand=True)
        self.predict_panel = Panel(self.predict_section,
                                   "Predicción con modelo")
        self.predict_panel.pack(fill="x", expand=True, padx=20, pady=20)

    def _create_predict_content(self):
        self.predict_content = ctk.CTkFrame(self.predict_outer_frame)
        self.predict_content.pack(fill="x", expand=True)
        self.predict_content.grid_columnconfigure(0, weight=1)
        self.predict_content.grid_columnconfigure(1, weight=1)
        self._create_entries_section()
        self._create_result_section()

    def _create_entries_section(self):
        self.entries_frame = ctk.CTkFrame(self.predict_content)
        self.entries_frame.pack(side="left",
                                fill="both",
                                expand=True,
                                padx=(0, 5))
        title = ctk.CTkLabel(self.entries_frame,
                             text="Entradas",
                             corner_radius=6,
                             font=("Orbitron", 13, "bold"),
                             fg_color=AppTheme.TERTIARY_BACKGROUND)
        title.pack(fill="x", pady=(5, 10), padx=15, anchor="n")
        self.multiple_entries = MultipleEntriesFrame(self.entries_frame,
                                                     self.col_entrada)

    def _create_result_section(self):
        self.result_frame = ctk.CTkFrame(self.predict_content)
        self.result_frame.pack(side="left",
                               fill="both",
                               expand=True,
                               padx=(5, 0))
        title = ctk.CTkLabel(self.result_frame,
                             text="Salida",
                             corner_radius=6,
                             font=("Orbitron", 13, "bold"),
                             fg_color=AppTheme.TERTIARY_BACKGROUND)
        title.pack(fill="x", pady=(5, 10), padx=15, anchor="n")
        self.result_label = ctk.CTkLabel(self.result_frame,
                                         fg_color=AppTheme.PRIMARY_BACKGROUND,
                                         corner_radius=6,
                                         font=AppConfig.MONO_FONT,
                                         text="Salida:"
                                         )

        self.result_label.pack(side="top",
                               anchor="n",
                               pady=10,
                               expand=True,
                               fill="x",
                               padx=20
                               )

        self.predict_button = UploadButton(self.result_frame,
                                           text="Predecir",
                                           command=self.pred_button_callback
                                           )
        self.predict_button.pack(side="bottom", anchor="center", pady=10)

    def pred_button_callback(self):
        self.predict_button.configure(state="disabled")
        self._check_entries()
        self.predict_button.configure(state="normal")

    def _create_empty_panel(self):
        """Crear panel vacío con mensaje de estado inicial"""
        self.predict_outer_frame = ctk.CTkFrame(
            self.predict_panel, fg_color="transparent"
        )
        self.predict_outer_frame.pack(fill="both", expand=True)

        self.predict_container = ctk.CTkFrame(
            self.predict_outer_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        self.predict_container.pack(fill="both", expand=True)

        self.empty_state_label = ctk.CTkLabel(
            self.predict_container,
            text="Seleccione o cree un modelo\npara predecir datos",
            font=("Segoe UI", 13),
            text_color=AppTheme.DIM_TEXT
        )
        self.empty_state_label.place(relx=0.5, rely=0.5, anchor="center")

    def display_data(self):
        """Mostrar panel de predicción de datos"""
        # Ocultar mensaje
        try:
            if self.empty_state_label.winfo_exists():
                self.empty_state_label.place_forget()
        except Exception:
            pass

        # Destruir contenedor anterior
        self.predict_container.destroy()

        # Destruir panel de preprocesamiento anterior si existe
        try:
            if (hasattr(self, 'predict_content') and
                    self.predict_content.winfo_exists()):

                self.predict_content.pack_forget()
                self.predict_content.destroy()
        except Exception:
            pass

        self._create_predict_content()
        self.predict_section.pack(fill="x", expand=True)


class MultipleEntriesFrame():
    def __init__(self, master, model):
        self.master = master
        self.model = model
        self.entries = []

        for col in model:
            self._create_col_entry(master, col)

    def _create_col_entry(self, master, col):
        entry_frame = ctk.CTkFrame(master)
        entry_frame.pack(padx=10, pady=(0, 10), anchor="w")
        label = ctk.CTkLabel(entry_frame, width=200, text=col)
        label.pack(side="left", padx=10)
        entry = ctk.CTkEntry(entry_frame,
                             placeholder_text="Introduzca la entrada",
                             fg_color=AppTheme.SECONDARY_BACKGROUND,
                             border_color=AppTheme.BORDER)
        entry.pack(side="left")
        self.entries.append(entry)


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1200x700")
    predict = PredictionSection(app, "Pepino")

    def a():
        predict.display_data()

    butt = ctk.CTkButton(app, text="CTkButton", command=a)
    butt.pack()
    app.mainloop()
