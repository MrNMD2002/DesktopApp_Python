"""
Styles and themes for the Exam Bank GUI application
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class ModernStyles:
    """Modern styling for the application"""
    
    # Color palette
    COLORS = {
        'primary': '#2196F3',      # Blue
        'primary_dark': '#1976D2',  # Dark Blue
        'secondary': '#FF9800',     # Orange
        'success': '#4CAF50',       # Green
        'warning': '#FFC107',       # Yellow
        'danger': '#F44336',        # Red
        'info': '#00BCD4',          # Cyan
        'light': '#F5F5F5',         # Light Gray
        'dark': '#212121',          # Dark Gray
        'white': '#FFFFFF',         # White
        'black': '#000000',         # Black
        'gray': '#9E9E9E',          # Gray
        'border': '#E0E0E0',        # Border Gray
    }
    
    @staticmethod
    def apply_modern_style():
        """Apply modern styling to the application"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Configure fonts
        default_font = ('Segoe UI', 9)
        title_font = ('Segoe UI', 12, 'bold')
        button_font = ('Segoe UI', 9, 'bold')
        label_font = ('Segoe UI', 9)
        
        # Configure colors
        bg_color = ModernStyles.COLORS['light']
        fg_color = ModernStyles.COLORS['dark']
        accent_color = ModernStyles.COLORS['primary']
        
        # Configure common styles
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', 
                       background=bg_color, 
                       foreground=fg_color,
                       font=label_font)
        style.configure('TButton', 
                       background=accent_color,
                       foreground=ModernStyles.COLORS['white'],
                       font=button_font,
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 5))
        
        # Configure button states
        style.map('TButton',
                 background=[('active', ModernStyles.COLORS['primary_dark']),
                           ('pressed', ModernStyles.COLORS['primary_dark'])],
                 foreground=[('active', ModernStyles.COLORS['white']),
                           ('pressed', ModernStyles.COLORS['white'])])
        
        # Configure entry style
        style.configure('TEntry',
                       fieldbackground=ModernStyles.COLORS['white'],
                       borderwidth=1,
                       relief='solid',
                       padding=(5, 3))
        
        # Configure combobox style
        style.configure('TCombobox',
                       fieldbackground=ModernStyles.COLORS['white'],
                       background=ModernStyles.COLORS['white'],
                       borderwidth=1,
                       relief='solid',
                       padding=(5, 3))
        
        # Configure treeview style
        style.configure('Treeview',
                       background=ModernStyles.COLORS['white'],
                       foreground=fg_color,
                       fieldbackground=ModernStyles.COLORS['white'],
                       borderwidth=1,
                       relief='solid',
                       font=label_font)
        
        style.configure('Treeview.Heading',
                       background=accent_color,
                       foreground=ModernStyles.COLORS['white'],
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=0)
        
        # Configure notebook style
        style.configure('TNotebook',
                       background=bg_color,
                       borderwidth=0)
        
        style.configure('TNotebook.Tab',
                       background=ModernStyles.COLORS['white'],
                       foreground=fg_color,
                       padding=(15, 8),
                       font=label_font)
        
        style.map('TNotebook.Tab',
                 background=[('selected', accent_color),
                           ('active', ModernStyles.COLORS['primary_dark'])],
                 foreground=[('selected', ModernStyles.COLORS['white']),
                           ('active', ModernStyles.COLORS['white'])])
        
        # Configure separator style
        style.configure('TSeparator',
                       background=ModernStyles.COLORS['border'])
        
        # Configure scrollbar style
        style.configure('Vertical.TScrollbar',
                       background=ModernStyles.COLORS['gray'],
                       borderwidth=0,
                       arrowcolor=ModernStyles.COLORS['white'],
                       troughcolor=ModernStyles.COLORS['light'],
                       width=12)
        
        style.map('Vertical.TScrollbar',
                 background=[('active', ModernStyles.COLORS['primary']),
                           ('pressed', ModernStyles.COLORS['primary_dark'])])
    
    @staticmethod
    def create_modern_button(parent, text, command=None, **kwargs):
        """Create a modern styled button"""
        btn = ttk.Button(parent, text=text, command=command, **kwargs)
        return btn
    
    @staticmethod
    def create_modern_entry(parent, **kwargs):
        """Create a modern styled entry"""
        entry = ttk.Entry(parent, **kwargs)
        return entry
    
    @staticmethod
    def create_modern_label(parent, text, **kwargs):
        """Create a modern styled label"""
        label = ttk.Label(parent, text=text, **kwargs)
        return label
    
    @staticmethod
    def create_modern_frame(parent, **kwargs):
        """Create a modern styled frame"""
        frame = ttk.Frame(parent, **kwargs)
        return frame
    
    @staticmethod
    def create_modern_treeview(parent, **kwargs):
        """Create a modern styled treeview"""
        tree = ttk.Treeview(parent, **kwargs)
        return tree
    
    @staticmethod
    def create_modern_combobox(parent, **kwargs):
        """Create a modern styled combobox"""
        combo = ttk.Combobox(parent, **kwargs)
        return combo
    
    @staticmethod
    def create_modern_separator(parent, **kwargs):
        """Create a modern styled separator"""
        sep = ttk.Separator(parent, **kwargs)
        return sep
    
    @staticmethod
    def create_modern_scrollbar(parent, **kwargs):
        """Create a modern styled scrollbar"""
        scrollbar = ttk.Scrollbar(parent, **kwargs)
        return scrollbar
    
    @staticmethod
    def center_window(window, width=None, height=None):
        """Center a window on the screen"""
        window.update_idletasks()
        
        if width is None:
            width = window.winfo_width()
        if height is None:
            height = window.winfo_height()
        
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    @staticmethod
    def create_title_label(parent, text, **kwargs):
        """Create a title label with modern styling"""
        title_font = ('Segoe UI', 14, 'bold')
        title = tk.Label(parent, text=text, font=title_font, 
                        fg=ModernStyles.COLORS['primary'],
                        bg=ModernStyles.COLORS['light'],
                        **kwargs)
        return title
    
    @staticmethod
    def create_subtitle_label(parent, text, **kwargs):
        """Create a subtitle label with modern styling"""
        subtitle_font = ('Segoe UI', 11, 'bold')
        subtitle = tk.Label(parent, text=text, font=subtitle_font,
                           fg=ModernStyles.COLORS['dark'],
                           bg=ModernStyles.COLORS['light'],
                           **kwargs)
        return subtitle
    
    @staticmethod
    def create_info_label(parent, text, **kwargs):
        """Create an info label with modern styling"""
        info_font = ('Segoe UI', 9)
        info = tk.Label(parent, text=text, font=info_font,
                       fg=ModernStyles.COLORS['gray'],
                       bg=ModernStyles.COLORS['light'],
                       **kwargs)
        return info
    
    @staticmethod
    def create_success_button(parent, text, command=None, **kwargs):
        """Create a success styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=ModernStyles.COLORS['success'],
                       fg=ModernStyles.COLORS['white'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padx=15, pady=5,
                       cursor='hand2',
                       **kwargs)
        return btn
    
    @staticmethod
    def create_danger_button(parent, text, command=None, **kwargs):
        """Create a danger styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=ModernStyles.COLORS['danger'],
                       fg=ModernStyles.COLORS['white'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padx=15, pady=5,
                       cursor='hand2',
                       **kwargs)
        return btn
    
    @staticmethod
    def create_warning_button(parent, text, command=None, **kwargs):
        """Create a warning styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=ModernStyles.COLORS['warning'],
                       fg=ModernStyles.COLORS['dark'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padx=15, pady=5,
                       cursor='hand2',
                       **kwargs)
        return btn
    
    @staticmethod
    def create_info_button(parent, text, command=None, **kwargs):
        """Create an info styled button"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=ModernStyles.COLORS['info'],
                       fg=ModernStyles.COLORS['white'],
                       font=('Segoe UI', 9, 'bold'),
                       relief='flat',
                       borderwidth=0,
                       padx=15, pady=5,
                       cursor='hand2',
                       **kwargs)
        return btn 