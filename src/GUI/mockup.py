"""
Test visual completo que simula la aplicación final.
"""
import customtkinter as ctk
from gui_components import (
    AppTheme, AppConfig, Panel, UploadButton,
    NotificationWindow, LoadingIndicator
)

class MockupApp(ctk.CTk):
    """Mockup visual de la aplicación completa."""
    
    def __init__(self):
        super().__init__()
        
        self.title("MOCKUP - Sistema de Importación de Datos")
        self.geometry(f"{AppConfig.WINDOW_WIDTH}x{AppConfig.WINDOW_HEIGHT}")
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color = AppTheme.PRIMARY_BACKGROUND)
        
        self._create_mockup()
    
    def _create_mockup(self):
        """Crea mockup visual."""
        # Header
        header = ctk.CTkFrame(
            self,
            height = 100,
            corner_radius = 0,
            fg_color = AppTheme.SECONDERY_BACKGROUND
        )
        header.pack(fill = "x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text = "Sistema de Importación de Datos",
            font = AppConfig.TITLE_FONT,
            text_color = AppTheme.PRIMARY_TEXT
        ).pack(pady = (25, 5))
        
        ctk.CTkLabel(
            header,
            text = "Sprint 1 - Historia #14 | Visualización profesional",
            font = AppConfig.SMALL_FONT,
            text_color = AppTheme.SECONDARY_TEXT
        ).pack()
        
        # Panel de control
        control_panel = Panel(self, "Control de Carga")
        control_panel.pack(fill = "x", padx = 20, pady = (20, 10))
        
        btn_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=15)
        
        UploadButton(
            btn_frame,
            text = "CARGAR ARCHIVO",
            command = lambda: NotificationWindow(
                self,
                "Carga Exitosa",
                "Archivo cargado: datos.csv\n\n1,000 filas × 5 columnas",
                "success"
            )
        ).pack(side = "left", padx = (0, 15))
        
        path_frame = ctk.CTkFrame(
            btn_frame,
            fg_color = AppTheme.PRIMARY_BACKGROUND,
            corner_radius = 6,
            border_width = 1,
            border_color = AppTheme.BORDER
        )
        path_frame.pack(side = "left", fill = "x", expand = True)
        
        ctk.CTkLabel(
            path_frame,
            text="Ningún archivo seleccionado",
            font=AppConfig.BODY_FONT,
            text_color=AppTheme.DIM_TEXT
        ).pack(pady = 10, padx = 15)
        
        # Panel de datos
        data_panel = Panel(self, "Visualización de Datos")
        data_panel.pack(fill = "both", expand = True, padx = 20, pady = (0, 20))
        
        ctk.CTkLabel(
            data_panel,
            text = "Selecciona un archivo para visualizar los datos",
            font = ("Segoe UI", 13),
            text_color = AppTheme.DIM_TEXT
        ).pack(expand = True)

if __name__ == "__main__":
    app = MockupApp()
    app.mainloop()