import tkinter as tk
from tkinter import ttk, messagebox
import logging
from gui.login_window import LoginWindow
from gui.styles import ModernStyles
import bcrypt
from services.api_client import clear_cache

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ExamBankApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_user = None
        self.setup_main_window()
        self.show_welcome_screen()
    
    def setup_main_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("🎓 Hệ thống Quản lý Ngân hàng Đề thi Trắc nghiệm")
        self.root.geometry("1000x700")  # Tăng kích thước mặc định
        self.root.resizable(True, True)  # Cho phép resize cả chiều rộng và chiều cao
        self.root.minsize(800, 600)  # Kích thước tối thiểu
        
        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.root.configure(bg=ModernStyles.COLORS['light'])
        
        # Căn giữa cửa sổ
        self.center_window()
    
    def center_window(self):
        """Căn giữa cửa sổ trên màn hình"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_welcome_screen(self):
        """Hiển thị màn hình chào mừng"""
        # Main container
        main_frame = ModernStyles.create_modern_frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=60, pady=60)

        # Header section
        header_frame = ModernStyles.create_modern_frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 50))
        
        # Main title
        title_label = ModernStyles.create_title_label(header_frame,
                                                     "🎓 HỆ THỐNG QUẢN LÝ\n📚 NGÂN HÀNG ĐỀ THI TRẮC NGHIỆM")
        title_label.pack()
        
        # Subtitle
        subtitle_label = ModernStyles.create_subtitle_label(header_frame,
                                                           "Giải pháp toàn diện cho việc quản lý và tổ chức thi trắc nghiệm")
        subtitle_label.pack(pady=(10, 0))
        
        # Content section with 2 columns
        content_frame = ModernStyles.create_modern_frame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=(30, 0))
        
        # Left column - Features description
        left_frame = ModernStyles.create_modern_frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 30))
        
        # Features title
        desc_title = ModernStyles.create_subtitle_label(left_frame, "🚀 Tính năng chính")
        desc_title.pack(anchor="w", pady=(0, 20))
        
        # System features with icons
        features = [
            ("👨‍💼 Admin", "Quản lý người dùng, đề thi, toàn bộ hệ thống"),
            ("📝 Question Creator", "Upload file .docx chứa câu hỏi"),
            ("📊 Exam Generator", "Tạo đề thi từ ngân hàng câu hỏi"),
            ("👨‍🎓 Student", "Làm bài thi trực tuyến"),
            ("📈 Analytics", "Thống kê và báo cáo chi tiết"),
            ("🔒 Security", "Bảo mật thông tin và phân quyền")
        ]
        
        for icon_text, description in features:
            feature_frame = ModernStyles.create_modern_frame(left_frame)
            feature_frame.pack(fill="x", pady=8)
            
            icon_label = tk.Label(feature_frame, text=icon_text, 
                                 font=("Segoe UI", 12, "bold"), 
                                 fg=ModernStyles.COLORS['primary'],
                                 bg=ModernStyles.COLORS['light'])
            icon_label.pack(anchor="w")
            
            desc_label = ModernStyles.create_info_label(feature_frame, f"   {description}")
            desc_label.pack(anchor="w")
        
        # Right column - Login information
        right_frame = ModernStyles.create_modern_frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Sample accounts frame
        info_frame = ModernStyles.create_modern_frame(right_frame)
        info_frame.pack(fill="x", pady=(0, 25))
        
        info_title = ModernStyles.create_subtitle_label(info_frame, "🔑 Tài khoản mẫu")
        info_title.pack(anchor="w", pady=(0, 15))
        
        password_info = ModernStyles.create_info_label(info_frame, "Mật khẩu: 123456")
        password_info.pack(anchor="w", pady=(0, 15))
        
        accounts = [
            ("👨‍💼 admin", "Quản trị viên (Admin)"),
            ("📝 creator1", "Người làm đề (Question Creator)"),
            ("📊 generator1", "Người sinh đề (Exam Generator)"),
            ("👨‍🎓 student1", "Học sinh (Student)")
        ]
        
        for username, role in accounts:
            account_frame = ModernStyles.create_modern_frame(info_frame)
            account_frame.pack(fill="x", pady=5)
            
            user_label = tk.Label(account_frame, text=username, 
                                 font=("Segoe UI", 11, "bold"), 
                                 fg=ModernStyles.COLORS['dark'],
                                 bg=ModernStyles.COLORS['light'])
            user_label.pack(anchor="w")
            
            role_label = ModernStyles.create_info_label(account_frame, f"   {role}")
            role_label.pack(anchor="w")
        
        # Login button frame
        button_frame = ModernStyles.create_modern_frame(right_frame)
        button_frame.pack(fill="x")
        
        # Login button with modern styling
        login_button = ModernStyles.create_success_button(button_frame, 
                                                         "🔐 ĐĂNG NHẬP", 
                                                         self.show_login)
        login_button.pack(pady=(0, 20))
        
        # Version information
        version_frame = ModernStyles.create_modern_frame(button_frame)
        version_frame.pack()
        
        version_label = ModernStyles.create_info_label(version_frame, "📋 Phiên bản 2.0")
        version_label.pack(side="left", padx=(0, 15))
        
        copyright_label = ModernStyles.create_info_label(version_frame, "© 2024 ExamBank System")
        copyright_label.pack(side="left")
    
    def show_login(self):
        """Hiển thị cửa sổ đăng nhập"""
        LoginWindow(self)
    
    def show_main_window_after_login(self):
        from gui.student_window import StudentWindow
        from gui.question_creator_window import QuestionCreatorWindow
        from gui.exam_generator_window import ExamGeneratorWindow
        from gui.admin_window import AdminWindow
        
        role = self.current_user['role']
        
        # Ẩn cửa sổ chính (welcome screen)
        self.root.withdraw()
        
        # Debug: In ra role để kiểm tra
        print(f"User role: {role}")
        print(f"User data: {self.current_user}")
        
        # Mở cửa sổ tương ứng với role
        if role == "admin":
            # Admin có quyền quản lý toàn bộ hệ thống
            AdminWindow(self, None)
        elif role == "student":
            # Student chỉ có thể làm bài thi
            StudentWindow(self, None)
        elif role == "question_creator":
            # Question Creator chỉ có thể upload câu hỏi
            QuestionCreatorWindow(self, None)
        elif role == "exam_generator":
            # Exam Generator chỉ có thể tạo đề thi
            ExamGeneratorWindow(self, None)
        else:
            messagebox.showerror("Lỗi", f"Role không hợp lệ: {role}")
    
    def show_login_after_logout(self):
        """Hiển thị lại cửa sổ đăng nhập sau khi đăng xuất"""
        self.current_user = None
        self.root.deiconify()  # Hiển thị lại cửa sổ chính
        self.show_welcome_screen()  # Hiển thị lại welcome screen

    def run(self):
        """Chạy ứng dụng"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            logging.info("Ứng dụng được tắt bởi người dùng")
        except Exception as e:
            logging.error(f"Lỗi chạy ứng dụng: {e}")
            messagebox.showerror("Lỗi", f"Lỗi chạy ứng dụng: {str(e)}")

    def verify_password(self, password, hashed):
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

def main():
    """Hàm main"""
    try:
        app = ExamBankApp()
        app.run()
    except Exception as e:
        logging.error(f"Lỗi khởi tạo ứng dụng: {e}")
        messagebox.showerror("Lỗi", f"Không thể khởi động ứng dụng: {str(e)}")

if __name__ == "__main__":
    main() 