import tkinter as tk
from tkinter import ttk, messagebox
import logging
from gui.login_window import LoginWindow
import bcrypt

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
        self.setup_main_window()
        self.show_welcome_screen()
    
    def setup_main_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("Hệ thống Quản lý Ngân hàng Đề thi Trắc nghiệm")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Tùy chỉnh style cho nút
        style.configure('Accent.TButton', 
                       background='#0078d4', 
                       foreground='white',
                       font=('Arial', 10, 'bold'))
    
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
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Logo/Tiêu đề
        title_label = ttk.Label(main_frame, 
                               text="HỆ THỐNG QUẢN LÝ\nNGÂN HÀNG ĐỀ THI TRẮC NGHIỆM",
                               font=("Arial", 18, "bold"),
                               justify="center")
        title_label.grid(row=0, column=0, pady=(0, 30))
        
        # Mô tả hệ thống
        description = """
        Hệ thống hỗ trợ quản lý ngân hàng đề thi trắc nghiệm với các chức năng:
        
        • Người làm đề: Upload file .docx chứa câu hỏi
        • Người sinh đề: Tạo đề thi từ ngân hàng câu hỏi
        • Học sinh: Làm bài thi trực tuyến
        
        Vui lòng đăng nhập để sử dụng hệ thống.
        """
        
        desc_label = ttk.Label(main_frame, text=description, 
                              font=("Arial", 10), justify="left")
        desc_label.grid(row=1, column=0, pady=(0, 30))
        
        # Nút đăng nhập
        login_button = ttk.Button(main_frame, text="ĐĂNG NHẬP", 
                                 command=self.show_login, style="Accent.TButton")
        login_button.grid(row=2, column=0, pady=(0, 20))
        
        # Thông tin phiên bản
        version_label = ttk.Label(main_frame, text="Phiên bản 1.0", 
                                 font=("Arial", 8), foreground="gray")
        version_label.grid(row=3, column=0)
        
        # Thông tin tài khoản mẫu
        info_frame = ttk.LabelFrame(main_frame, text="Tài khoản mẫu", padding="10")
        info_frame.grid(row=4, column=0, pady=(20, 0), sticky="ew")
        
        info_text = """
        Tài khoản mẫu (mật khẩu: 123456):
        • student1 - Học sinh
        • creator1 - Người làm đề  
        • admin - Người sinh đề
        """
        
        info_label = ttk.Label(info_frame, text=info_text, 
                              font=("Arial", 9), justify="left")
        info_label.grid(row=0, column=0)
    
    def show_login(self):
        """Hiển thị cửa sổ đăng nhập"""
        LoginWindow(self.root)
    
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