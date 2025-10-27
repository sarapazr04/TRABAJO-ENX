import customtkinter as ctk
from sklearn.model_selection import train_test_split
from .components import Panel, NotificationWindow, AppTheme, AppConfig


class DataSplitPanel(ctk.CTkFrame):
    """
    Panel para dividir el DataFrame (ya preprocesado) en entrenamiento y test.
    - Control de % de train (test = 1 - train)
    - Semilla configurable (aleatorio reproducible)
    - Guarda los subconjuntos en la app: app.train_df y app.test_df
    - Muestra tamaños y notificaciones
    """

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.train_df = None
        self.test_df = None
        self._create_ui()

    # ---------------- UI ----------------
    def _create_ui(self):
        panel = Panel(self, "División de Datos en Entrenamiento y Test")
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        # Nota informativa
        info = ctk.CTkLabel(
            panel,
            text="Usa el dataset PREPROCESADO. (Obligatorio haber confirmado el preprocesado)",
            font=AppConfig.SMALL_FONT,
            text_color=AppTheme.SECONDARY_TEXT
        )
        info.pack(pady=(10, 0))

        # Slider % train
        self.slider_label = ctk.CTkLabel(
            panel, text="Porcentaje de entrenamiento: 80%")
        self.slider_label.pack(pady=(12, 6))

        self.slider = ctk.CTkSlider(
            panel, from_=50,
            to=95,
            number_of_steps=45,
            command=self._update_label
        )
        self.slider.set(80)
        self.slider.pack(fill="x", padx=20)

        # Semilla
        seed_frame = ctk.CTkFrame(panel, fg_color="transparent")
        seed_frame.pack(pady=12)
        ctk.CTkLabel(seed_frame, text="Semilla aleatoria:").pack(
            side="left", padx=6)
        self.seed_entry = ctk.CTkEntry(seed_frame, width=100)
        self.seed_entry.insert(0, "42")
        self.seed_entry.pack(side="left")

        # Botón dividir
        self.split_button = ctk.CTkButton(
            panel,
            text="Dividir Dataset",
            command=self._split_dataset,
            font=("Orbitron", 11, "bold"),
            height=AppConfig.BUTTON_HEIGHT,
            corner_radius=6,
            fg_color=AppTheme.PRIMARY_ACCENT,
            hover_color=AppTheme.HOVER_ACCENT,
            text_color="#ffffff",
        )
        self.split_button.pack(pady=12)

        # Resultado
        self.result_label = ctk.CTkLabel(
            panel, text="", text_color=AppTheme.SECONDARY_TEXT)
        self.result_label.pack(pady=(4, 12))

    def _update_label(self, value):
        self.slider_label.configure(
            text=f"Porcentaje de entrenamiento: {int(value)}%")

    # --------------- LÓGICA ---------------
    def _split_dataset(self):
        # Restricción: solo tras preprocesado
        if not getattr(self.app, "is_preprocessed", False):
            NotificationWindow(
                self.app,
                "Acción no permitida",
                "Primero debes PREPROCESAR y confirmar los cambios.",
                "warning"
            )
            return

        df = getattr(self.app, "preprocessed_df", None)
        if df is None:
            NotificationWindow(
                self.app,
                "Error",
                "No hay dataset preprocesado disponible.",
                "error")
            return

        if len(df) < 5:
            NotificationWindow(
                self.app,
                "Datos insuficientes",
                "No hay suficientes filas para realizar la separación (mínimo 5).",
                "error"
            )
            return

        # Parámetros
        train_size = self.slider.get() / 100
        try:
            random_state = int(self.seed_entry.get())
        except ValueError:
            NotificationWindow(
                self.app,
                "Error",
                "La semilla debe ser un número entero.",
                "error")
            return

        # División aleatoria reproducible
        train_df, test_df = train_test_split(
            df, train_size=train_size, random_state=random_state, shuffle=True
        )

        # Guardar internamente para historias posteriores (entrenar/evaluar)
        self.app.train_df = train_df
        self.app.test_df = test_df
        self.train_df = train_df
        self.test_df = test_df

        # Feedback visual
        self.result_label.configure(
            text=f"Entrenamiento: {len(train_df)} filas | Test: {len(test_df)} filas"
        )
        NotificationWindow(
            self.app,
            "División completada",
            f"Datos separados correctamente.\n"
            f"Entrenamiento: {len(train_df)} filas\nTest: {len(test_df)} filas",
            "success"
        )
