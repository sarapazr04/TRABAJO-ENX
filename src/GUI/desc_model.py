import customtkinter as ctk

from components import (
    NotificationWindow, Panel
)
import tkinter.font as tkfont


class DescriptBox:
    def __init__(self, master, app):
        self.master = master
        self.app = app

    def get(self):
        """Obtiene el contenido del textbox"""
        return self.textbox.get("0.0", "end")

    def create_textbox(self, master):
        """Crea el textbox dentro del panel"""
        # Configurar el grid del master para que el textbox se expanda
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(
            master=master,
            width=400,
            corner_radius=0
        )
        self.textbox.pack(fill="both",
                          expand=True,
                          padx=10,
                          pady=10,)
        custom_font = tkfont.Font(family="Inter", size=13)
        self.textbox._textbox.configure(font=custom_font)

    def _create_description_panel(self):
        """Crear el panel de descripción"""
        description_panel = Panel(self.master, "Descripción del Modelo")
        self.create_textbox(description_panel)
        return description_panel


# Ejemplo de uso
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Selector de Datos")
    app.geometry("1200x700")
    ctk.set_appearance_mode("dark")

    # Instanciar la clase
    panel = DescriptBox(app, app)  # Crear instancia

    # Crear y obtener el panel
    interface = panel._create_description_panel()  # Llamar al método

    # Empaquetar el panel para que sea visible
    interface.pack(fill="both", expand=True, padx=10, pady=10)
    app.mainloop()
