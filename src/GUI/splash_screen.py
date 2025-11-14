"""
Pantalla de bienvenida (Splash Screen).

Este módulo implementa una splash screen que se muestra
al iniciar la aplicación. Incluye spinner de carga y
transición gradual al programa principal.
"""

import customtkinter as ctk
from .components import AppTheme


class SplashScreen(ctk.CTkToplevel):
    """
    Ventana de splash screen con animaciones profesionales.
    
    Caracteristicas:
    - Título 
    - Spinner circular animado
    - Barra de progreso con texto descriptivo
    """
    
    def __init__(self, parent):
        """
        Inicializa la splash screen.
        
        Parameters
        ----------
        parent : ctk.CTk
            Ventana principal de la aplicación
        """
        super().__init__(parent)
        
        self.parent = parent
        
        # Configuración de la ventana
        self.title("")
        self.geometry("700x500")
        self.resizable(False, False)
        
        # Quitar bordes de ventana
        self.overrideredirect(True)
        
        # Centrar en pantalla
        self._center_window()
        
        # Hacer que esté siempre al frente
        self.attributes("-topmost", True)
        
        # Variables de control
        self.animation_running = True
        self.spinner_angle = 0
        self.progress = 0
        
        # Crear interfaz
        self._create_ui()
        
        # Iniciar animaciones
        self._animate_spinner()
        self._simulate_loading()
    
    def _center_window(self):
        """Centrar la ventana en la pantalla."""
        self.update_idletasks()
        width = 700
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _create_ui(self):
        """Crear la interfaz de la splash screen."""
        
        # ═══════════════════════════════════════════════════════════
        # CONTENEDOR PRINCIPAL CON GRADIENTE
        # ═══════════════════════════════════════════════════════════
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=AppTheme.PRIMARY_BACKGROUND,
            corner_radius=20,
            border_width=2,
            border_color=AppTheme.PRIMARY_ACCENT
        )
        self.main_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # ═══════════════════════════════════════════════════════════
        # CONTENEDOR SUPERIOR: DECORACIÓN
        # ═══════════════════════════════════════════════════════════
        top_decoration = ctk.CTkFrame(
            self.main_frame,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            height=8,
            corner_radius=0
        )
        top_decoration.pack(fill="x", side="top")
        
        # ═══════════════════════════════════════════════════════════
        # SECCIÓN CENTRAL: CONTENIDO
        # ═══════════════════════════════════════════════════════════
        content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, pady=30)
        
        # ─────────────────────────────────────────────────────────
        # TITULO PRINCIPAL 
        # ─────────────────────────────────────────────────────────
        self.title_label = ctk.CTkLabel(
            content_frame,
            text="LUNEX DATASETS LOADER",
            font=("Orbitron", 38, "bold"),
            text_color=AppTheme.PRIMARY_TEXT
        )
        self.title_label.pack(pady=(50, 10))
        
        # ─────────────────────────────────────────────────────────
        # SUBTITULO
        # ─────────────────────────────────────────────────────────
        self.subtitle_label = ctk.CTkLabel(
            content_frame,
            text="Bienvenid@",
            font=("Segoe UI", 16),
            text_color=AppTheme.SECONDARY_TEXT
        )
        self.subtitle_label.pack(pady=(0, 40))
        
        # ─────────────────────────────────────────────────────────
        # SPINNER ANIMADO
        # ─────────────────────────────────────────────────────────
        self.spinner_canvas = ctk.CTkCanvas(
            content_frame,
            width=80,
            height=80,
            bg=AppTheme.PRIMARY_BACKGROUND,
            highlightthickness=0
        )
        self.spinner_canvas.pack(pady=20)
        
        # ─────────────────────────────────────────────────────────
        # BARRA DE PROGRESO
        # ─────────────────────────────────────────────────────────
        progress_container = ctk.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        progress_container.pack(pady=(20, 10), padx=100, fill="x")
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            mode="determinate",
            progress_color=AppTheme.PRIMARY_ACCENT,
            fg_color=AppTheme.TERTIARY_BACKGROUND,
            height=8,
            corner_radius=4
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        # ─────────────────────────────────────────────────────────
        # TEXTO DE ESTADO
        # ─────────────────────────────────────────────────────────
        self.status_label = ctk.CTkLabel(
            content_frame,
            text="Inicializando...",
            font=("Segoe UI", 13),
            text_color=AppTheme.DIM_TEXT
        )
        self.status_label.pack(pady=(10, 0))
        
        # ═══════════════════════════════════════════════════════════
        # PIE DE PAGINA: VERSION
        # ═══════════════════════════════════════════════════════════
        footer_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        footer_frame.pack(side="bottom", pady=(10, 25))
        
        version_label = ctk.CTkLabel(
            footer_frame,
            text="Version 1.0.0",
            font=("Segoe UI", 12),
            text_color=AppTheme.SECONDARY_TEXT
        )
        version_label.pack()
    
    def _animate_spinner(self):
        """
        Animar el spinner circular.
        
        Dibuja un arco rotatorio que simula un spinner de carga.
        """
        if not self.animation_running:
            return
        
        # Limpiar canvas
        self.spinner_canvas.delete("all")
        
        # Parámetros del spinner
        center_x = 40
        center_y = 40
        radius = 30
        thickness = 4
        
        # Dibujar circulo de fondo
        self.spinner_canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=AppTheme.TERTIARY_BACKGROUND,
            width=thickness
        )
        
        # Calcular angulos para el arco animado
        start_angle = self.spinner_angle
        extent = 120  # Longitud del arco
        
        # Dibujar arco principal 
        self.spinner_canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=start_angle,
            extent=extent,
            outline=AppTheme.PRIMARY_ACCENT,
            width=thickness,
            style="arc"
        )
        
        # Dibujar arco de "brillo" 
        self.spinner_canvas.create_arc(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            start=start_angle + extent - 30,
            extent=30,
            outline=AppTheme.LIGHT_ACCENT,
            width=thickness,
            style="arc"
        )
        
        # Incrementar angulo para rotación
        self.spinner_angle = (self.spinner_angle + 8) % 360
        
        # Continuar animación
        self.after(30, self._animate_spinner)
    
    def _simulate_loading(self):
        """
        Simular proceso de carga con barra de progreso.
        
        Simula diferentes etapas de inicialización del programa:
        - Cargando componentes
        - Inicializando interfaz
        - Preparando módulos
        - Finalizando
        """
        self.stages = [
            (0.2, "Cargando componentes..."),
            (0.4, "Inicializando interfaz..."),
            (0.6, "Preparando módulos de análisis..."),
            (0.8, "Configurando herramientas..."),
            (1.0, "Finalizando..."),
        ]
        
        self.current_stage = 0
        
        self.after(1200, self._update_loading_stage)
    
    def _update_loading_stage(self):
        """
        Actualizar la etapa actual de carga.
        
        Este método se llama recursivamente para avanzar por todas las etapas.
        """
        if self.current_stage >= len(self.stages):
            # Terminar animación y cerrar
            self._close_splash()
            return
        
        target_progress, status_text = self.stages[self.current_stage]
        self._animate_progress_to(target_progress, status_text)
        
        # Tiempo de espera antes de la siguiente etapa (en milisegundos)
        delay = 800 if self.current_stage < len(self.stages) - 1 else 600
        self.current_stage += 1
        self.after(delay, self._update_loading_stage)
    
    def _animate_progress_to(self, target, status_text):
        """
        Animar la barra de progreso hacia un valor objetivo.
        
        Parameters
        ----------
        target : float
            Valor objetivo de progreso (0.0 a 1.0)
        status_text : str
            Texto de estado a mostrar
        """
        # Actualizar texto de estado inmediatamente
        self.status_label.configure(text=status_text)
        
        # Guardar el objetivo para la animación
        self.progress_target = target
        
        # Iniciar animación de la barra
        self._animate_progress_step()
    
    def _animate_progress_step(self):
        """
        Un paso de la animación de progreso.
        
        Este método se llama recursivamente hasta alcanzar el objetivo.
        """
        if self.progress < self.progress_target:
            self.progress += 0.02
            self.progress_bar.set(min(self.progress, self.progress_target))
            self.after(20, self._animate_progress_step)
    
    def _close_splash(self):
        """
        Cerrar la splash screen con transición suave.
        
        Detiene las animaciones y cierra la ventana.
        """
        self.animation_running = False
        
        # Esperar un momento antes de cerrar
        self.after(200, self._destroy_and_show_main)
    
    def _destroy_and_show_main(self):
        """
        Destruir la splash screen y mostrar la ventana principal.
        """
        self.destroy()
        # Mostrar la ventana principal
        self.parent.deiconify()


def show_splash_screen(app):
    """
    Mostrar la splash screen antes de la aplicación principal.
    
    Esta función se llama desde main() antes de iniciar el mainloop.
    
    Parameters
    ----------
    app : DataLoaderApp
        Instancia de la aplicación principal
    
    Usage
    -----
    app = DataLoaderApp()
    app.withdraw() 
    show_splash_screen(app)
    app.mainloop()
    """
    splash = SplashScreen(app)
    return splash