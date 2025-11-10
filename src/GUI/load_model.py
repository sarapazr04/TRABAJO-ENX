"""
Módulo para cargar un modelo previamente guardado (.joblib)
y actualizar la interfaz con su información.
"""

import customtkinter as ctk
from tkinter import filedialog
import joblib
from .components import (
    AppTheme, AppConfig, Panel, NotificationWindow, UploadButton
)


class LoadModelPanel(ctk.CTkFrame):
    """Panel principal para cargar un modelo entrenado desde archivo .joblib."""

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.result_container = None  # <- contenedor para limpiar resultados fácilmente
        self._create_ui()

    # ================================================================
    # INTERFAZ VISUAL
    # ================================================================
    def _create_ui(self):
        """Crea el panel principal (botón + ruta)."""
        panel = Panel(self, "Cargar Modelo Guardado")
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        frame = ctk.CTkFrame(panel, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(10, 15))

        self.tag_label = ctk.CTkLabel(
            frame,
            text="RUTA :",
            font=("Orbitron", 15, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.tag_label.pack(side="left", padx=(0, 10))

        # Cuadro de texto de ruta
        self.path_frame = ctk.CTkFrame(
            frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        self.path_frame.pack(side="left", fill="x", expand=True)

        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="Ningún modelo seleccionado",
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.DIM_TEXT
        )
        self.path_label.pack(pady=10, padx=15)

        # Botón para abrir el diálogo
        self.load_button = UploadButton(
            frame,
            text="Cargar Modelo",
            command=self._load_model
        )
        self.load_button.pack(side="right", padx=(15, 0))

        # Frame vacío para mostrar resultados (fórmula, descripción, etc.)
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # ================================================================
    # LÓGICA DE CARGA DE MODELO
    # ================================================================
    def _load_model(self):
        """Abre el diálogo de selección de archivo y carga el modelo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar modelo guardado",
            filetypes=[("Modelos de regresión (.joblib)", "*.joblib")]
        )

        if not file_path:
            return

        try:
            data_loaded = joblib.load(file_path)

            if not isinstance(data_loaded, dict) or "model" not in data_loaded:
                raise ValueError("El archivo no contiene un modelo válido.")

            # Limpiar la interfaz principal (modo 'crear modelo')
            self._reset_app_state()

            # Mostrar nuevo modelo (borra resultados anteriores)
            self._display_model_info(data_loaded, file_path)

            # Notificación de éxito (sin botón)
            notif = NotificationWindow(
                self.app,
                "Modelo Cargado",
                "El modelo ha sido recuperado correctamente.",
                "success"
            )
            self.after(2000, notif.destroy)

        except Exception as e:
            NotificationWindow(
                self.app,
                "Error al cargar modelo",
                f"No se pudo cargar el archivo:\n\n{str(e)}",
                "error"
            )

    # ================================================================
    # FUNCIONES AUXILIARES
    # ================================================================
    def _reset_app_state(self):
        """Elimina secciones previas del modo 'Crear Modelo'."""
        for frame in [
            getattr(self.app, "selection_frame", None),
            getattr(self.app, "_split_panel_frame", None),
            getattr(self.app, "_model_panel_frame", None),
        ]:
            try:
                if frame and frame.winfo_exists():
                    frame.destroy()
            except Exception:
                pass

    def _display_model_info(self, data, file_path):
        """Muestra la información básica del modelo cargado."""
        # 🔹 Limpiar solo el contenedor de resultados previos
        for w in self.result_container.winfo_children():
            w.destroy()

        model = data.get("model")
        desc = data.get("desc", "Sin descripción guardada.")

        # Intentar obtener fórmula si el modelo es lineal
        if hasattr(model, "coef_") and hasattr(model, "intercept_"):
            coef_str = " + ".join(
                [f"{c:.4f}·x{i+1}" for i, c in enumerate(model.coef_)]
            )
            formula = f"y = {coef_str} + {model.intercept_:.4f}"
        else:
            formula = "Fórmula no disponible."

        # Crear panel de información
        panel = Panel(self.result_container, "Modelo Cargado")
        panel.pack(fill="both", expand=True, padx=20, pady=(20, 20))

        # Mostrar fórmula
        label_formula = ctk.CTkLabel(
            panel,
            text=f" Fórmula del modelo:\n\n{formula}",
            font=("Consolas", 14),
            text_color=AppTheme.PRIMARY_TEXT,
            justify="left",
            wraplength=900
        )
        label_formula.pack(pady=(10, 20), padx=25, anchor="w")

        # Mostrar descripción
        desc_panel = Panel(panel, "Descripción Guardada")
        desc_panel.pack(fill="x", padx=20, pady=(10, 20))

        desc_box = ctk.CTkTextbox(
            desc_panel,
            wrap="word",
            font=("Segoe UI", 14),
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            text_color=AppTheme.PRIMARY_TEXT,
            height=200
        )
        desc_box.insert("0.0", desc)
        desc_box.configure(state="disabled")
        desc_box.pack(fill="both", expand=True, padx=15, pady=15)

        # Actualizar visualmente la ruta
        self.path_label.configure(
            text=file_path,
            text_color=AppTheme.PRIMARY_ACCENT
        )

        self.update_idletasks()
