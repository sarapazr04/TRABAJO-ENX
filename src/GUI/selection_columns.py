from components import (
     NotificationWindow,
     Panel
)


import customtkinter as ctk
import pandas as pd

class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    
    def __init__(self, master, title, dataframe):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        
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
        #Retorna la columna seleccionada.
        return self.option_menu.get()
    
    def set(self, value):
        #Establece el valor del OptionMenu.
        self.option_menu.set(value)


class SelectorDatosPanel(Panel):
    def __init__(self, master, dataframe, **kwargs):

        super().__init__(master, "Selector de Datos", **kwargs)
        
        self.df = dataframe
        
        # Crear el contenido del panel
        self._crear_contenido()
    def _crear_contenido(self):
        #Crea las cosas de la interfaz.
        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        
        contenedor.grid_columnconfigure((0, 1), weight=1)
        contenedor.grid_rowconfigure(0, weight=1)
        
        # Frame izquierdo: Datos de Entrada 
        self.frame_entrada = ScrollableCheckboxFrame(
            contenedor, 
            "Datos de Entrada",  
            self.df
        )
        self.frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        #Frame derecho: Datos de Salida 
        self.frame_salida = ColumnFrame(
            contenedor,
            "Datos de Salida", 
            self.df
           
        )
        self.frame_salida.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Botón 
        self.button = ctk.CTkButton(
            contenedor, 
            text="Procesar Datos", 
            command=self.button_callback
        )
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)


    def button_callback(self):
  
            
        columnas_entrada_inicial = self.frame_entrada.get()
        if len(columnas_entrada_inicial) == 0:
            NotificationWindow(
                app,
                "Error de selección",
                "Debe elegir al menos una columna de entrada",
                "warning"
            )
        else:

            columnas_entrada = columnas_entrada_inicial
            columna_salida = self.frame_salida.get()
            
            print(f"\n--- Procesando Datos ---")
            print(f"Datos de Entrada: {columnas_entrada}")
            print(f"Datos de Salida: {columna_salida}")


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
    app.title("Aplicación Principal")
    app.geometry("600x500")

    selector_panel = SelectorDatosPanel(app, df)
    selector_panel.pack(fill="both", expand=True, padx=20, pady=20)
    app.mainloop()