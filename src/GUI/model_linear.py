import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
from .components import Panel, UploadButton, NotificationWindow, AppTheme, AppConfig
from .desc_model import DescriptBox 


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

        # Contenedor de resultados 
        self.results_container = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        self.results_container.pack(fill="x", padx=20, pady=10)

        # Contenedor del gráfico
        self.graph_frame = ctk.CTkFrame(panel, fg_color=AppTheme.PRIMARY_BACKGROUND)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Contenedor de la descripcion del modelo
        self.description_frame = ctk.CTkFrame(
            panel, 
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            height=400  
        )
        self.description_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.description_frame.pack_propagate(False) 

    
    def _display_results(self, formula, r2_train, r2_test, mse_train, mse_test):
        # Limpiar resultados anteriores

        for widget in self.results_container.winfo_children():
            widget.destroy()
        
        formula_panel = ctk.CTkFrame(
            self.results_container,
            fg_color=AppTheme.SECONDERY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        formula_panel.pack(fill="x", pady=(0, 12))

        # Título de la sección
        formula_title = ctk.CTkLabel(
            formula_panel,
            text="Formula Del Modelo",
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

        formula_label = ctk.CTkLabel(
            formula_panel, 
            text=formula, 
            font=("Consolas", 13),
            text_color=AppTheme.PRIMARY_TEXT,
            wraplength=800,
            anchor="center"
        )
        formula_label.pack(pady=(0, 15), padx=20, anchor="center")

        # Metricas
        metrics_container = ctk.CTkFrame(
            self.results_container,
            fg_color="transparent"
        )
        metrics_container.pack(fill="x")

        # Configurar grid para dos columnas iguales
        metrics_container.grid_columnconfigure(0, weight=1)
        metrics_container.grid_columnconfigure(1, weight=1)

        # Columna Entrenamiento
        train_panel = ctk.CTkFrame(
            metrics_container,
            fg_color=AppTheme.SECONDERY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        train_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        train_title = ctk.CTkLabel(
            train_panel,
            text="Entrenamiento",
            font=("Orbitron", 12, "bold"),
            text_color=AppTheme.PRIMARY_TEXT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            corner_radius=6
        )
        train_title.pack(pady=(12, 8), padx=15, anchor="w")

        train_sep = ctk.CTkFrame(train_panel, height=1, fg_color=AppTheme.BORDER)
        train_sep.pack(fill="x", padx=15, pady=(0, 10))

        # Metricas de entrenamiento
        self._create_metric_row(train_panel, "R²", r2_train, r2_test)
        self._create_metric_row(train_panel, "ECM", mse_train, mse_test, is_ecm=True)

        # Columna Test
        test_panel = ctk.CTkFrame(
            metrics_container,
            fg_color=AppTheme.SECONDERY_BACKGROUND, 
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        test_panel.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

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

        # Metricas de test
        self._create_metric_row(test_panel, "R²", r2_test, r2_train)
        self._create_metric_row(test_panel, "ECM", mse_test, mse_train, is_ecm=True)


    def _create_metric_row(self, parent, metric_name, value, compare_value, is_ecm=False):
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
            font=("Segoe UI", 12, "bold"),
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
            font=("Consolas", 13, "bold"),
            text_color=color
        )
        value_label.pack(side="left", padx=(10, 0))

    def _create_description_panel(self,formula, r2_test, y_label):
        """
        Crea el panel de descripción del modelo.
        
        Parameters
        ----------
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
            fg_color=AppTheme.SECONDERY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        desc_container.pack(fill="both", expand=True)
        
        # Titulo del panel
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
            f"Formula del modelo:\n"
            f"{formula}\n"
            f"═══════════════════════════════════════════════════\n"
            f"Interpretación:\n"
            f"1. Coeficientes:"
            f"   Cada coeficiente indica el cambio promedio en '{y_label}' cuando\n"
            f"   su variable correspondiente aumenta en 1 unidad, manteniendo\n"
            f"   las demás variables constantes.\n\n"
            f"2. Capacidad Predectiva"
            f"   R² (test) = {r2_test:.4f} muestra la capacidad de generalización del modelo.\n"
            f"   El modelo explica el {r2_test*100:.1f}% de la variabilidad de '{y_label}'.\n"
            f"═══════════════════════════════════════════════════\n\n"
            f"Escribe aquí tus observaciones adicionales..."
        )
        self.desc_box.set(descripcion_inicial)

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

        # Construir fórmula con símbolos matemáticos
        coef_terms = [f"{coef:+.4f} * {col}" for coef, col in zip(model.coef_, X_train.columns)]
        intercept = model.intercept_

        formula = (
            f"{self.app.selection_panel.columna_salida} = "
            f"{' '.join(coef_terms)} {intercept:+.4f}"
        )

        # Mostrar resultados y métricas
        self._display_results(formula, r2_train, r2_test, mse_train, mse_test)

        # Si es representable gráficamente
        if X_train.shape[1] == 1:
            self._plot_graph(
                X_train, y_train, X_test, y_test, model, self.app.selection_panel.columna_salida
            )
        else:
            self.graph_frame.pack_forget()
            
            NotificationWindow(
                self.app,
                "Aviso",
                "No se puede representar el gráfico (más de una variable de entrada).",
                "info"
            )
        # =============================
        # PANEL DE DESCRIPCIÓN DEL MODELO
        # ============================= 

        # Crear panel de description en su propio frame
        self._create_description_panel(formula, r2_test, self.app.selection_panel.columna_salida)
        
        # Notification de exito
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
        # ═══════════════════════════════════════════════════════════
        # CONTENEDOR DEL GRAFICO CON EL TITULO
        # ═══════════════════════════════════════════════════════════
        # Frame principal con bordes
        graph_container = ctk.CTkFrame(
            self.graph_frame,
            fg_color=AppTheme.SECONDERY_BACKGROUND,
            corner_radius=8,
            border_width=1,
            border_color=AppTheme.BORDER
        )
        graph_container.pack(fill="both", expand=True)

        # Título del gráfico
        graph_title = ctk.CTkLabel(
            graph_container,
            text="Gráfica",
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

        # Frame interno para el graqfico
        plot_frame = ctk.CTkFrame(
            graph_container,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=6
        )
        plot_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Si hay muchos datos, muestrear para mejorar rendimiento
        # Esto reduce el número de puntos a dibujar sin perder la visualización general
        sample_size = 1000
        
        # Muestrear datos de entrenamiento
        if len(X_train) > sample_size:
            train_indices = np.random.choice(len(X_train), sample_size, replace=False)
            X_train_sample = X_train.iloc[train_indices]
            y_train_sample = y_train.iloc[train_indices]
        else:
            X_train_sample = X_train
            y_train_sample = y_train
        
        # Muestrear datos de test
        if len(X_test) > sample_size:
            test_indices = np.random.choice(len(X_test), sample_size, replace=False)
            X_test_sample = X_test.iloc[test_indices]
            y_test_sample = y_test.iloc[test_indices]
        else:
            X_test_sample = X_test
            y_test_sample = y_test

        # Crear figura y DPI optimizado para rendimiento
        fig, ax = plt.subplots(figsize=(10, 6), dpi=80)

        # Datos de entrenamiento
        ax.scatter(
            X_train_sample, 
            y_train_sample, 
            color="#2ea88c",
            label="Entrenamiento",
            s=40,
            alpha=0.7
        )
        
        # Datos de test
        ax.scatter(
            X_test_sample, 
            y_test_sample, 
            color="#dc5539",
            label="Test",
            s=40,
            alpha=0.7
        )

        # Recta de ajuste
        x_range = np.linspace(
            min(X_train.values.min(), X_test.values.min()),
            max(X_train.values.max(), X_test.values.max()),
            100
        )
        # Convertir a DataFrame con el mismo nombre de columna para evitar warnings
        x_range_df = pd.DataFrame(x_range, columns=X_train.columns)
        y_line = model.predict(x_range_df)
        
        ax.plot(
            x_range, 
            y_line, 
            color="red",
            label="Recta de ajuste",
            linewidth=2.5
        )

        # Etiquetas y estilo
        ax.set_xlabel(X_train.columns[0], fontsize=11)
        ax.set_ylabel(y_label, fontsize=11)
        ax.legend(loc='best', fontsize=10)
        ax.grid(True)
        
        # Ajustar layout para evitar recortes
        plt.tight_layout()

        # Limpiar canvas anterior si existe
        if self.current_canvas is not None:
            try:
                self.current_canvas.get_tk_widget().destroy()
            except:
                pass
        
        # Crear y almacenar el nuevo canvas
        self.current_canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.current_canvas.draw()
        
        # Obtener el widget de tkinter
        canvas_widget = self.current_canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Desactivar redibujado automático durante scroll
        canvas_widget.configure(takefocus=0)
        
        # IMPORTANTE: Cerrar la figura de matplotlib para liberar recursos
        plt.close(fig)