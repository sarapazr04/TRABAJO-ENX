import customtkinter as ctk
from sklearn.model_selection import train_test_split
from .components import (Panel,
                         NotificationWindow, AppTheme, AppConfig, UploadButton)


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

        # Label del slider
        self.slider_label = ctk.CTkLabel(
            panel,
            text="Porcentaje de entrenamiento: 80%",
            font=AppConfig.BODY_FONT
        )
        self.slider_label.pack(pady=(15, 10))

        controls_frame = ctk.CTkFrame(panel, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Semilla aleatoria
        seed_container = ctk.CTkFrame(controls_frame, fg_color="transparent")
        seed_container.pack(side="left", padx=(0, 15))

        seed_label = ctk.CTkLabel(
            seed_container,
            text="Semilla :",
            font=AppConfig.BODY_FONT
        )
        seed_label.pack(side="left", padx=(0, 8))

        self.seed_entry = ctk.CTkEntry(
            seed_container,
            width=100,
            height=32,
            font=AppConfig.BODY_FONT,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            border_color=AppTheme.BORDER
        )
        self.seed_entry.insert(0, "42")
        self.seed_entry.pack(side="left")

        # Botón dividir
        self.split_button = UploadButton(
            controls_frame,
            text="Dividir Dataset y crear modelo",
            command=self._split_dataset  # Función a ejecutar al hacer clic
        )
        self.split_button.pack(side="right")

        # Slider
        slider_container = ctk.CTkFrame(
            controls_frame,
            fg_color="transparent",
        )
        slider_container.pack(side="left", fill="x", expand=True, padx=(0, 15))

        self.slider = ctk.CTkSlider(
            slider_container,
            from_=50,
            to=95,
            command=self._update_label,
            height=16,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            progress_color=AppTheme.PRIMARY_ACCENT,
            button_color=AppTheme.PRIMARY_ACCENT,
            button_hover_color=AppTheme.HOVER_ACCENT
        )
        self.slider.set(80)
        self.slider.pack(fill="x", pady=6)

        # Etiquetas de rango (50% - 95%)
        range_frame = ctk.CTkFrame(slider_container, fg_color="transparent")
        range_frame.pack(fill="x")

        ctk.CTkLabel(
            range_frame,
            text="50%",
            font=("Segoe UI", 14),
            text_color=AppTheme.DIM_TEXT,
        ).pack(side="left")

        ctk.CTkLabel(
            range_frame,
            text="95%",
            font=("Segoe UI", 14),
            text_color=AppTheme.DIM_TEXT,
        ).pack(side="right")

        # Resultado
        self.result_label = ctk.CTkLabel(
            panel,
            text="",
            text_color=AppTheme.SECONDARY_TEXT,
            font=AppConfig.BODY_FONT
        )
        self.result_label.pack(pady=(4, 12))

    def _update_label(self, value):
        """Actualizar el label con el porcentaje actual"""
        self.slider_label.configure(
            text=f"Porcentaje de entrenamiento: {value:.1f}%")

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

        self.app.set_split_completed()
