import customtkinter
import pandas as pd




import customtkinter
class ScrollableCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, dataframe):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        
        self.dataframe = dataframe
        self.checkboxes = []
        
        self._crear_checkboxes_desde_columnas()
    def _crear_checkboxes_desde_columnas(self):
        for i, columna in enumerate(self.dataframe.columns):
            checkbox = customtkinter.CTkCheckBox(self, text=columna)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class ColumnOptionMenu(customtkinter.CTkOptionMenu):
    
    def __init__(self, master, dataframe, command=None):
        columnas = list(dataframe.columns)
        
        super().__init__(
            master, 
            values=columnas,
            command=command
        )


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x250")
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.df = self._cargar_datos()

        self._crear_interfaz()

    def _cargar_datos(self):
        """Carga los datos según la configuración del proyecto."""
        # Ejemplo: DataFrame de prueba
        return pd.DataFrame({
            'ID': [1, 2, 3],
            'Nombre': ['Azúcar', 'Café', 'Leche'],
            'Precio': [28.5, 45.0, 32.0],
            'Cantidad': [34, 12, 8],
            'Categoria': ['A', 'B', 'A']
        })
    def _crear_interfaz(self):
        self.checkbox_frame = ScrollableCheckboxFrame(
            self, 
            "Selecciona Columnas", 
            self.df  
        )
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.column_selector = ColumnOptionMenu(
            self, 
            self.df  
        )
        self.column_selector.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="new")

        self.button = customtkinter.CTkButton(
            self, 
            text="Procesar Datos", 
            command=self.button_callback
        )
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def optionmenu_callback(self,choice):
        print("optionmenu dropdown clicked:", choice)

    def button_callback(self):
        print("checkbox_state:", self.checkbox_frame.get())
        print("option_selection:", self.column_selector.get())
app = App()
app.mainloop()