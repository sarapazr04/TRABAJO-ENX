import customtkinter as ctk
from components import (
    AppTheme, AppConfig, NotificationWindow,
    Panel, LoadingIndicator
)

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
    pass


def combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


app = ctk.CTk()

'''
combobox = ctk.CTkComboBox(app, values=["option 1", "option 2"],
                                     command=combobox_callback)
combobox.set("option 2")


combobox.pack(padx=20, pady=20)
'''
_create_preprocessing_panel(app)

app.mainloop()