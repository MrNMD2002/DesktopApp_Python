import tkinter as tk
from tkinter import ttk, messagebox
from utils.auth import AuthManager
import logging

class UserManagementWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth_manager = auth_manager
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_users()
    
    def setup_window(self):
        """Thiết lập cửa sổ"""
        self.window.title("Quản lý Người dùng")
        self.window.geometry("900x600")
        self.window.resizable(True, True)
        
        # Căn giữa cửa sổ
        self.center_window()
        
        # Style
        style = ttk.Style()
        style.configure('Success.TButton', background='#28a745', foreground='white')
        style.configure('Danger.TButton', background='#dc3545', foreground='white')
        style.configure('Warning.TButton', background='#ffc107', foreground='black')
    
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
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="QUẢN LÝ NGƯỜI DÙNG", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame bên trái - Form thêm/sửa user
        form_frame = ttk.LabelFrame(main_frame, text="Thông tin người dùng", padding="10")
        form_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # Các trường nhập liệu
        ttk.Label(form_frame, text="Tên đăng nhập:").grid(row=0, column=0, sticky="w", pady=2)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(form_frame, textvariable=self.username_var, width=20)
        self.username_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(form_frame, text="Họ tên:").grid(row=1, column=0, sticky="w", pady=2)
        self.fullname_var = tk.StringVar()
        self.fullname_entry = ttk.Entry(form_frame, textvariable=self.fullname_var, width=20)
        self.fullname_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky="w", pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(form_frame, textvariable=self.email_var, width=20)
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(form_frame, text="Mật khẩu:").grid(row=3, column=0, sticky="w", pady=2)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(form_frame, textvariable=self.password_var, width=20, show="*")
        self.password_entry.grid(row=3, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(form_frame, text="Vai trò:").grid(row=4, column=0, sticky="w", pady=2)
        self.role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=17)
        role_combo.grid(row=4, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        ttk.Label(form_frame, text="Trạng thái:").grid(row=5, column=0, sticky="w", pady=2)
        self.status_var = tk.BooleanVar(value=True)
        status_check = ttk.Checkbutton(form_frame, text="Hoạt động", variable=self.status_var)
        status_check.grid(row=5, column=1, sticky="w", pady=2, padx=(5, 0))
        
        # Cấu hình grid cho form_frame
        form_frame.columnconfigure(1, weight=1)
        
        # Frame nút bấm
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        self.add_button = ttk.Button(button_frame, text="Thêm mới", 
                                    command=self.add_user, style="Success.TButton")
        self.add_button.grid(row=0, column=0, padx=(0, 5))
        
        self.update_button = ttk.Button(button_frame, text="Cập nhật", 
                                       command=self.update_user, style="Warning.TButton")
        self.update_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Xóa form", 
                                      command=self.clear_form)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        # Frame bên phải - Bảng danh sách users
        list_frame = ttk.LabelFrame(main_frame, text="Danh sách người dùng", padding="10")
        list_frame.grid(row=1, column=1, sticky="nsew")
        
        # Tạo Treeview
        columns = ("ID", "Username", "Full Name", "Email", "Role", "Status", "Created", "Last Login")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình cột
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Tên đăng nhập")
        self.tree.heading("Full Name", text="Họ tên")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Role", text="Vai trò")
        self.tree.heading("Status", text="Trạng thái")
        self.tree.heading("Created", text="Ngày tạo")
        self.tree.heading("Last Login", text="Đăng nhập cuối")
        
        # Độ rộng cột
        self.tree.column("ID", width=50)
        self.tree.column("Username", width=100)
        self.tree.column("Full Name", width=120)
        self.tree.column("Email", width=150)
        self.tree.column("Role", width=100)
        self.tree.column("Status", width=80)
        self.tree.column("Created", width=100)
        self.tree.column("Last Login", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Cấu hình grid cho list_frame
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Frame nút bấm cho danh sách
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.delete_button = ttk.Button(list_button_frame, text="Xóa", 
                                       command=self.delete_user, style="Danger.TButton")
        self.delete_button.grid(row=0, column=0, padx=(0, 5))
        
        self.toggle_button = ttk.Button(list_button_frame, text="Khóa/Mở khóa", 
                                       command=self.toggle_user_status)
        self.toggle_button.grid(row=0, column=1, padx=5)
        
        self.refresh_button = ttk.Button(list_button_frame, text="Làm mới", 
                                        command=self.load_users)
        self.refresh_button.grid(row=0, column=2, padx=5)
        
        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self.on_user_select)
        
        # Biến lưu user đang chọn
        self.selected_user_id = None
    
    def load_users(self):
        """Tải danh sách users"""
        try:
            # Xóa dữ liệu cũ
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Lấy danh sách users
            users = self.auth_manager.get_all_users()
            
            for user in users:
                # Format dữ liệu
                status = "Hoạt động" if user['is_active'] else "Đã khóa"
                created = user['created_at'].strftime('%d/%m/%Y') if user['created_at'] else ""
                last_login = user['last_login'].strftime('%d/%m/%Y %H:%M') if user['last_login'] else ""
                
                self.tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['full_name'],
                    user['email'] or "",
                    user['role'],
                    status,
                    created,
                    last_login
                ))
            
            logging.info(f"Đã tải {len(users)} users")
        except Exception as e:
            logging.error(f"Lỗi tải danh sách users: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {str(e)}")
    
    def clear_form(self):
        """Xóa form"""
        self.username_var.set("")
        self.fullname_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.role_var.set("student")
        self.status_var.set(True)
        self.selected_user_id = None
        
        # Cập nhật trạng thái nút
        self.add_button.config(state="normal")
        self.update_button.config(state="disabled")
    
    def on_user_select(self, event):
        """Xử lý khi chọn user trong bảng"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Lưu ID user đang chọn
            self.selected_user_id = values[0]
            
            # Điền thông tin vào form
            self.username_var.set(values[1])
            self.fullname_var.set(values[2])
            self.email_var.set(values[3] if values[3] else "")
            self.role_var.set(values[4])
            self.status_var.set(values[5] == "Hoạt động")
            self.password_var.set("")  # Không hiển thị mật khẩu
            
            # Cập nhật trạng thái nút
            self.add_button.config(state="disabled")
            self.update_button.config(state="normal")
    
    def add_user(self):
        """Thêm user mới"""
        try:
            # Lấy dữ liệu từ form
            username = self.username_var.get().strip()
            fullname = self.fullname_var.get().strip()
            email = self.email_var.get().strip()
            password = self.password_var.get()
            role = self.role_var.get()
            is_active = self.status_var.get()
            
            # Kiểm tra dữ liệu
            if not username or not fullname or not password:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin bắt buộc")
                return
            
            # Tạo user
            success, message = self.auth_manager.create_user(
                username, password, fullname, email, role
            )
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_users()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi thêm user: {e}")
            messagebox.showerror("Lỗi", f"Không thể thêm người dùng: {str(e)}")
    
    def update_user(self):
        """Cập nhật user"""
        if not self.selected_user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng cần cập nhật")
            return
        
        try:
            # Lấy dữ liệu từ form
            fullname = self.fullname_var.get().strip()
            email = self.email_var.get().strip()
            role = self.role_var.get()
            is_active = self.status_var.get()
            
            # Kiểm tra dữ liệu
            if not fullname:
                messagebox.showwarning("Cảnh báo", "Vui lòng điền họ tên")
                return
            
            # Cập nhật user
            success, message = self.auth_manager.update_user(
                self.selected_user_id, fullname, email, role, is_active
            )
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_users()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi cập nhật user: {e}")
            messagebox.showerror("Lỗi", f"Không thể cập nhật người dùng: {str(e)}")
    
    def delete_user(self):
        """Xóa user"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng cần xóa")
            return
        
        item = self.tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", 
                                     f"Bạn có chắc chắn muốn xóa người dùng '{username}'?")
        if not confirm:
            return
        
        try:
            success, message = self.auth_manager.delete_user(user_id)
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.clear_form()
                self.load_users()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi xóa user: {e}")
            messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {str(e)}")
    
    def toggle_user_status(self):
        """Khóa/mở khóa user"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng")
            return
        
        item = self.tree.item(selection[0])
        user_id = item['values'][0]
        username = item['values'][1]
        current_status = item['values'][5]
        
        action = "mở khóa" if current_status == "Đã khóa" else "khóa"
        confirm = messagebox.askyesno("Xác nhận", 
                                     f"Bạn có chắc chắn muốn {action} người dùng '{username}'?")
        if not confirm:
            return
        
        try:
            success, message = self.auth_manager.toggle_user_status(user_id)
            
            if success:
                messagebox.showinfo("Thành công", message)
                self.load_users()
            else:
                messagebox.showerror("Lỗi", message)
        except Exception as e:
            logging.error(f"Lỗi thay đổi trạng thái user: {e}")
            messagebox.showerror("Lỗi", f"Không thể thay đổi trạng thái: {str(e)}") 