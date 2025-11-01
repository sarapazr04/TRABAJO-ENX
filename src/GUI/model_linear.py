import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
from .components import Panel, UploadButton, NotificationWindow, AppTheme, AppConfig


class LinearModelPanel(ctk.CTkFrame):
    """
    Panel para crear un modelo lineal, mostrar la recta y métricas.
    """

    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self._create_ui()

    def _create_ui(self):
        panel = Panel(self, "Creación y Evaluación del Modelo Lineal")
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para crear el modelo
        self.train_button = UploadButton(
            panel, text="Crear Modelo Lineal", command=self._train_model)
        self.train_button.pack(pady=15)

        # Área de resultados
        self.result_text = ctk.CTkTextbox(panel, height=150)
        self.result_text.pack(fill="x", padx=20, pady=10)

        # Contenedor del gráfico
        self.graph_frame = ctk.CTkFrame(panel, fg_color=AppTheme.PRIMARY_BACKGROUND)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def _train_model(self):
        # Verificaciones
        if self.app.train_df is None or self.app.test_df is None:
            NotificationWindow(self.app, "Error", "Primero divide el dataset.", "error")
            return

        X_train = self.app.train_df[self.app.selection_panel.columnas_entrada]
        y_train = self.app.train_df[self.app.selection_panel.columna_salida]
        X_test = self.app.test_df[self.app.selection_panel.columnas_entrada]
        y_test = self.app.test_df[self.app.selection_panel.columna_salida]

        # Ajustar modelo
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Predicciones
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # Métricas
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)

        # Mostrar fórmula
        coefs = " + ".join(
            [f"{coef:.4f} * {col}" for coef, col in zip(model.coef_, X_train.columns)]
        )
        formula = f"{self.app.selection_panel.columna_salida} = {coefs} + {model.intercept_:.4f}"

        # Mostrar resultados en el cuadro de texto
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", f" Fórmula del Modelo:\n{formula}\n\n")
        self.result_text.insert(
            "end",
            f" Métricas:\n"
            f"Entrenamiento → R²={r2_train:.4f}, ECM={mse_train:.4f}\n"
            f"Test → R²={r2_test:.4f}, ECM={mse_test:.4f}\n",
        )

        self.result_text.configure(state="disabled")

        # Si es representable gráficamente
        if X_train.shape[1] == 1:
            self._plot_graph(
                X_train, y_train, X_test, y_test, model, self.app.selection_panel.columna_salida
            )
        else:
            NotificationWindow(
                self.app,
                "Aviso",
                "No se puede representar el gráfico (más de una variable de entrada).",
                "info",
            )

        NotificationWindow(self.app, "Éxito", "Modelo creado y evaluado correctamente.", "success")

    def _plot_graph(self, X_train, y_train, X_test, y_test, model, y_label):
        """Mostrar gráfico con recta de ajuste"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(X_train, y_train, color="blue", label="Entrenamiento")
        ax.scatter(X_test, y_test, color="orange", label="Test")

        x_range = np.linspace(
            min(X_train.values.min(), X_test.values.min()),
            max(X_train.values.max(), X_test.values.max()),
            100
        ).reshape(-1, 1)
        y_line = model.predict(x_range)
        ax.plot(x_range, y_line, color="red", label="Recta de ajuste")

        ax.set_xlabel(X_train.columns[0])
        ax.set_ylabel(y_label)
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
