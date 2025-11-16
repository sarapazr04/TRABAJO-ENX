import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from .components import Panel, UploadButton, NotificationWindow, AppTheme, AppConfig
from .desc_model import DescriptBox
from .predict_gui import PredictionSection


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
        # Cachear canvas para evitar lags
        self.current_canvas = None
        self._create_ui()
        self._train_model()

    # ============================================================
    # INTERFAZ GRÁFICA
    # ============================================================

    def _create_ui(self):
        """Crea la estructura visual del panel (botón, resultados y gráfico)"""

        panel = Panel(self, "Creación y Evaluación del Modelo Lineal")
        panel.pack(fill="both", expand=True, padx=10, pady=10)

        # ═══════════════════════════════════════════════════════════
        # CONTENEDOR PRINCIPAL CON LAYOUT DE 2 COLUMNAS (GRID)
        # ═══════════════════════════════════════════════════════════
        # Este contenedor organizará los resultados (izquierda) y
        # el gráfico (derecha) en dos columnas

        self.main_container = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar el grid: 2 columnas
        # Columna 0 (resultados): 40% del espacio (weight=4)
        # Columna 1 (gráfico): 60% del espacio (weight=6)
        self.main_container.grid_columnconfigure(0, weight=4)
        self.main_container.grid_columnconfigure(1, weight=6)
        self.main_container.grid_rowconfigure(0, weight=1)

        # ─────────────────────────────────────────────────────────
        # COLUMNA IZQUIERDA: RESULTADOS (Fórmula + Métricas)
        # ─────────────────────────────────────────────────────────
        self.results_container = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.results_container.grid(
            row=0,
            column=0,
            sticky="nsew",  # Se expande en todas direcciones
            padx=(0, 10)    # Espacio a la derecha para separar del gráfico
        )

        # ─────────────────────────────────────────────────────────
        # COLUMNA DERECHA: GRÁFICO
        # ─────────────────────────────────────────────────────────
        self.graph_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=AppTheme.PRIMARY_BACKGROUND
        )
        self.graph_frame.grid(
            row=0,
            column=1,
            sticky="nsew",  # Se expande en todas direcciones
            padx=(10, 0)    # Espacio a la izquierda
        )

        # Contenedor de la descripcion del modelo
        self.description_frame = ctk.CTkFrame(
            panel,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            height=400
        )
        self.description_frame.pack(
            fill="both", expand=True, padx=20, pady=10)
        self.description_frame.pack_propagate(False)

        # Botón de guardar modelo
        self._create_save_button(panel)

        # Contenedor de la predicción del modelo

        self.prediction_frame = ctk.CTkFrame(
            panel,
            fg_color=AppTheme.PRIMARY_BACKGROUND
        )
        self.prediction_frame.pack(fill="x", expand=True, padx=20, pady=10)

    def _display_results(self, formula, r2_train, r2_test, mse_train, mse_test):
        """
        Muestra la fórmula y las métricas en la columna izquierda.

        Organización vertical:
        1. Fórmula del modelo
        2. Métricas de entrenamiento
        3. Métricas de test
        """
        # Limpiar resultados anteriores
        for widget in self.results_container.winfo_children():
            widget.destroy()

        # ═══════════════════════════════════════════════════════════
        # 1. PANEL DE FÓRMULA
        # ═══════════════════════════════════════════════════════════
        formula_panel = ctk.CTkFrame(
            self.results_container,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        formula_panel.pack(fill="x", pady=(0, 12))

        # Título de la sección
        formula_title = ctk.CTkLabel(
            formula_panel,
            text="Fórmula Del Modelo",
            font=("Orbitron", 13, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        formula_title.pack(pady=(12, 8), padx=15, anchor="w")

        # Separador
        separator = ctk.CTkFrame(
            formula_panel,
            height=1,
            fg_color=AppTheme.BORDER
        )
        separator.pack(fill="x", padx=15, pady=(0, 12))

        # Fórmula con wraplength ajustado para columna más estrecha
        formula_label = ctk.CTkLabel(
            formula_panel,
            text=formula,
            font=AppConfig.MONO_FONT,
            text_color=AppTheme.PRIMARY_TEXT,
            wraplength=400,  # Ajustado para columna izquierda
            anchor="center"
        )
        formula_label.pack(pady=(0, 15), padx=15, anchor="center")

        # ═══════════════════════════════════════════════════════════
        # 2. PANEL DE MÉTRICAS DE ENTRENAMIENTO
        # ═══════════════════════════════════════════════════════════
        train_panel = ctk.CTkFrame(
            self.results_container,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        train_panel.pack(fill="x", pady=(0, 12))

        train_title = ctk.CTkLabel(
            train_panel,
            text="Entrenamiento",
            font=("Orbitron", 12, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        train_title.pack(pady=(12, 8), padx=15, anchor="w")

        train_sep = ctk.CTkFrame(
            train_panel, height=1, fg_color=AppTheme.BORDER)
        train_sep.pack(fill="x", padx=15, pady=(0, 10))

        # Métricas de entrenamiento
        self._create_metric_row(train_panel, "R²", r2_train, r2_test)
        self._create_metric_row(
            train_panel, "ECM", mse_train, mse_test, is_ecm=True)

        # ═══════════════════════════════════════════════════════════
        # 3. PANEL DE MÉTRICAS DE TEST
        # ═══════════════════════════════════════════════════════════
        test_panel = ctk.CTkFrame(
            self.results_container,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        test_panel.pack(fill="x", pady=(0, 0))

        test_title = ctk.CTkLabel(
            test_panel,
            text="Test",
            font=("Orbitron", 12, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        test_title.pack(pady=(12, 8), padx=15, anchor="w")

        # Separador
        test_sep = ctk.CTkFrame(test_panel, height=1, fg_color=AppTheme.BORDER)
        test_sep.pack(fill="x", padx=15, pady=(0, 10))

        # Métricas de test
        self._create_metric_row(test_panel, "R²", r2_test, r2_train)
        self._create_metric_row(
            test_panel, "ECM", mse_test, mse_train, is_ecm=True)

    def _create_metric_row(self,
                           parent,
                           metric_name,
                           value,
                           compare_value,
                           is_ecm=False):
        """
        Crea una fila con nombre y valor de métrica.

        Parameters
        ----------
        parent : CTkFrame
            Frame contenedor
        metric_name : str
            Nombre de la métrica (ej: "R²", "ECM")
        value : float
            Valor de la métrica
        compare_value : float
            Valor de comparación (para determinar color)
        is_ecm : bool
            True si es ECM (menor es mejor), False si es R² (mayor es mejor)
        """
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=4)

        # Nombre de la métrica
        name_label = ctk.CTkLabel(
            row_frame,
            text=f"{metric_name}:",
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.SECONDARY_TEXT,
            width=60,
            anchor="w"
        )
        name_label.pack(side="left")

        # Determinar color segun la comparacion
        if is_ecm:
            # Para ECM: menor es mejor
            color = AppTheme.SUCCES if value <= compare_value else AppTheme.WARNING
        else:
            # Para R²: mayor es mejor
            color = AppTheme.SUCCES if value >= compare_value else AppTheme.WARNING

        # Valor de la métrica
        value_label = ctk.CTkLabel(
            row_frame,
            text=f"{value:.4f}",
            font=AppConfig.MONO_FONT,
            text_color=color
        )
        value_label.pack(side="left", padx=(10, 0))

    def _create_description_panel(self, formula, r2_test, y_label):
        """
        Crea el panel de descripción del modelo.

        Parameters
        ----------
        formula : str
            Fórmula del modelo lineal
        r2_test : float
            R² del conjunto de test para incluir en la descripción
        y_label : str
            Nombre de la variable de salida
        """
        # Limpiar panel anterior si existe
        for widget in self.description_frame.winfo_children():
            widget.destroy()

        # Crear panel
        desc_container = ctk.CTkFrame(
            self.description_frame,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        desc_container.pack(fill="both", expand=True)

        # Título del panel
        desc_title = ctk.CTkLabel(
            desc_container,
            text="Descripción del Modelo",
            font=("Orbitron", 13, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        desc_title.pack(pady=(12, 8), padx=15, anchor="w")

        # Separador
        separator = ctk.CTkFrame(
            desc_container,
            height=1,
            fg_color=AppTheme.BORDER
        )
        separator.pack(fill="x", padx=15, pady=(0, 12))

        # Crear el textbox para descripción
        self.desc_box = DescriptBox(desc_container)
        self.desc_box.create_textbox(desc_container)

        # Texto inicial orientativo
        descripcion_inicial = (
            f"Modelo creado correctamente.\n\n"
            f"Fórmula del modelo:\n"
            f"{formula}\n"
            f"═══════════════════════════════════════════════════\n"
            f"Interpretación:\n"
            f"1. Coeficientes: "
            f"Cada coeficiente indica el cambio promedio en '{y_label}' cuando\n"
            f"   su variable correspondiente aumenta en 1 unidad, manteniendo\n"
            f"   las demás variables constantes.\n\n"
            f"2. Capacidad Predictiva: "
            f"R² (test) = {r2_test:.4f} muestra la capacidad de generalización del modelo.\n"
            f"   El modelo explica el {r2_test*100:.1f}% de la variabilidad de '{y_label}'.\n"
            f"═══════════════════════════════════════════════════\n\n"
            f"Escribe aquí tus observaciones adicionales..."
        )
        self.desc_box.set(descripcion_inicial)

    def _create_prediction_panel(self, master, formula):
        """Crea el panel de predicción del modelo."""
        # Limpiar panel anterior si existe
        for widget in self.prediction_frame.winfo_children():
            widget.destroy()

        # Crear el panel de predicción
        prediction_panel = PredictionSection(self.app, master, self.app.selection_panel.columnas_entrada, formula)
        prediction_panel.display_data()


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
        # ===================================
        # 1. VALIDACIÓN: Verificar que los datos están divididos
        # ===================================
        if self.app.train_df is None or self.app.test_df is None:
            NotificationWindow(
                self.app,
                "Error",
                "Primero divide el dataset en entrenamiento y test.",
                "error"
            )
            return

        # ===================================
        # 2. OBTENER DATOS CON LAS COLUMNAS SELECCIONADAS
        # ===================================
        X_train = self.app.train_df[self.app.selection_panel.columnas_entrada]
        y_train = self.app.train_df[self.app.selection_panel.columna_salida]
        X_test = self.app.test_df[self.app.selection_panel.columnas_entrada]
        y_test = self.app.test_df[self.app.selection_panel.columna_salida]

        # ===================================
        # 3. ENTRENAR EL MODELO
        # ===================================
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Almacenar el modelo en el panel para guardarlo después
        self.model = model

        # ===================================
        # 4. CALCULAR PREDICCIONES
        # ===================================
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        # ===================================
        # 5. CALCULAR MÉTRICAS
        # ===================================
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        mse_train = mean_squared_error(y_train, y_pred_train)
        mse_test = mean_squared_error(y_test, y_pred_test)

        self.r2 = [r2_train, r2_test]
        self.mse = [mse_train, mse_test]

        # ===================================
        # 6. CONSTRUIR FÓRMULA
        # ===================================
        coef_terms = []
        for coef, col in zip(model.coef_, X_train.columns):
            # Formatear cada término con su signo
            if coef >= 0:
                coef_terms.append(f"{coef:.4f} * {col}")
            else:
                coef_terms.append(f"{coef:.4f} * {col}")

        # Construir fórmula completa
        intercept = model.intercept_
        if intercept >= 0:
            formula = f"{self.app.selection_panel.columna_salida} = {' + '.join(coef_terms)} + {intercept:.4f}"
        else:
            formula = f"{self.app.selection_panel.columna_salida} = {' + '.join(coef_terms)} - {abs(intercept):.4f}"

        # ===================================
        # 7. MOSTRAR RESULTADOS (fórmula y métricas)
        # ===================================
        self._display_results(formula, r2_train, r2_test, mse_train, mse_test)

        # ===================================
        # 8. GRÁFICO (solo si hay 1 variable de entrada)
        # ===================================
        if X_train.shape[1] == 1:
            self._plot_graph(
                X_train,
                y_train,
                X_test,
                y_test,
                y_pred_test,  # IMPORTANTE: Pasar las predicciones
                model,
                self.app.selection_panel.columna_salida
            )
        else:
            # Si hay múltiples variables, ocultar el frame del gráfico
            self.graph_frame.grid_forget()

            NotificationWindow(
                self.app,
                "Aviso",
                "No se puede representar el gráfico (más de una variable de entrada).",
                "info"
            )

        # ===================================
        # 9. PANEL DE DESCRIPCIÓN DEL MODELO
        # ===================================
        self._create_description_panel(
            formula,
            r2_test,
            self.app.selection_panel.columna_salida
        )

        # ===================================
        # 10. PANEL DE PREDICCIÓN DEL MODELO
        # ===================================
        self._create_prediction_panel(self.prediction_frame, formula)


        # ===================================
        # 11. NOTIFICACIÓN DE ÉXITO
        # ===================================
        NotificationWindow(
            self.app,
            "Éxito",
            "Modelo creado y evaluado correctamente.",
            "success"
        )

    # ============================================================
    # GRÁFICO: PUNTOS Y RECTA DE AJUSTE CON VALORES REALES Y PREDICHOS
    # ============================================================

    def _plot_graph(self, X_train, y_train, X_test, y_test, y_pred_test, model, y_label):
        """
        Dibuja los puntos de entrenamiento y test junto con la recta de ajuste.

        Para los datos de TEST, muestra valores reales y predichos.

        Parameters
        ----------
        X_train : pd.DataFrame
            Variables de entrada del conjunto de entrenamiento.
        y_train : pd.Series
            Variable de salida del conjunto de entrenamiento.
        X_test : pd.DataFrame
            Variables de entrada del conjunto de test.
        y_test : pd.Series
            Variable de salida REAL del conjunto de test.
        y_pred_test : np.ndarray
            Valores PREDICHOS por el modelo para el conjunto de test.
        model : LinearRegression
            Modelo entrenado.
        y_label : str
            Nombre de la variable dependiente (para el eje Y).
        """

        # Eliminar gráfico previo si lo hubiera
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # ═══════════════════════════════════════════════════════════
        # CONTENEDOR DEL GRAFICO CON TITULO
        # ═══════════════════════════════════════════════════════════
        graph_container = ctk.CTkFrame(
            self.graph_frame,
            fg_color=AppTheme.SECONDARY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        graph_container.pack(fill="both", expand=True)

        # Título del gráfico
        graph_title = ctk.CTkLabel(
            graph_container,
            text="Gráfica de Regresión",
            font=("Orbitron", 13, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        graph_title.pack(pady=(12, 8), padx=15, anchor="w")

        # Separador
        separator = ctk.CTkFrame(
            graph_container,
            height=1,
            fg_color=AppTheme.BORDER
        )
        separator.pack(fill="x", padx=15, pady=(0, 12))

        # Frame interno para el gráfico
        plot_frame = ctk.CTkFrame(
            graph_container,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6
        )
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # ═══════════════════════════════════════════════════════════
        # CREAR GRAFICO CON TODOS LOS DATOS
        # ═══════════════════════════════════════════════════════════

        # Crear figura con altura reducida para que coincida con columna izquierda
        fig, ax = plt.subplots(figsize=(8, 3.8), dpi=85)

        # ─────────────────────────────────────────────────────────
        # DATOS DE ENTRENAMIENTO
        # ─────────────────────────────────────────────────────────
        ax.scatter(
            X_train,
            y_train,
            color="#2ea88c",
            label="Entrenamiento",
            s=25,
            alpha=0.5,
            edgecolors='none'
        )

        # ─────────────────────────────────────────────────────────
        # DATOS DE TEST : VALORES REALES
        # ─────────────────────────────────────────────────────────
        ax.scatter(
            X_test,
            y_test,
            color="#dc5539",
            label="Test (Real)",
            s=25,
            alpha=0.6,
            edgecolors='#8b2e1f',
            linewidths=0.8
        )

        # ─────────────────────────────────────────────────────────
        # 3. DATOS DE TEST : VALORES PREDICHOS
        # ─────────────────────────────────────────────────────────
        # Usar un marcador diferente
        ax.scatter(
            X_test,
            y_pred_test,
            color='#4da6ff',
            label="Test (Predicho)",
            s=60,
            alpha=0.9,
            marker='+',  # Marcador de cruz
            linewidths=2.5
        )

        # ─────────────────────────────────────────────────────────
        # RECTA DE AJUSTE DEL MODELO
        # ─────────────────────────────────────────────────────────
        x_range = np.linspace(
            min(X_train.values.min(), X_test.values.min()),
            max(X_train.values.max(), X_test.values.max()),
            100
        )
        # Convertir a DataFrame con el mismo nombre de columna
        x_range_df = pd.DataFrame(x_range, columns=X_train.columns)
        y_line = model.predict(x_range_df)

        ax.plot(
            x_range,
            y_line,
            color="#ff4444",
            label="Recta de ajuste",
            linewidth=2.5,
            zorder=10
        )

        # ─────────────────────────────────────────────────────────
        # CONFIGURACION DE ETIQUETAS Y ESTILO
        # ─────────────────────────────────────────────────────────
        ax.set_xlabel(X_train.columns[0], fontsize=10, fontweight='bold')
        ax.set_ylabel(y_label, fontsize=10, fontweight='bold')
        ax.legend(loc='best', fontsize=8, framealpha=0.9)
        ax.grid(True, alpha=0.25, linestyle='--')

        # Ajustar layout para evitar recortes
        plt.tight_layout()

        # Limpiar canvas anterior si existe
        if self.current_canvas is not None:
            try:
                self.current_canvas.get_tk_widget().destroy()
            except Exception:
                pass

        # Crear y almacenar el nuevo canvas
        self.current_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.current_canvas.draw()

        # Obtener el widget de tkinter
        canvas_widget = self.current_canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)

        # Desactivar redibujado automático durante scroll
        canvas_widget.configure(takefocus=0)

        # Cerrar la figura de matplotlib para liberar recursos
        plt.close(fig)

    # ============================================================
    # GUARDAR MODELO
    # ============================================================

    def save_model(self, master, compress=3):
        """
        Guarda un modelo entrenado en un archivo .joblib.

        Abre un diálogo para que el usuario elija dónde guardar el archivo.

        Parameters
        ----------
        master : widget
            Widget padre para el diálogo
        compress : int
            Nivel de compresión (por defecto 3)

        Returns
        -------
        str or None
            Ruta donde se guardó el modelo, o None si el usuario canceló.
        """
        folder_path = filedialog.askdirectory(
            parent=master,
            title="Selecciona la carpeta para guardar el modelo",
            mustexist=True
        )

        if not folder_path:
            NotificationWindow(
                master,
                "Error",
                "No se seleccionó ninguna ruta",
                "error"
            )
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"modelo_{timestamp}.joblib"
        file_path = Path(folder_path) / file_name

        try:
            desc = self.desc_box.get()
            data_to_save = {
                "model": self.model,
                "desc": desc,
                "r2": self.r2,
                "mse": self.mse,
                "col_entrada": self.app.selection_panel.columnas_entrada,
                "col_salida": self.app.selection_panel.columna_salida
            }

            joblib.dump(data_to_save, file_path, compress=compress)
            NotificationWindow(
                master,
                "Éxito",
                f"Modelo guardado correctamente en:\n{file_path}",
                "success"
            )
            return str(file_path)
        except Exception as e:
            NotificationWindow(
                master,
                "Error",
                f"Error al guardar el modelo:\n{str(e)}",
                "error"
            )
            return None

    def _create_save_button(self, master):
        """Crea el botón para guardar el modelo"""
        self.save_button = ctk.CTkButton(
            master,
            text="💾 Guardar Modelo",
            command=lambda: self.save_model(master),
            font=("Orbitron", 12, "bold"),
            height=AppConfig.BUTTON_HEIGHT,
            corner_radius=6,
            fg_color=AppTheme.PRIMARY_ACCENT,
            hover_color=AppTheme.HOVER_ACCENT,
            text_color="#ffffff"
        )
        self.save_button.pack(pady=15)
