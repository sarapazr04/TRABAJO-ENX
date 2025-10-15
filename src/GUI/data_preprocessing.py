import customtkinter as ctk
from components import (
    AppTheme, AppConfig, NotificationWindow,
    Panel, LoadingIndicator
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
            self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
            self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            if i in self.input_box:
                input_button_frame = ctk.CTkFrame(self, fg_color = "transparent")
                input_button_frame.grid(row=i + 1, column=0, padx=0, pady=0, sticky="w")

                radiobutton = ctk.CTkRadioButton(input_button_frame, text=value, value=value, variable=self.variable)
                radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
                self.radiobuttons.append(radiobutton)

                entry = ctk.CTkEntry(input_button_frame, placeholder_text="")
                entry.grid(row= i+1, column = 1, padx=10, pady=(10, 0), sticky="w")
                self.entries.append(entry)
            else:
                radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
                radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")
                self.radiobuttons.append(radiobutton)

    def get_button(self):
        return self.variable.get()

    def set_button(self, value):
        self.variable.set(value)
    
    def get_entry(self, index):
        return self.entries[index].get()
    
    def del_entry(self, index):
        last_index = len(self.entries[index].get())
        self.entries[index].delete(0,last_index)
        

def _create_preprocessing_panel(master):
    preprocessing_panel = Panel(master, "Preprocesamiento de datos")
    preprocessing_panel.pack(
            fill = "x",
            padx = AppConfig.PADDING,
            pady=(AppConfig.PADDING, 10))
    _create_NA_table(preprocessing_panel)
    _create_substitute_options(preprocessing_panel)
    
def _create_NA_table(master):
    pass

def _create_substitute_options(master):
    app.radiobutton_frame = RadioButtonFrame(app, "Opciones", values=["Eliminar", "Media", "Mediana", "Constante"], input_box= [3])
    app.radiobutton_frame.entries[0].configure(placeholder_text = "Introduzca constante")
    app.radiobutton_frame.pack(fill="both", expand= True, padx=10, pady=(10, 0))
    app.button = ctk.CTkButton(app, text="Confirmar", command = _confirm_button_callback)
    app.button.pack(side = "left", expand= False, padx=10, pady=10)


def _confirm_button_callback():
    choice = app.radiobutton_frame.get_button()
    if choice == "":
        NotificationWindow(
            app,
            "Error de confirmación",
            "Tiene que eligir una opción.",
            "warning"
        )
    if choice == "Constante":
        entry_val = app.radiobutton_frame.get_entry(0)
        try:
            float(entry_val)
        except:
            app.radiobutton_frame.del_entry(0)
            NotificationWindow(
            app,
            "Error de confirmación",
            "La constante debe de ser un número! Ej: 4.25",
            "warning"
        )
    pass


app = ctk.CTk()
app.geometry("400x350")
_create_preprocessing_panel(app)

app.mainloop()