"""
Módulo para crear un panel de descripción de modelo con textbox.

Este módulo proporciona un componente GUI que permite al usuario ingresar
y almacenar la descripción de un modelo mediante un textbox personalizado
dentro de un panel con estilo.
"""
import customtkinter as ctk
import tkinter.font as tkfont
from .components import Panel


"""
    Widget de caja de texto para descripción de modelos.

    Proporciona una interfaz para crear y gestionar un textbox dentro de un
    panel, permitiendo al usuario ingresar descripciones de texto con formato
    y fuente personalizada.

    Attributes
    ----------
    master : ctk.CTk o ctk.CTkFrame
        Widget padre que contiene este componente.
    textbox : ctk.CTkTextbox o None
        Widget de texto donde el usuario puede escribir la descripción.
        Es None hasta que se llama a create_textbox().
"""


class DescriptBox:
    def __init__(self, master):
        """
        Inicializa el DescriptBox.

        Parameters
        ----------
        master : ctk.CTk o ctk.CTkFrame
            Widget padre que contendrá este componente.
        """

        self.master = master

    def get(self):
        """
        Obtiene el contenido completo del textbox.

        Returns
        -------
        str
            Todo el texto contenido en el textbox desde el inicio hasta
            el final, incluyendo saltos de línea. Si el textbox no ha sido
            creado, retorna una cadena vacía.

        Notes
        -----
        El método retorna todo el texto desde la posición "0.0" (inicio)
        hasta "end" (final). Incluye un salto de línea final automático
        que añade tkinter.
        """
        if self.textbox:
            return self.textbox.get("0.0", "end")
        return ""

    def set(self, text):
        """
        Establece el contenido del textbox.

        Parameters
        ----------
        text : str
            Texto a insertar en el textbox.

        Notes
        -----
        Este método primero borra todo el contenido existente y luego
        inserta el nuevo texto. Si el textbox no ha sido creado, la
        operación se omite.
        """
        if self.textbox:
            self.textbox.delete("0.0", "end")
            self.textbox.insert("0.0", text)

    def create_textbox(self, master):
        """
        Crea y configura el widget textbox dentro del panel.

        Crea un textbox con fuente personalizada (Inter, 13pt) y lo
        configura para que se expanda y llene todo el espacio disponible
        del contenedor padre.

        Parameters
        ----------
        master : ctk.CTkFrame
            Frame padre donde se colocará el textbox. Típicamente es
            el panel creado por _create_description_panel().

        Notes
        -----
        - Configura el grid del master para expansión automática
        - Usa pack geometry manager para el textbox
        - Aplica fuente personalizada mediante el widget tkinter interno
        - Si la fuente Inter no está disponible, usa la fuente por defecto
        """
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
        custom_font = tkfont.Font(family="Inter", size=16)
        self.textbox._textbox.configure(font=custom_font)

    def _create_description_panel(self):
        """
        Crea el panel completo con título y textbox.

        Construye un panel con el título "Descripción del Modelo" y
        añade dentro el textbox configurado para entrada de texto.

        Returns
        -------
        Panel
            Panel completo que contiene el textbox, listo para ser
            empaquetado o colocado en la interfaz principal.

        Notes
        -----
        Este método es el punto de entrada principal para crear la
        interfaz de descripción. Debe ser llamado después de crear
        la instancia de DescriptBox.
        """

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
    panel = DescriptBox(app)  # Crear instancia

    # Crear y obtener el panel
    interface = panel._create_description_panel()  # Llamar al método

    # Empaquetar el panel para que sea visible
    interface.pack(fill="both", expand=True, padx=10, pady=10)
    app.mainloop()
