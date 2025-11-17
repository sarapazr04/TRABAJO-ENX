"""
Módulo para cargar un modelo previamente guardado (.joblib)
y mostrar su información en la interfaz gráfica.

Compatible con el formato extendido:
{
    "model": objeto_sklearn,
    "desc": str,
    "r2": [r2_train, r2_test],
    "mse": [mse_train, mse_test],
    "col_entrada": list[str],
    "col_salida": str
}
"""

import joblib
import customtkinter as ctk
from tkinter import filedialog
from .components import AppTheme, AppConfig, Panel, NotificationWindow, UploadButton
from .predict_gui import PredictionSection


class LoadModelPanel(ctk.CTkFrame):
    """
    Panel principal para cargar y visualizar modelos entrenados.

    Permite seleccionar un archivo .joblib, restaurar el modelo
    y mostrar su información (fórmula, métricas, columnas y descripción).
    """

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.result_container = None
        self._create_ui()

    # ================================================================
    # INTERFAZ GRÁFICA
    # ================================================================

    def _create_ui(self):
        """Crea la interfaz visual del panel de carga."""
        panel = Panel(self, "Cargar Modelo Guardado")
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        # Cabecera con botón y ruta
        header_frame = ctk.CTkFrame(panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 15))

        ctk.CTkLabel(
            header_frame,
            text="RUTA :",
            font=("Orbitron", 15, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
        ).pack(side="left", padx=(0, 10))

        self.path_frame = ctk.CTkFrame(
            header_frame,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6,
            border_width=1,
            border_color=AppTheme.BORDER,
        )
        self.path_frame.pack(side="left", fill="x", expand=True)

        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="Ningún modelo seleccionado",
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.DIM_TEXT,
        )
        self.path_label.pack(pady=10, padx=15)

        self.load_button = UploadButton(
            header_frame, text="Cargar Modelo", command=self._load_model
        )
        self.load_button.pack(side="right", padx=(15, 0))

        # Contenedor inferior de resultados
        self.result_container = ctk.CTkFrame(self, fg_color="transparent")
        self.result_container.pack(fill="both",
                                   expand=True, padx=20, pady=(0, 20))

    # ================================================================
    # LÓGICA DE CARGA
    # ================================================================

    def _load_model(self):
        """Abre el diálogo y carga el modelo desde archivo .joblib."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar modelo guardado",
            filetypes=[("Modelos de regresión (.joblib)", "*.joblib")],
        )

        if not file_path:
            return

        try:
            data = joblib.load(file_path)

            if not isinstance(data, dict) or "model" not in data:
                raise ValueError("El archivo no contiene un modelo válido.")

            self._display_model_info(data, file_path)

            notif = NotificationWindow(
                self.app,
                "Modelo Cargado",
                "El modelo se ha cargado correctamente.",
                "success",
            )
            self.after(2000, notif.destroy)

        except Exception as e:
            NotificationWindow(
                self.app,
                "Error al cargar modelo",
                f"No se pudo cargar el archivo:\n\n{str(e)}",
                "error",
            )

    # ================================================================
    # MÉTODOS AUXILIARES
    # ================================================================

    def _display_model_info(self, data, file_path):
        """
        Muestra la información completa del modelo cargado.
        """
        for widget in self.result_container.winfo_children():
            widget.destroy()

        model = data.get("model")
        desc = data.get("desc", "Sin descripción guardada.")
        r2 = data.get("r2")
        mse = data.get("mse")
        cols_in = data.get("col_entrada", [])
        col_out = data.get("col_salida", "Variable de salida desconocida")

        # Fórmula (si el modelo es lineal)
        if hasattr(model, "coef_") and hasattr(model, "intercept_"):
            coef_str = " + ".join(
                f"{coef:.4f}*{col}" for coef, col in zip(model.coef_, cols_in)
            )
            formula = f"y = {coef_str} + {model.intercept_:.4f}"
        else:
            formula = "Fórmula no disponible."

        # Panel principal de resultados
        info_panel = Panel(self.result_container, "Modelo Cargado")
        info_panel.pack(fill="both", expand=True, padx=20, pady=20)

        # Fórmula
        ctk.CTkLabel(
            info_panel,
            text=f" Fórmula del modelo:\n\n{formula}",
            font=("Consolas", 14),
            text_color=AppTheme.PRIMARY_TEXT,
            justify="left",
            wraplength=900,
        ).pack(pady=(10, 20), padx=25, anchor="w")

        # Métricas (si existen)
        if isinstance(r2, (list, tuple)) and isinstance(mse, (list, tuple)):
            metrics_text = (
                f" Métricas del modelo:\n\n"
                f"  R² Entrenamiento: {r2[0]:.4f}\n"
                f"  R² Test:          {r2[1]:.4f}\n"
                f"  ECM Entrenamiento: {mse[0]:.4f}\n"
                f"  ECM Test:          {mse[1]:.4f}"
            )
            ctk.CTkLabel(
                info_panel,
                text=metrics_text,
                font=AppConfig.BODY_FONT,
                text_color=AppTheme.SECONDARY_TEXT,
                justify="left",
                wraplength=700,
            ).pack(pady=(0, 20), padx=25, anchor="w")

        # Columnas de entrada/salida
        cols_text = (
            f" Columnas de entrada: {', '.join(cols_in)}\n"
            f" Columna de salida: {col_out}"
        )
        ctk.CTkLabel(
            info_panel,
            text=cols_text,
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.SECONDARY_TEXT,
            justify="left",
        ).pack(pady=(0, 20), padx=25, anchor="w")

        # Descripción guardada
        desc_panel = Panel(info_panel, "Descripción Guardada")
        desc_panel.pack(fill="x", padx=20, pady=(10, 20))

        desc_box = ctk.CTkTextbox(
            desc_panel,
            wrap="word",
            font=("Segoe UI", 14),
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            text_color=AppTheme.PRIMARY_TEXT,
            height=200,
        )
        desc_box.insert("0.0", desc)
        desc_box.configure(state="disabled")
        desc_box.pack(fill="both", expand=True, padx=15, pady=15)

        # Actualizar ruta en interfaz
        self.path_label.configure(text=file_path,
                                  text_color=AppTheme.PRIMARY_ACCENT)
        self.update_idletasks()

        prediction_panel = PredictionSection(self.app, self.result_container, cols_in, formula)
        prediction_panel.display_data()
