import customtkinter as ctk
import tkinter as tk
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

    def get_button(self): #
        return self.variable.get()

    def set_button(self, value):
        self.variable.set(value)
    
    def get_entry(self, index):
        return self.entries[index].get()
    
    def del_entry(self, index):
        last_index = len(self.entries[index].get())
        self.entries[index].delete(0,last_index)
        

class PreprocessingPanel(Panel):

    def __init__(self, master):
        self.elements = []
        

    # def _create_preprocessing_panel(self,master):
    #     preprocessing_panel = Panel(master, "Preprocesamiento de datos")
    #     preprocessing_panel.pack(
    #             fill = "x",
    #             padx = AppConfig.PADDING,
    #             pady=(AppConfig.PADDING, 10))
    #     self._create_NA_table(preprocessing_panel)
    #     self._create_substitute_options(preprocessing_panel)

    def _create_preprocessing_panel(self,master):
        preprocessing_panel = Panel(master, "Preprocesamiento de datos")
        
        self._create_NA_table(preprocessing_panel)
        self._create_substitute_options(preprocessing_panel)
        return preprocessing_panel


    def _create_NA_table(self, master):
        label = ctk.CTkLabel(master, text="Nº total de N/As:", fg_color="transparent")
        self.elements.append(label)
        label.pack(expand=True)
        table = tk.ttk.Treeview()
        pass

    def _create_substitute_options(self,master):
        radiobutton_frame = RadioButtonFrame(master, "Opciones", values=["Eliminar", "Media", "Mediana", "Constante"], input_box= [3])
        self.elements.append(radiobutton_frame)
        radiobutton_frame.entries[0].configure(placeholder_text = "Introduzca constante")
        radiobutton_frame.pack(fill="both", expand= True, padx=10, pady=(10, 0))
        button = ctk.CTkButton(master, text="Confirmar", command = self._confirm_button_callback)
        self.elements.append(button)
        button.pack(side = "left", expand= False, padx=10, pady=10)


    def _confirm_button_callback(self):
        choice = self.elements[1].get_button()
        if choice == "":
            NotificationWindow(
                app,
                "Error de confirmación",
                "Tiene que eligir una opción.",
                "warning"
            )
        if choice == "Constante":
            entry_val = self.elements[1].get_entry(0)
            try:
                float(entry_val)
            except:
                self.elements[1].del_entry(0)
                NotificationWindow(
                app,
                "Error de confirmación",
                "La constante debe de ser un número! Ej: 4.25",
                "warning"
            )



app = ctk.CTk()
app.geometry("800x350")
a = PreprocessingPanel(app)
b = a._create_preprocessing_panel(app)
c = a._create_preprocessing_panel(app)
b.pack(
                side = "left",
                fill= "y",
                padx = AppConfig.PADDING,
                pady=(AppConfig.PADDING, 10))
c.pack(
                side = "right",
                padx = AppConfig.PADDING,
                pady=(AppConfig.PADDING, 10))


app.mainloop()