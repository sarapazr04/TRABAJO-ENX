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
    Panel para la creación y evaluación de un modelo de regresión lineal.
    Permite entrenar el modelo con los datos de entrenamiento, evaluar con test
    y mostrar fórmula, métricas y representación gráfica si procede.
    """

    def __init__(self, master, app):
        """
        Inicializa el panel y su interfaz.

        Parameters
        ----------
        master : tk.Widget
            Contenedor padre del panel.
        app : DataLoaderApp
            Instancia principal de la aplicación (para acceder a datos y estado).
        """
        super().__init__(master)
        self.app = app
        self._create_ui()

    # ============================================================
    # INTERFAZ GRÁFICA
    # ============================================================
    
    def _create_ui(self):
        """Crea la estructura visual del panel (botón, resultados y gráfico)."""

        panel = Panel(self, "Creación y Evaluación del Modelo Lineal")
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        # # Botón principal: entrenar y evaluar modelo lineal
        self.train_button = UploadButton(
            panel, text="Crear Modelo Lineal", command=self._train_model)
        self.train_button.pack(pady=15)

        # Área de resultados
        self.result_text = ctk.CTkTextbox(panel, height=150)
        self.result_text.pack(fill="x", padx=20, pady=10)

        # Contenedor del gráfico
        self.graph_frame = ctk.CTkFrame(panel, fg_color=AppTheme.PRIMARY_BACKGROUND)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ============================================================
    # ENTRENAMIENTO Y EVALUACIÓN DEL MODELO
    # ============================================================

    def _train_model(self):
        """
        Entrena el modelo de regresión lineal y muestra resultados.

        - Ajusta el modelo solo con el conjunto de entrenamiento.
        - Calcula predicciones y métricas en train y test.
        - Muestra fórmula y resultados numéricos.
        - Dibuja la recta si solo hay una variable de entrada.
        """
        # Verificar que los datos están cargados y divididos
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

    # ============================================================
    # GRÁFICO: PUNTOS Y RECTA DE AJUSTE
    # ============================================================

    def _plot_graph(self, X_train, y_train, X_test, y_test, model, y_label):
        """
        Dibuja los puntos de entrenamiento y test junto con la recta de ajuste.

        Parameters
        ----------
        X_train, X_test : pd.DataFrame
            Variables de entrada.
        y_train, y_test : pd.Series
            Variable de salida.
        model : LinearRegression
            Modelo entrenado.
        y_label : str
            Nombre de la variable dependiente (para el eje Y).
        """

        # Eliminar gráfico previo si lo hubiera
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Crear figura
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
