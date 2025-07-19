import tkinter as tk
from tkinter import ttk, messagebox
from utils.auth import AuthManager
import logging
import secrets
import string

class ChangePasswordWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Đổi Mật Khẩu")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Style
        style = ttk.Style()
        style.configure('Success.TButton', background='#28a745', foreground='white')
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="ĐỔI MẬT KHẨU", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Thông tin user hiện tại
        current_user = self.auth_manager.get_current_user()
        if current_user:
            user_info = f"Người dùng: {current_user['full_name']} ({current_user['username']})"
            user_label = ttk.Label(main_frame, text=user_info, font=("Arial", 10))
            user_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Mật khẩu cũ
        ttk.Label(main_frame, text="Mật khẩu hiện tại:").grid(row=2, column=0, sticky="w", pady=5)
        self.old_password_var = tk.StringVar()
        self.old_password_entry = ttk.Entry(main_frame, textvariable=self.old_password_var, 
                                           show="*", width=25)
        self.old_password_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Mật khẩu mới
        ttk.Label(main_frame, text="Mật khẩu mới:").grid(row=3, column=0, sticky="w", pady=5)
        self.new_password_var = tk.StringVar()
        self.new_password_entry = ttk.Entry(main_frame, textvariable=self.new_password_var, 
                                           show="*", width=25)
        self.new_password_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Xác nhận mật khẩu mới
        ttk.Label(main_frame, text="Xác nhận mật khẩu:").grid(row=4, column=0, sticky="w", pady=5)
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(main_frame, textvariable=self.confirm_password_var, 
                                               show="*", width=25)
        self.confirm_password_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Lưu ý
        note_text = "Lưu ý: Mật khẩu phải có ít nhất 6 ký tự"
        note_label = ttk.Label(main_frame, text=note_text, font=("Arial", 9), foreground="gray")
        note_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Frame nút bấm
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        self.change_button = ttk.Button(button_frame, text="Đổi Mật Khẩu", 
                                       command=self.change_password, style="Success.TButton")
        self.change_button.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Hủy", 
                                       command=self.window.destroy)
        self.cancel_button.grid(row=0, column=1)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.change_password())
        self.window.bind('<Escape>', lambda e: self.window.destroy())
    
    def change_password(self):
        """Đổi mật khẩu"""
        try:
            # Lấy dữ liệu
            old_password = self.old_password_var.get()
            new_password = self.new_password_var.get()
            confirm_password = self.confirm_password_var.get()
            
            # Kiểm tra dữ liệu
            if not old_password or not new_password or not confirm_password:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
                return
            
            if len(new_password) < 6:
                messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
                return
            
            # Lấy user hiện tại
            current_user = self.auth_manager.get_current_user()
            if not current_user:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin người dùng")
                return
            
            # Đổi mật khẩu
            success, message = self.auth_manager.change_password(
                current_user['id'], old_password, new_password
            )
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.window.destroy()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi đổi mật khẩu: {e}")
            messagebox.showerror("Lỗi", f"Không thể đổi mật khẩu: {str(e)}")


class ForgotPasswordWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Quên Mật Khẩu")
        self.window.geometry("450x400")
        self.window.resizable(False, False)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Style
        style = ttk.Style()
        style.configure('Success.TButton', background='#28a745', foreground='white')
        style.configure('Info.TButton', background='#17a2b8', foreground='white')
    
    def center_window(self):
        """Căn giữa cửa sổ"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Tạo các widget"""
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="QUÊN MẬT KHẨU", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Mô tả
        desc_text = "Nhập tên đăng nhập để nhận token reset mật khẩu"
        desc_label = ttk.Label(main_frame, text=desc_text, font=("Arial", 10))
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Frame thông tin về token
        info_frame = ttk.LabelFrame(main_frame, text="ℹ️ Thông tin về Token", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        info_text = """
Token có định dạng: RESET-USERNAME-TIMESTAMP-RANDOM

Ví dụ: RESET-student1-20241201143022-ABC123

• Username: Tên đăng nhập của bạn
• Timestamp: Thời gian tạo (YYYYMMDDHHMMSS)
• Random: 6 ký tự ngẫu nhiên
• Hạn sử dụng: 1 giờ
        """
        
        info_label = ttk.Label(info_frame, text=info_text, justify="left", font=("Arial", 9))
        info_label.grid(row=0, column=0, sticky="w")
        
        # Username
        ttk.Label(main_frame, text="Tên đăng nhập:").grid(row=3, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=25)
        self.username_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Frame nút bấm
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        self.request_button = ttk.Button(button_frame, text="Tạo Token", 
                                        command=self.request_token, style="Success.TButton")
        self.request_button.grid(row=0, column=0, padx=(0, 10))
        
        self.demo_button = ttk.Button(button_frame, text="Tạo Demo Token", 
                                     command=self.create_demo_token, style="Info.TButton")
        self.demo_button.grid(row=0, column=1, padx=5)
        
        self.cancel_button = ttk.Button(button_frame, text="Hủy", 
                                       command=self.window.destroy)
        self.cancel_button.grid(row=0, column=2, padx=(10, 0))
        
        # Frame hiển thị token
        self.token_frame = ttk.LabelFrame(main_frame, text="🔑 Token Reset", padding="10")
        self.token_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # Token entry
        self.token_var = tk.StringVar()
        self.token_var.trace('w', self.on_token_change)
        self.token_entry = ttk.Entry(self.token_frame, textvariable=self.token_var, 
                                    width=50, font=("Courier", 10))
        self.token_entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Thông tin token
        self.token_info_label = ttk.Label(self.token_frame, text="", font=("Arial", 9))
        self.token_info_label.grid(row=1, column=0, sticky="w")
        
        # Frame reset mật khẩu
        self.reset_frame = ttk.LabelFrame(main_frame, text="🔄 Reset Mật Khẩu", padding="10")
        self.reset_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        # Mật khẩu mới
        ttk.Label(self.reset_frame, text="Mật khẩu mới:").grid(row=0, column=0, sticky="w", pady=5)
        self.new_password_var = tk.StringVar()
        self.new_password_entry = ttk.Entry(self.reset_frame, textvariable=self.new_password_var, 
                                           show="*", width=25)
        self.new_password_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Xác nhận mật khẩu
        ttk.Label(self.reset_frame, text="Xác nhận mật khẩu:").grid(row=1, column=0, sticky="w", pady=5)
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(self.reset_frame, textvariable=self.confirm_password_var, 
                                               show="*", width=25)
        self.confirm_password_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Nút reset
        self.reset_button = ttk.Button(self.reset_frame, text="Reset Mật Khẩu", 
                                      command=self.reset_password, style="Success.TButton")
        self.reset_button.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Cấu hình grid
        main_frame.columnconfigure(1, weight=1)
        self.token_frame.columnconfigure(0, weight=1)
        self.reset_frame.columnconfigure(1, weight=1)
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.request_token())
        self.window.bind('<Escape>', lambda e: self.window.destroy())
    
    def on_token_change(self, *args):
        """Xử lý khi token thay đổi"""
        token = self.token_var.get().strip()
        if token:
            self.show_token_info()
        else:
            self.token_info_label.config(text="")
    
    def show_token_info(self):
        """Hiển thị thông tin token"""
        token = self.token_var.get().strip()
        if not token:
            return
        
        token_info = self.auth_manager.decode_token_info(token)
        if token_info:
            info_text = f"""
Username: {token_info['username']}
Thời gian tạo: {token_info['timestamp']}
Trạng thái: {'✅ Hợp lệ' if token_info['is_valid'] else '❌ Không hợp lệ hoặc hết hạn'}
            """
        else:
            info_text = "❌ Token không đúng định dạng"
        
        self.token_info_label.config(text=info_text)
    
    def request_token(self):
        """Yêu cầu tạo token"""
        username = self.username_var.get().strip()
        
        if not username:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập")
            return
        
        try:
            success, result = self.auth_manager.generate_reset_token(username)
            
            if success:
                token = result
                self.token_var.set(token)
                messagebox.showinfo("Thành công", f"Token đã được tạo:\n\n{token}\n\nToken có hiệu lực trong 1 giờ.")
            else:
                messagebox.showerror("Lỗi", result)
                
        except Exception as e:
            logging.error(f"Lỗi tạo token: {e}")
            messagebox.showerror("Lỗi", f"Không thể tạo token: {str(e)}")
    
    def create_demo_token(self):
        """Tạo token demo"""
        demo_tokens = [
            "RESET-student1-20241201143022-ABC123",
            "RESET-creator1-20241201143500-DEF456",
            "RESET-admin-20241201144015-GHI789"
        ]
        
        import random
        demo_token = random.choice(demo_tokens)
        self.token_var.set(demo_token)
        
        messagebox.showinfo("Demo Token", f"Đã tạo token demo:\n\n{demo_token}\n\nToken này chỉ để demo, không có hiệu lực thật.")
    
    def reset_password(self):
        """Reset mật khẩu bằng token"""
        token = self.token_var.get().strip()
        new_password = self.new_password_var.get()
        confirm_password = self.confirm_password_var.get()
        
        if not token:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập token")
            return
        
        if not new_password or not confirm_password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập mật khẩu mới")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 6 ký tự")
            return
        
        try:
            success, message = self.auth_manager.reset_password_with_token(token, new_password)
            
            if success:
                messagebox.showinfo("Thành công", message)
                # Xóa form
                self.token_var.set("")
                self.new_password_var.set("")
                self.confirm_password_var.set("")
            else:
                messagebox.showerror("Lỗi", message)
                
        except Exception as e:
            logging.error(f"Lỗi reset mật khẩu: {e}")
            messagebox.showerror("Lỗi", f"Không thể reset mật khẩu: {str(e)}") 