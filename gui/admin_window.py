import tkinter as tk
from tkinter import ttk, messagebox
from services import user_service
from gui.exam_generator_window import ExamGeneratorWindow
from gui.question_creator_window import QuestionCreatorWindow
from gui.styles import ModernStyles

def find_exambank_app_and_logout(parent):
    """Helper function để tìm ExamBankApp và gọi show_login_after_logout"""
    current_parent = parent
    while hasattr(current_parent, 'parent'):
        current_parent = current_parent.parent
        if hasattr(current_parent, 'show_login_after_logout'):
            current_parent.show_login_after_logout()
            return True
    # Nếu không tìm thấy, thử gọi trực tiếp
    if hasattr(parent, 'show_login_after_logout'):
        parent.show_login_after_logout()
        return True
    return False

class AdminWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.current_user = self.parent.current_user
        self.window = tk.Toplevel(self.parent.root)
        self.window.title("👨‍💼 Trang chủ Quản trị viên - Hệ thống Quản lý Đề thi")
        self.window.geometry("800x600")
        
        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.window.configure(bg=ModernStyles.COLORS['light'])
        
        # Center window
        ModernStyles.center_window(self.window, 800, 600)
        
        # Ẩn cửa sổ đăng nhập
        self.parent.root.withdraw()
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ModernStyles.create_modern_frame(self.window)
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Header section
        header_frame = ModernStyles.create_modern_frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Avatar and admin info
        admin_info_frame = ModernStyles.create_modern_frame(header_frame)
        admin_info_frame.pack()
        
        # Avatar icon
        avatar_label = tk.Label(admin_info_frame, text="👨‍💼", 
                               font=("Segoe UI", 64), 
                               fg=ModernStyles.COLORS['primary'],
                               bg=ModernStyles.COLORS['light'])
        avatar_label.pack(pady=(0, 15))
        
        # Admin name
        name_label = ModernStyles.create_title_label(admin_info_frame, 
                                                    f"Xin chào, {self.current_user['full_name']}")
        name_label.pack()
        
        # Subtitle
        subtitle_label = ModernStyles.create_subtitle_label(admin_info_frame, 
                                                           "🎛️ Bảng điều khiển quản trị hệ thống")
        subtitle_label.pack(pady=(5, 0))
        
        # Function buttons section
        button_frame = ModernStyles.create_modern_frame(main_frame)
        button_frame.pack(expand=True, pady=(0, 30))
        
        # Main function buttons with modern styling
        buttons = [
            ("👥 Quản lý người dùng", "Thêm, sửa, xóa người dùng", self.open_user_management),
            ("📊 Quản lý đề thi", "Tạo và quản lý đề thi", self.open_exam_management),
            ("📝 Quản lý câu hỏi", "Upload và quản lý câu hỏi", self.open_question_management),
            ("📚 Quản lý môn học", "Thêm, sửa, xóa môn học", self.open_subject_management)
        ]
        
        # Create button grid
        button_grid = ModernStyles.create_modern_frame(button_frame)
        button_grid.pack(expand=True)
        
        for i, (text, description, command) in enumerate(buttons):
            # Button container
            btn_container = ModernStyles.create_modern_frame(button_grid)
            btn_container.grid(row=i, column=0, pady=15, padx=20, sticky="ew")
            
            # Main button with modern styling
            btn = ModernStyles.create_info_button(btn_container, text, command)
            btn.pack(pady=(0, 8))
            
            # Description
            desc_label = ModernStyles.create_info_label(btn_container, description)
            desc_label.pack()
        
        # Footer section
        footer_frame = ModernStyles.create_modern_frame(main_frame)
        footer_frame.pack(side="bottom", fill="x", pady=(30, 0))
        
        # System info
        system_info = ModernStyles.create_info_label(footer_frame, 
                                                    "🖥️ Hệ thống đang hoạt động bình thường")
        system_info.pack(side="left")
        
        # Logout button
        logout_btn = ModernStyles.create_danger_button(footer_frame, 
                                                      "🚪 Đăng xuất", 
                                                      self.logout)
        logout_btn.pack(side="right")
    
    def open_user_management(self):
        # Ẩn cửa sổ hiện tại trước khi mở cửa sổ mới
        self.window.withdraw()
        UserManagementWindow(self)
    
    def open_exam_management(self):
        # Ẩn cửa sổ hiện tại trước khi mở cửa sổ mới
        self.window.withdraw()
        ExamGeneratorWindow(self, None)
    
    def open_question_management(self):
        # Ẩn cửa sổ hiện tại trước khi mở cửa sổ mới
        self.window.withdraw()
        QuestionCreatorWindow(self, None)
    
    def open_subject_management(self):
        # Ẩn cửa sổ hiện tại trước khi mở cửa sổ mới
        self.window.withdraw()
        SubjectManagementWindow(self)
    
    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        # Hiển thị lại cửa sổ admin và đóng cửa sổ hiện tại
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()  # Hiển thị lại cửa sổ admin
        self.window.destroy()
    
    def logout(self):
        """Đăng xuất và quay về cửa sổ đăng nhập"""
        self.window.destroy()
        # Kiểm tra parent type để xử lý logout đúng cách
        if hasattr(self.parent, 'show_login_after_logout'):
            # Nếu parent là ExamBankApp
            self.parent.show_login_after_logout()
        else:
            # Nếu parent là window khác, tìm ExamBankApp
            current_parent = self.parent
            while hasattr(current_parent, 'parent'):
                current_parent = current_parent.parent
                if hasattr(current_parent, 'show_login_after_logout'):
                    current_parent.show_login_after_logout()
                    break
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!")

