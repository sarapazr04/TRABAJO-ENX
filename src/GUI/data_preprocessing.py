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

                entry = ctk.CTkEntry(input_button_frame, placeholder_text="")
                entry.grid(row= i+1, column = 1, padx=10, pady=(10, 0), sticky="w")
            else:
                radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
                radiobutton.grid(row=i + 1, column=0, padx=10, pady=(10, 0), sticky="w")

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

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
    app.radiobutton_frame.pack(fill="both", expand= True, padx=10, pady=(10, 0))


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)




app = ctk.CTk()
app.geometry("400x350")
_create_preprocessing_panel(app)




app.mainloop()