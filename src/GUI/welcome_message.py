import customtkinter as ctk
from PIL import Image
from .components import AppTheme, AppConfig


class WelcomeMessage():
    def __init__(self, app):

        self.app = app
        # Configurar ventana
        self.window = ctk.CTkToplevel(self.app)
        self.window.geometry("900x600")
        self.window.resizable(False, True)
        self.window.title("")

        # Crear el contenido del mensaje de bienvenida
        self._create_scroll_text()

    def _create_scroll_text(self):
        self.ext_frame = ctk.CTkScrollableFrame(self.window,
                                                fg_color="transparent")
        self.ext_frame.pack(fill="both", expand=True)
        self._create_header(self.ext_frame)
        self._load_create_text(self.ext_frame)

    def _create_header(self, master):
        self.header_frame = ctk.CTkFrame(master,
                                         fg_color=AppTheme.TERTIARY_BACKGROUND)
        self.header_frame.pack(fill="x",
                               expand=False,
                               padx=0, pady=(0, 10),
                               side="top")

        self.title = ctk.CTkLabel(
            self.header_frame,
            text="Bienvenid@ a Lunex Dataset Loader",
            font=("Orbitron", 20, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.title.pack(fill="both", expand=True, pady=20)

    def _load_create_text(self, master):
        self.load_create_model = InfoPanel(master, "Crear y cargar modelos")
        self.load_create_model.pack(fill="both",
                                    expand=True,
                                    padx=10, pady=(0, 10),
                                    side="top")
        body_text1 = ("Para empezar a crear un modelo a partir de datos, en la "
                      "pestaña de Crear modelo, haga click en Cargar Datos.")
        image1 = ctk.CTkImage(
            dark_image=Image.open("src/GUI/images/cargar_datos_guia.png"),
            size=(870, 196))

        body_text2 = ("Para cargar un modelo ya entrenado, en la "
                      "pestaña de Cargar modelo, haga click en Cargar Modelo.")

        textbox1 = ctk.CTkTextbox(self.load_create_model)
        textbox1.configure(font=AppConfig.BODY_FONT,
                           wrap="word",
                           text_color=AppTheme.PRIMARY_TEXT,
                           fg_color="transparent",
                           height=40)
        textbox1.insert("0.0", body_text1)
        textbox1.configure(state="disabled")
        textbox1.pack(fill="both", expand=False, pady=(5, 0))
        image_label1 = ctk.CTkLabel(
            self.load_create_model, image=image1, text="")
        image_label1.pack(fill="both", expand=True, pady=(5, 10))

        textbox2 = ctk.CTkTextbox(self.load_create_model)
        textbox2.configure(font=AppConfig.BODY_FONT,
                           wrap="word",
                           text_color=AppTheme.PRIMARY_TEXT,
                           fg_color="transparent",
                           height=40)
        textbox2.insert("0.0", body_text2)
        textbox2.configure(state="disabled")
        textbox2.pack(fill="both", expand=False, pady=(5, 0))

        image2 = ctk.CTkImage(
            dark_image=Image.open("src/GUI/images/cargar_modelo_guia.png"),
            size=(870, 196)
        )

        image_label2 = ctk.CTkLabel(
            self.load_create_model, image=image2, text=""
        )
        image_label2.pack(fill="both", expand=True, pady=(5, 10))


class InfoPanel(ctk.CTkFrame):
    def __init__(self, master, title):
        # Crear el frame
        super().__init__(
            master,
            corner_radius=8,
            fg_color="transparent",
        )

        # Crear la barra de titulo
        self._create_title_bar(title)

    def _create_title_bar(self, title):
        """Crear la barra de titulo del panel"""
        title_bar = ctk.CTkFrame(
            self,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6,
            height=38
        )
        title_bar.pack(fill="x", padx=2, pady=2)
        title_bar.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            title_bar,
            text=title,
            font=("Orbitron", 15, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.title_label.pack(pady=10, padx=15, anchor="w")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x400")
    a = WelcomeMessage(app)
    app.mainloop()