# Tách phần quản lý người dùng thành class riêng
class UserManagementWindow:
    def __init__(self, parent):
        self.parent = parent  # parent phải có current_user
        self.window = tk.Toplevel(parent.window if hasattr(parent, 'window') else parent)
        self.window.title("👥 Quản lý người dùng - Hệ thống Quản lý Đề thi")
        self.window.geometry("1200x800")
        
        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.window.configure(bg=ModernStyles.COLORS['light'])
        
        # Center window
        ModernStyles.center_window(self.window, 1200, 800)
        
        self.setup_ui()
        self.load_users()
        
        # Thêm event handler để đảm bảo parent window được hiển thị khi đóng window này
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Thiết lập giao diện admin"""
        self.window.title("👥 Quản lý người dùng - Hệ thống Quản lý Đề thi")
        self.window.geometry("1200x800")
        
        # Tạo style cho user management
        style = ttk.Style()
        style.configure('UserMgmt.TFrame', background='#f8f9fa')
        style.configure('UserMgmtHeader.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground='#2c3e50',
                       background='#f8f9fa')
        # Style cho các nút khác nhau
        style.configure('AddButton.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8),
                       background='#27ae60',
                       foreground='white',
                       borderwidth=2,
                       relief='raised')
        style.map('AddButton.TButton',
                 background=[('active', '#229954'), ('pressed', '#1e8449')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        style.configure('EditButton.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8),
                       background='#3498db',
                       foreground='white',
                       borderwidth=2,
                       relief='raised')
        style.map('EditButton.TButton',
                 background=[('active', '#2980b9'), ('pressed', '#21618c')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        style.configure('PasswordButton.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8),
                       background='#f39c12',
                       foreground='white',
                       borderwidth=2,
                       relief='raised')
        style.map('PasswordButton.TButton',
                 background=[('active', '#e67e22'), ('pressed', '#d35400')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        style.configure('DeleteButton.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8),
                       background='#e74c3c',
                       foreground='white',
                       borderwidth=2,
                       relief='raised')
        style.map('DeleteButton.TButton',
                 background=[('active', '#c0392b'), ('pressed', '#a93226')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        style.configure('RefreshButton.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(15, 8),
                       background='#9b59b6',
                       foreground='white',
                       borderwidth=2,
                       relief='raised')
        style.map('RefreshButton.TButton',
                 background=[('active', '#8e44ad'), ('pressed', '#7d3c98')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="20", style='UserMgmt.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header với gradient background
        header_frame = ttk.Frame(main_frame, style='UserMgmt.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Thông tin admin
        user_info = self.parent.current_user
        admin_info_frame = ttk.Frame(header_frame, style='UserMgmt.TFrame')
        admin_info_frame.pack(side=tk.LEFT)
        
        # Icon và tên admin
        admin_icon = ttk.Label(admin_info_frame, text="👥", 
                              font=("Arial", 24), background='#f8f9fa')
        admin_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        admin_text_frame = ttk.Frame(admin_info_frame, style='UserMgmt.TFrame')
        admin_text_frame.pack(side=tk.LEFT)
        
        ttk.Label(admin_text_frame, text="Quản lý người dùng", 
                 style="UserMgmtHeader.TLabel").pack(anchor="w")
        
        ttk.Label(admin_text_frame, text=f"Admin: {user_info['full_name']}", 
                 font=("Arial", 12), foreground="#7f8c8d",
                 background='#f8f9fa').pack(anchor="w")
        
        # Nút quay lại và đăng xuất
        button_frame = ttk.Frame(header_frame, style='UserMgmt.TFrame')
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="⬅️ Quay lại", 
                  command=self.back_to_admin, style="EditButton.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="🚪 Đăng xuất", 
                  command=self.logout, style="DeleteButton.TButton").pack(side=tk.RIGHT)
        
        # Frame quản lý người dùng với style đẹp
        users_frame = ttk.LabelFrame(main_frame, text="📋 Danh sách người dùng", 
                                    padding="15", style='UserMgmt.TFrame')
        users_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Treeview cho danh sách người dùng với style
        columns = ("ID", "Tên đăng nhập", "Họ tên", "Vai trò", "Ngày tạo")
        self.users_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=18)
        
        # Cấu hình style cho treeview
        style.configure("Treeview", 
                       background="#ffffff",
                       foreground="#2c3e50",
                       rowheight=30,
                       fieldbackground="#ffffff")
        style.configure("Treeview.Heading", 
                       font=('Arial', 10, 'bold'),
                       background="#3498db",
                       foreground="white")
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=180, anchor="center")
        
        self.users_tree.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Scrollbar với style
        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=self.users_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame nút chức năng với layout đẹp
        button_frame = ttk.Frame(users_frame, style='UserMgmt.TFrame')
        button_frame.grid(row=1, column=0, columnspan=2, pady=15)
        
        # Nút bên trái
        left_buttons = ttk.Frame(button_frame, style='UserMgmt.TFrame')
        left_buttons.pack(side=tk.LEFT)
        
        ttk.Button(left_buttons, text="➕ Thêm người dùng", 
                  command=self.add_user, style="AddButton.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(left_buttons, text="✏️ Sửa người dùng", 
                  command=self.edit_user, style="EditButton.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(left_buttons, text="🔐 Đổi mật khẩu", 
                  command=self.change_password, style="PasswordButton.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(left_buttons, text="🗑️ Xóa người dùng", 
                  command=self.delete_user, style="DeleteButton.TButton").pack(side=tk.LEFT, padx=(0, 10))
        
        # Không có nút refresh
        
        # Thống kê người dùng
        stats_frame = ttk.Frame(users_frame, style='UserMgmt.TFrame')
        stats_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        stats_label = ttk.Label(stats_frame, text="📊 Tổng số người dùng: 0", 
                               font=("Arial", 11), foreground="#27ae60",
                               background='#f8f9fa')
        stats_label.pack(side=tk.LEFT)
        self.stats_label = stats_label
        
        # Cấu hình grid
        users_frame.columnconfigure(0, weight=1)
        users_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.users_tree.bind("<Double-1>", lambda e: self.edit_user())
    
    def load_users(self):
        """Tải danh sách người dùng"""
        try:
            users = user_service.get_users()
            
            # Xóa dữ liệu cũ
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Thêm dữ liệu mới
            for user in users:
                created_at = user.get('created_at')
                if isinstance(created_at, str):
                    try:
                        import datetime
                        created_date = datetime.datetime.fromisoformat(created_at).strftime('%d/%m/%Y %H:%M')
                    except Exception:
                        created_date = created_at
                else:
                    created_date = created_at.strftime('%d/%m/%Y %H:%M')
                
                role_display = {
                    'student': 'Học sinh',
                    'question_creator': 'Người làm đề',
                    'exam_generator': 'Người sinh đề',
                    'admin': 'Quản trị viên'
                }.get(user['role'], user['role'])
                
                self.users_tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['full_name'],
                    role_display,
                    created_date
                ), tags=(user['id'],))
            
            # Cập nhật thống kê
            if hasattr(self, 'stats_label'):
                self.stats_label.config(text=f"📊 Tổng số người dùng: {len(users)}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách người dùng: {str(e)}")
    
    def get_selected_user_id(self):
        """Lấy ID người dùng được chọn"""
        selection = self.users_tree.selection()
        if not selection:
            return None
        item = self.users_tree.item(selection[0])
        return item['tags'][0]
    
    def add_user(self):
        """Thêm người dùng mới"""
        dialog = tk.Toplevel(self.window)
        dialog.title("➕ Thêm người dùng mới")
        dialog.geometry("500x450")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Căn giữa dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f"500x450+{x}+{y}")
        
        # Style cho dialog
        style = ttk.Style()
        style.configure('Dialog.TFrame', background='#f8f9fa')
        style.configure('DialogHeader.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground='#2c3e50',
                       background='#f8f9fa')
        
        frame = ttk.Frame(dialog, padding="25", style='Dialog.TFrame')
        frame.pack(fill="both", expand=True)
        
        # Header với icon
        header_frame = ttk.Frame(frame, style='Dialog.TFrame')
        header_frame.pack(fill="x", pady=(0, 25))
        
        icon_label = ttk.Label(header_frame, text="➕", 
                              font=("Arial", 24), background='#f8f9fa')
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        header_label = ttk.Label(header_frame, text="Thêm người dùng mới", 
                                style="DialogHeader.TLabel")
        header_label.pack(side=tk.LEFT)
        
        # Form fields với layout đẹp
        form_frame = ttk.Frame(frame, style='Dialog.TFrame')
        form_frame.pack(fill="x", pady=(0, 25))
        
        # Tên đăng nhập
        username_frame = ttk.Frame(form_frame, style='Dialog.TFrame')
        username_frame.pack(fill="x", pady=8)
        
        ttk.Label(username_frame, text="👤 Tên đăng nhập:", 
                 font=("Arial", 11, "bold"), background='#f8f9fa').pack(anchor="w")
        username_var = tk.StringVar()
        username_entry = ttk.Entry(username_frame, textvariable=username_var, 
                                  width=50, font=("Arial", 11))
        username_entry.pack(fill="x", pady=(5, 0))
        
        # Mật khẩu
        password_frame = ttk.Frame(form_frame, style='Dialog.TFrame')
        password_frame.pack(fill="x", pady=8)
        
        ttk.Label(password_frame, text="🔐 Mật khẩu:", 
                 font=("Arial", 11, "bold"), background='#f8f9fa').pack(anchor="w")
        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=password_var, 
                                  show="*", width=50, font=("Arial", 11))
        password_entry.pack(fill="x", pady=(5, 0))
        
        # Họ tên
        fullname_frame = ttk.Frame(form_frame, style='Dialog.TFrame')
        fullname_frame.pack(fill="x", pady=8)
        
        ttk.Label(fullname_frame, text="📝 Họ tên:", 
                 font=("Arial", 11, "bold"), background='#f8f9fa').pack(anchor="w")
        fullname_var = tk.StringVar()
        fullname_entry = ttk.Entry(fullname_frame, textvariable=fullname_var, 
                                  width=50, font=("Arial", 11))
        fullname_entry.pack(fill="x", pady=(5, 0))
        
        # Vai trò
        role_frame = ttk.Frame(form_frame, style='Dialog.TFrame')
        role_frame.pack(fill="x", pady=8)
        
        ttk.Label(role_frame, text="🎭 Vai trò:", 
                 font=("Arial", 11, "bold"), background='#f8f9fa').pack(anchor="w")
        role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(role_frame, textvariable=role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=47, font=("Arial", 11))
        role_combo.pack(fill="x", pady=(5, 0))
        
        def validate_form():
            username = username_var.get().strip()
            password = password_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            if not username:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập tên đăng nhập!")
                username_entry.focus()
                return False
            
            if not password:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập mật khẩu!")
                password_entry.focus()
                return False
            
            if len(password) < 6:
                messagebox.showwarning("Cảnh báo", "⚠️ Mật khẩu phải có ít nhất 6 ký tự!")
                password_entry.focus()
                return False
            
            if not fullname:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập họ tên!")
                fullname_entry.focus()
                return False
            
            if not role:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng chọn vai trò!")
                role_combo.focus()
                return False
            
            return True
        
        def save():
            if not validate_form():
                return
            
            username = username_var.get().strip()
            password = password_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            # Xác nhận cuối cùng
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có chắc chắn muốn thêm người dùng mới?\n\n"
                                       f"📋 Thông tin người dùng:\n"
                                       f"• Tên đăng nhập: {username}\n"
                                       f"• Họ tên: {fullname}\n"
                                       f"• Vai trò: {role}")
            
            if not result:
                return
            
            try:
                from services.api_client import clear_cache
                
                # Xóa cache trước khi tạo user mới
                clear_cache()
                
                user_service.create_user(username, password, fullname, role)
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã thêm người dùng mới thành công!\n\n"
                                  f"📋 Thông tin:\n"
                                  f"• Tên đăng nhập: {username}\n"
                                  f"• Họ tên: {fullname}\n"
                                  f"• Vai trò: {role}")
                dialog.destroy()
                
                # Xóa cache và load lại danh sách ngay lập tức
                clear_cache()
                self.window.after(100, self.load_users)
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể thêm người dùng:\n{str(e)}")
        
        def cancel():
            dialog.destroy()
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons
        ttk.Button(button_frame, text="❌ Hủy", command=cancel, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✅ Xác nhận thêm người dùng", command=save, 
                  style='Accent.TButton', width=25).pack(side=tk.RIGHT)
        
        # Focus vào username entry
        username_entry.focus()
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: save())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def edit_user(self):
        """Sửa thông tin người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để sửa!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Sửa thông tin người dùng")
        dialog.geometry("500x400")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.resizable(False, False)  # Không cho phép thay đổi kích thước
        
        # Căn giữa dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Main container frame
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form frame
        frame = ttk.Frame(main_frame)
        frame.pack(fill="both", expand=True)
        
        # Form fields với layout cải thiện
        # Cấu hình grid
        frame.columnconfigure(1, weight=1)
        
        ttk.Label(frame, text="Tên đăng nhập:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))
        username_var = tk.StringVar(value=user['username'])
        username_entry = ttk.Entry(frame, textvariable=username_var, width=35, font=("Arial", 10))
        username_entry.grid(row=0, column=1, sticky="ew", pady=8)
        
        ttk.Label(frame, text="Họ tên:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
        fullname_var = tk.StringVar(value=user['full_name'])
        fullname_entry = ttk.Entry(frame, textvariable=fullname_var, width=35, font=("Arial", 10))
        fullname_entry.grid(row=1, column=1, sticky="ew", pady=8)
        
        ttk.Label(frame, text="Vai trò:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))
        role_var = tk.StringVar(value=user['role'])
        role_combo = ttk.Combobox(frame, textvariable=role_var, 
                                 values=["student", "question_creator", "exam_generator", "admin"],
                                 state="readonly", width=32, font=("Arial", 10))
        role_combo.grid(row=2, column=1, sticky="ew", pady=8)
        
        def validate_form():
            username = username_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            if not username:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập tên đăng nhập!")
                return False
            
            if not fullname:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập họ tên!")
                return False
            
            if not role:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng chọn vai trò!")
                return False
            
            return True
        
        def save():
            if not validate_form():
                return
            
            username = username_var.get().strip()
            fullname = fullname_var.get().strip()
            role = role_var.get()
            
            # Xác nhận cuối cùng
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có chắc chắn muốn cập nhật thông tin người dùng?\n\n"
                                       f"📋 Thông tin mới:\n"
                                       f"• Tên đăng nhập: {username}\n"
                                       f"• Họ tên: {fullname}\n"
                                       f"• Vai trò: {role}")
            
            if not result:
                return
            
            try:
                from services.api_client import clear_cache
                
                # Xóa cache trước khi cập nhật user
                clear_cache()
                
                user_service.update_user(user_id, {
                    "username": username,
                    "full_name": fullname,
                    "role": role
                })
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã cập nhật thông tin người dùng thành công!\n\n"
                                  f"📋 Thông tin mới:\n"
                                  f"• Tên đăng nhập: {username}\n"
                                  f"• Họ tên: {fullname}\n"
                                  f"• Vai trò: {role}")
                dialog.destroy()
                
                # Xóa cache và load lại danh sách ngay lập tức
                clear_cache()
                self.window.after(100, self.load_users)
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể cập nhật:\n{str(e)}")
        
        def cancel():
            dialog.destroy()
        
        # Thêm separator để phân tách
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=(20, 0))
        
        # Button frame riêng biệt
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Buttons với kích thước lớn hơn và rõ ràng
        cancel_btn = ttk.Button(button_frame, text="❌ Hủy", command=cancel, 
                               width=20, style='Danger.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        save_btn = ttk.Button(button_frame, text="✅ Lưu thay đổi", command=save, 
                             width=22, style='Accent.TButton')
        save_btn.pack(side=tk.RIGHT)
        
        # Focus vào entry đầu tiên
        username_entry.focus()
    
    def change_password(self):
        """Đổi mật khẩu người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để đổi mật khẩu!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Đổi mật khẩu - {user['username']}")
        dialog.geometry("550x400")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.resizable(False, False)  # Không cho phép thay đổi kích thước
        
        # Căn giữa dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"550x400+{x}+{y}")
        
        # Main container frame
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        frame = ttk.Frame(main_frame)
        frame.pack(fill="both", expand=True)
        
        # Header
        header_label = ttk.Label(frame, text=f"🔐 Đổi mật khẩu", font=("Arial", 16, "bold"))
        header_label.pack(pady=(0, 10))
        
        user_label = ttk.Label(frame, text=f"Người dùng: {user['full_name']} ({user['username']})", 
                              font=("Arial", 12))
        user_label.pack(pady=(0, 30))
        
        # Form fields
        form_frame = ttk.Frame(frame)
        form_frame.pack(fill="x", pady=(0, 30))
        
        ttk.Label(form_frame, text="Mật khẩu mới:", font=("Arial", 12, "bold")).pack(anchor="w")
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, show="*", width=50, font=("Arial", 12))
        password_entry.pack(pady=(8, 20), fill="x")
        
        ttk.Label(form_frame, text="Xác nhận mật khẩu:", font=("Arial", 12, "bold")).pack(anchor="w")
        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(form_frame, textvariable=confirm_var, show="*", width=50, font=("Arial", 12))
        confirm_entry.pack(pady=(8, 20), fill="x")
        
        # Validation function
        def validate_password():
            password = password_var.get().strip()
            confirm = confirm_var.get().strip()
            
            if not password:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập mật khẩu mới!")
                password_entry.focus()
                return False
            
            if len(password) < 6:
                messagebox.showwarning("Cảnh báo", "⚠️ Mật khẩu phải có ít nhất 6 ký tự!")
                password_entry.focus()
                return False
            
            if password != confirm:
                messagebox.showwarning("Cảnh báo", "⚠️ Mật khẩu xác nhận không khớp!")
                confirm_entry.focus()
                return False
            
            return True
        
        def save():
            if not validate_password():
                return
            
            password = password_var.get().strip()
            
            # Xác nhận cuối cùng
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có chắc chắn muốn đổi mật khẩu cho người dùng:\n"
                                       f"• {user['full_name']}\n"
                                       f"• {user['username']}\n\n"
                                       f"⚠️ Mật khẩu mới sẽ có hiệu lực ngay lập tức!")
            
            if not result:
                return
            
            try:
                user_service.change_password(user_id, password)
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã đổi mật khẩu thành công cho người dùng:\n"
                                  f"• {user['full_name']}\n"
                                  f"• {user['username']}")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể đổi mật khẩu:\n{str(e)}")
        
        def cancel():
            dialog.destroy()
        
        # Thêm separator để phân tách
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=(20, 0))
        
        # Button frame riêng biệt
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(15, 0))
        
        # Buttons với kích thước lớn hơn và rõ ràng
        cancel_btn = ttk.Button(button_frame, text="❌ Hủy", command=cancel, 
                               width=20, style='Danger.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        save_btn = ttk.Button(button_frame, text="✅ Xác nhận đổi mật khẩu", command=save, 
                             width=28, style='Accent.TButton')
        save_btn.pack(side=tk.RIGHT)
        
        # Focus vào password entry
        password_entry.focus()
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: save())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def delete_user(self):
        """Xóa người dùng"""
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn người dùng để xóa!")
            return
        
        try:
            user = user_service.get_user(user_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin người dùng: {str(e)}")
            return
        
        result = messagebox.askyesno("Xác nhận", 
                                   f"Bạn có chắc chắn muốn xóa người dùng {user['full_name']}?\n"
                                   f"Tên đăng nhập: {user['username']}")
        
        if result:
            try:
                from services.api_client import clear_cache
                
                # Xóa cache trước khi xóa user
                clear_cache()
                
                user_service.delete_user(user_id)
                messagebox.showinfo("Thành công", "Đã xóa người dùng!")
                
                # Xóa cache và load lại danh sách ngay lập tức
                clear_cache()
                self.window.after(100, self.load_users)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa người dùng: {str(e)}")
    
    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        # Hiển thị lại cửa sổ admin và đóng cửa sổ hiện tại
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()  # Hiển thị lại cửa sổ admin
        self.window.destroy()
    
    def logout(self):
        """Đăng xuất và quay về cửa sổ đăng nhập"""
        self.window.destroy()
        # Kiểm tra parent type để xử lý logout đúng cách
        if hasattr(self.parent, 'show_login_after_logout'):
            # Nếu parent là ExamBankApp
            self.parent.show_login_after_logout()
        else:
            # Nếu parent là window khác, tìm ExamBankApp
            current_parent = self.parent
            while hasattr(current_parent, 'parent'):
                current_parent = current_parent.parent
                if hasattr(current_parent, 'show_login_after_logout'):
                    current_parent.show_login_after_logout()
                    break
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!")
    
    def on_closing(self):
        """Xử lý khi đóng window"""
        self.back_to_admin()

# Quản lý môn học
class SubjectManagementWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.window if hasattr(parent, 'window') else parent)
        self.window.title("Quản lý môn học")
        self.window.geometry("800x600")
        self.setup_ui()
        self.load_subjects()
        
        # Thêm event handler để đảm bảo parent window được hiển thị khi đóng window này
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Thiết lập giao diện quản lý môn học"""
        self.window.title("Quản lý môn học - Hệ thống Quản lý Đề thi")
        self.window.geometry("800x600")
        
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        user_info = self.parent.current_user
        ttk.Label(header_frame, text=f"📚 Quản lý môn học - Admin: {user_info['full_name']}", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Nút quay lại và đăng xuất
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="⬅️ Quay lại", 
                  command=self.back_to_admin).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame quản lý môn học
        subjects_frame = ttk.LabelFrame(main_frame, text="Danh sách môn học", padding="10")
        subjects_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Treeview cho danh sách môn học với cột thao tác
        columns = ("ID", "Tên môn học", "Mã môn học", "Mô tả", "Số câu hỏi", "Ngày tạo", "Thao tác")
        self.subjects_tree = ttk.Treeview(subjects_frame, columns=columns, show="headings", height=15)
        
        # Cấu hình cột
        column_widths = {
            "ID": 60,
            "Tên môn học": 150,
            "Mã môn học": 100,
            "Mô tả": 180,
            "Số câu hỏi": 80,
            "Ngày tạo": 100,
            "Thao tác": 100
        }
        
        for col in columns:
            self.subjects_tree.heading(col, text=col)
            self.subjects_tree.column(col, width=column_widths[col], minwidth=50)
        
        # Đảm bảo cột "Thao tác" luôn hiển thị và có thể nhìn thấy
        self.subjects_tree.column("Thao tác", stretch=False, anchor="center")
        
        self.subjects_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(subjects_frame, orient="vertical", command=self.subjects_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.subjects_tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame nút chức năng đơn giản
        button_frame = ttk.Frame(subjects_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Nút thêm môn học mới
        ttk.Button(button_frame, text="➕ Thêm môn học mới", 
                  command=self.add_subject, 
                  style='AdminButton.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút sửa môn học
        ttk.Button(button_frame, text="✏️ Sửa môn học", 
                  command=self.edit_subject, 
                  style='AdminButton.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        # Cấu hình grid
        subjects_frame.columnconfigure(0, weight=1)
        subjects_frame.rowconfigure(0, weight=1)
        
        # Bind events
        self.subjects_tree.bind("<Double-1>", lambda e: self.edit_subject())
        self.subjects_tree.bind("<Button-1>", self.on_tree_click)
    
    # Không cần hàm manage_subjects và execute_and_close nữa
    
    def load_subjects(self):
        """Tải danh sách môn học"""
        try:
            from services import subject_service, question_service
            from services.api_client import clear_cache
            
            # Xóa cache trước khi tải dữ liệu mới
            clear_cache()
            
            # Xóa dữ liệu cũ trước
            for item in self.subjects_tree.get_children():
                self.subjects_tree.delete(item)
            
            # Tải dữ liệu mới
            subjects = subject_service.get_subjects()
            
            # Thêm dữ liệu mới
            for subject in subjects:
                try:
                    # Đếm số câu hỏi trong môn học
                    questions = question_service.get_questions(subject['id'])
                    question_count = len(questions)
                except:
                    question_count = 0
                
                created_at = subject.get('created_at', 'N/A')
                if isinstance(created_at, str) and created_at != 'N/A':
                    try:
                        import datetime
                        created_date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%d/%m/%Y')
                    except:
                        created_date = created_at
                else:
                    created_date = 'N/A'
                
                self.subjects_tree.insert("", "end", values=(
                    subject['id'],
                    subject['name'],
                    subject.get('code', ''),
                    subject.get('description', ''),
                    question_count,
                    created_date,
                    "🗑️ Xóa"  # Nút xóa trong cột thao tác
                ), tags=(subject['id'],))
            
            # Cập nhật UI ngay lập tức
            self.subjects_tree.update()
            self.window.update_idletasks()  # Đảm bảo UI được cập nhật
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")
    
    def on_tree_click(self, event):
        """Xử lý click vào treeview"""
        region = self.subjects_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.subjects_tree.identify_column(event.x)
            if column == "#7":  # Cột "Thao tác"
                item = self.subjects_tree.identify_row(event.y)
                if item:
                    subject_id = self.subjects_tree.item(item, "tags")[0]
                    self.delete_subject_by_id(subject_id)
    
    def delete_subject_by_id(self, subject_id):
        """Xóa môn học theo ID (từ click vào cột thao tác)"""
        try:
            from services import subject_service
            from services.api_client import clear_cache
            
            # Xóa cache trước khi kiểm tra
            clear_cache()
            
            # Kiểm tra môn học có tồn tại không
            try:
                subject = subject_service.get_subject(subject_id)
            except Exception:
                messagebox.showerror("❌ Lỗi", f"Môn học không tồn tại hoặc đã bị xóa!")
                self.load_subjects()  # Làm mới danh sách
                return
            
            # Lấy thông tin chi tiết từ subject
            subject_name = subject.get('name', 'N/A')
            subject_code = subject.get('code', 'N/A')
            
            result = messagebox.askyesno(
                "🗑️ Xác nhận xóa môn học", 
                f"Bạn có chắc chắn muốn xóa môn học này?\n\n"
                f"📝 Thông tin môn học:\n"
                f"• ID: {subject_id}\n"
                f"• Tên môn học: {subject_name}\n"
                f"• Mã môn học: {subject_code}\n\n"
                f"⚠️ Cảnh báo: Việc xóa môn học sẽ xóa tất cả câu hỏi và đề thi liên quan!\n\n"
                f"⚠️ Lưu ý: Hành động này không thể hoàn tác!"
            )
            
            if result:
                try:
                    # Xóa cache trước khi xóa
                    clear_cache()
                    subject_service.delete_subject(subject_id)
                    messagebox.showinfo("✅ Thành công", f"Đã xóa môn học {subject_name} thành công!")
                    
                    # Làm mới danh sách ngay lập tức
                    self.load_subjects()
                except Exception as e:
                    messagebox.showerror("❌ Lỗi", f"Không thể xóa môn học: {str(e)}")
                    # Làm mới danh sách nếu có lỗi
                    self.load_subjects()
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể xóa môn học: {str(e)}")
            # Làm mới danh sách
            self.load_subjects()
    
    def get_selected_subject_id(self):
        """Lấy ID của môn học được chọn"""
        selection = self.subjects_tree.selection()
        if not selection:
            return None
        return self.subjects_tree.item(selection[0], "tags")[0]
    
    def add_subject(self):
        """Thêm môn học mới"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Thêm môn học mới")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Form fields
        ttk.Label(frame, text="Tên môn học:", font=("Arial", 10, "bold")).pack(anchor="w")
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        ttk.Label(frame, text="Mã môn học:", font=("Arial", 10, "bold")).pack(anchor="w")
        code_var = tk.StringVar()
        ttk.Entry(frame, textvariable=code_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        ttk.Label(frame, text="Mô tả:", font=("Arial", 10, "bold")).pack(anchor="w")
        desc_var = tk.StringVar()
        ttk.Entry(frame, textvariable=desc_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        def validate_form():
            name = name_var.get().strip()
            code = code_var.get().strip()
            if not name:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập tên môn học!")
                return False
            if not code:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập mã môn học!")
                return False
            return True
        
        def save():
            if not validate_form():
                return
            
            name = name_var.get().strip()
            code = code_var.get().strip()
            description = desc_var.get().strip()
            
            # Xác nhận cuối cùng
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có chắc chắn muốn thêm môn học mới?\n\n"
                                       f"📋 Thông tin môn học:\n"
                                       f"• Tên môn học: {name}\n"
                                       f"• Mã môn học: {code}\n"
                                       f"• Mô tả: {description}")
            
            if not result:
                return
            
            try:
                from services import subject_service
                subject_service.create_subject({
                    "name": name,
                    "code": code,
                    "description": description
                })
                # Xóa cache và làm mới danh sách ngay lập tức
                from services.api_client import clear_cache
                clear_cache()
                
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã thêm môn học thành công!\n\n"
                                  f"📋 Thông tin môn học:\n"
                                  f"• Tên môn học: {name}\n"
                                  f"• Mã môn học: {code}\n"
                                  f"• Mô tả: {description}")
                dialog.destroy()
                
                # Làm mới danh sách ngay lập tức
                self.load_subjects()
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể thêm môn học:\n{str(e)}")
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="❌ Hủy", command=cancel, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✅ Thêm môn học", command=save, 
                  style='Accent.TButton', width=20).pack(side=tk.RIGHT)
    
    def edit_subject(self):
        """Sửa thông tin môn học"""
        subject_id = self.get_selected_subject_id()
        if not subject_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học để sửa!")
            return
        
        try:
            from services import subject_service
            subject = subject_service.get_subject(subject_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin môn học: {str(e)}")
            return
        
        dialog = tk.Toplevel(self.window)
        dialog.title("Sửa thông tin môn học")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill="both", expand=True)
        
        # Form fields
        ttk.Label(frame, text="Tên môn học:", font=("Arial", 10, "bold")).pack(anchor="w")
        name_var = tk.StringVar(value=subject['name'])
        ttk.Entry(frame, textvariable=name_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        ttk.Label(frame, text="Mã môn học:", font=("Arial", 10, "bold")).pack(anchor="w")
        code_var = tk.StringVar(value=subject.get('code', ''))
        ttk.Entry(frame, textvariable=code_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        ttk.Label(frame, text="Mô tả:", font=("Arial", 10, "bold")).pack(anchor="w")
        desc_var = tk.StringVar(value=subject.get('description', ''))
        ttk.Entry(frame, textvariable=desc_var, width=40, font=("Arial", 10)).pack(pady=(5, 15), fill="x")
        
        def validate_form():
            name = name_var.get().strip()
            code = code_var.get().strip()
            if not name:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập tên môn học!")
                return False
            if not code:
                messagebox.showwarning("Cảnh báo", "⚠️ Vui lòng nhập mã môn học!")
                return False
            return True
        
        def save():
            if not validate_form():
                return
            
            name = name_var.get().strip()
            code = code_var.get().strip()
            description = desc_var.get().strip()
            
            # Xác nhận cuối cùng
            result = messagebox.askyesno("Xác nhận", 
                                       f"Bạn có chắc chắn muốn cập nhật thông tin môn học?\n\n"
                                       f"📋 Thông tin mới:\n"
                                       f"• Tên môn học: {name}\n"
                                       f"• Mã môn học: {code}\n"
                                       f"• Mô tả: {description}")
            
            if not result:
                return
            
            try:
                from services import subject_service
                subject_service.update_subject(subject_id, {
                    "name": name,
                    "code": code,
                    "description": description
                })
                # Xóa cache và làm mới danh sách ngay lập tức
                from services.api_client import clear_cache
                clear_cache()
                
                messagebox.showinfo("✅ Thành công", 
                                  f"Đã cập nhật thông tin môn học thành công!\n\n"
                                  f"📋 Thông tin mới:\n"
                                       f"• Tên môn học: {name}\n"
                                       f"• Mã môn học: {code}\n"
                                       f"• Mô tả: {description}")
                dialog.destroy()
                
                # Làm mới danh sách ngay lập tức
                self.load_subjects()
            except Exception as e:
                messagebox.showerror("❌ Lỗi", f"Không thể cập nhật môn học:\n{str(e)}")
        
        def cancel():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(button_frame, text="❌ Hủy", command=cancel, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✅ Cập nhật", command=save, 
                  style='Accent.TButton', width=20).pack(side=tk.RIGHT)
    

    
    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        # Hiển thị lại cửa sổ admin và đóng cửa sổ hiện tại
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()  # Hiển thị lại cửa sổ admin
        self.window.destroy()
    
    def logout(self):
        """Đăng xuất và quay về cửa sổ đăng nhập"""
        self.window.destroy()
        # Kiểm tra parent type để xử lý logout đúng cách
        if hasattr(self.parent, 'show_login_after_logout'):
            # Nếu parent là ExamBankApp
            self.parent.show_login_after_logout()
        else:
            # Nếu parent là window khác, tìm ExamBankApp
            current_parent = self.parent
            while hasattr(current_parent, 'parent'):
                current_parent = current_parent.parent
                if hasattr(current_parent, 'show_login_after_logout'):
                    current_parent.show_login_after_logout()
                    break
        messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!")
    
    def on_closing(self):
        """Xử lý khi đóng window"""
        self.back_to_admin()