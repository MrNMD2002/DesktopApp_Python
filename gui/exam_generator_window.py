import tkinter as tk
from tkinter import ttk, messagebox
from services import subject_service, exam_service, question_service
from gui.styles import ModernStyles
import datetime
import os
from PIL import Image, ImageTk  # Thêm các thư viện cần thiết

class ExamGeneratorWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        # Lấy current_user từ parent nếu có
        self.current_user = getattr(parent, 'current_user', None)
        # Nếu parent có thuộc tính window thì truyền parent.window, còn không thì truyền parent
        tk_parent = parent.window if hasattr(parent, 'window') else parent
        self.window = tk.Toplevel(tk_parent)
        # self.window = tk.Toplevel(self.parent.root)
        self.window.title("📊 Quản lý đề thi - Hệ thống Quản lý Đề thi")
        self.window.geometry("1000x700")

        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.window.configure(bg=ModernStyles.COLORS['light'])

        # Center window
        ModernStyles.center_window(self.window, 1000, 700)

        self.setup_ui()
        self.load_subjects()
        self.load_exams()

        # Thêm event handler để đảm bảo parent window được hiển thị khi đóng window này
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """Thiết lập giao diện người sinh đề"""
        self.window.title("Người sinh đề - Hệ thống Quản lý Đề thi")
        self.window.geometry("800x600")

        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        user_info = self.current_user
        if user_info and 'full_name' in user_info:
            name = user_info['full_name']
        else:
            name = "Quản trị viên"
        ttk.Label(header_frame, text=f"Chào mừng: {name}",
                  font=("Arial", 12, "bold")).pack(side=tk.LEFT)

        # Nút quay lại và đăng xuất
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)

        ttk.Button(button_frame, text="⬅️ Quay lại",
                   command=self.back_to_admin).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(button_frame, text="Đăng xuất",
                   command=self.logout).pack(side=tk.RIGHT)

        # Frame tạo đề thi mới
        create_frame = ttk.LabelFrame(main_frame, text="Tạo đề thi mới", padding="10")
        create_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Mã đề
        ttk.Label(create_frame, text="Mã đề:").grid(row=0, column=0, sticky="w", pady=2)
        self.exam_code_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.exam_code_var, width=20).grid(row=0, column=1, padx=(10, 0),
                                                                                sticky="w")

        # Tên đề
        ttk.Label(create_frame, text="Tên đề:").grid(row=0, column=2, sticky="w", padx=(20, 0), pady=2)
        self.exam_title_var = tk.StringVar()
        ttk.Entry(create_frame, textvariable=self.exam_title_var, width=30).grid(row=0, column=3, padx=(10, 0),
                                                                                 sticky="w")

        # Môn học
        ttk.Label(create_frame, text="Môn học:").grid(row=1, column=0, sticky="w", pady=2)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(create_frame, textvariable=self.subject_var,
                                          state="readonly", width=20)
        self.subject_combo.grid(row=1, column=1, padx=(10, 0), sticky="w")

        # Số câu hỏi
        ttk.Label(create_frame, text="Số câu hỏi:").grid(row=1, column=2, sticky="w", padx=(20, 0), pady=2)
        self.question_count_var = tk.StringVar(value="20")
        ttk.Entry(create_frame, textvariable=self.question_count_var, width=10).grid(row=1, column=3, padx=(10, 0),
                                                                                     sticky="w")

        # Thời gian làm bài
        ttk.Label(create_frame, text="Thời gian (phút):").grid(row=2, column=0, sticky="w", pady=2)
        self.duration_var = tk.StringVar(value="30")
        duration_frame = ttk.Frame(create_frame)
        duration_frame.grid(row=2, column=1, padx=(10, 0), sticky="w")
        ttk.Entry(duration_frame, textvariable=self.duration_var, width=10).pack(side=tk.LEFT)
        ttk.Label(duration_frame, text="(15-180 phút)", font=("Arial", 8), foreground="gray").pack(side=tk.LEFT,
                                                                                                   padx=(5, 0))

        # Nút tạo đề
        ttk.Button(create_frame, text="🎯 Tạo đề thi",
                   command=self.create_exam).grid(row=2, column=2, columnspan=2, padx=(20, 0), pady=10)

        # Frame quản lý môn học
        subject_mgmt_frame = ttk.LabelFrame(main_frame, text="Quản lý môn học", padding="10")
        subject_mgmt_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Nút quản lý môn học duy nhất
        ttk.Button(subject_mgmt_frame, text="📚 Quản lý môn học",
                   command=self.open_subject_management_dialog,
                   style='AdminButton.TButton').pack(pady=10)

        # Frame danh sách đề thi
        exams_frame = ttk.LabelFrame(main_frame, text="Danh sách đề thi", padding="10")
        exams_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Treeview cho danh sách đề thi với cột thao tác
        columns = ("Mã đề", "Tên đề", "Môn học", "Thời gian", "Số câu", "Ngày tạo", "Thao tác")
        self.exams_tree = ttk.Treeview(exams_frame, columns=columns, show="headings", height=10)

        # Cấu hình cột
        column_widths = {
            "Mã đề": 80,
            "Tên đề": 180,
            "Môn học": 120,
            "Thời gian": 80,
            "Số câu": 60,
            "Ngày tạo": 120,
            "Thao tác": 100
        }

        for col in columns:
            self.exams_tree.heading(col, text=col)
            self.exams_tree.column(col, width=column_widths[col], minwidth=50)

        self.exams_tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(exams_frame, orient="vertical", command=self.exams_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.exams_tree.configure(yscrollcommand=scrollbar.set)

        # Frame nút chức năng đơn giản
        button_frame = ttk.Frame(exams_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        # Nút xem chi tiết
        ttk.Button(button_frame, text="👁️ Xem chi tiết",
                   command=self.view_exam_details).pack(side=tk.LEFT, padx=(0, 10))

        # Nút xóa đề thi
        ttk.Button(button_frame, text="🗑️ Xóa đề thi",
                   command=self.delete_exam).pack(side=tk.LEFT, padx=(0, 10))

        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        exams_frame.columnconfigure(0, weight=1)
        exams_frame.rowconfigure(0, weight=1)
        create_frame.columnconfigure(3, weight=1)

        # Bind events
        self.exams_tree.bind("<Button-1>", self.on_exam_tree_click)

    def load_subjects(self):
        """Tải danh sách môn học"""
        try:
            from services.api_client import clear_cache

            # Xóa cache trước khi tải dữ liệu mới
            clear_cache()

            subjects = subject_service.get_subjects()

            subject_dict = {}
            subject_names = []

            for subject in subjects:
                subject_dict[subject['name']] = subject['id']
                subject_names.append(subject['name'])

            self.subject_combo['values'] = subject_names
            self.subject_dict = subject_dict

            if subject_names:
                self.subject_combo.set(subject_names[0])

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")

    def load_exams(self):
        """Tải danh sách đề thi"""
        try:
            from services.api_client import clear_cache

            # Xóa cache trước khi tải dữ liệu mới
            clear_cache()
            clear_cache()  # Clear cache 2 lần để đảm bảo

            exams = exam_service.get_exams()

            # Xóa dữ liệu cũ
            for item in self.exams_tree.get_children():
                self.exams_tree.delete(item)

            # Thêm dữ liệu mới
            for exam in exams:
                created_at = exam.get('created_at')
                if isinstance(created_at, str):
                    try:
                        created_date = datetime.datetime.fromisoformat(created_at).strftime('%d/%m/%Y %H:%M')
                    except Exception:
                        created_date = created_at
                else:
                    created_date = created_at.strftime('%d/%m/%Y %H:%M')
                self.exams_tree.insert("", "end", values=(
                    exam['exam_code'],
                    exam['title'],
                    exam['subject_name'],
                    f"{exam['duration']} phút",
                    exam['total_questions'],
                    created_date,
                    "🗑️ Xóa"  # Nút xóa trong cột thao tác
                ), tags=(exam['id'],))

            # Cập nhật UI ngay lập tức
            self.exams_tree.update()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách đề thi: {str(e)}")

    def create_exam(self):
        """Tạo đề thi mới"""
        exam_code = self.exam_code_var.get().strip()
        exam_title = self.exam_title_var.get().strip()
        subject_name = self.subject_var.get()
        question_count = self.question_count_var.get().strip()
        duration = self.duration_var.get().strip()

        # Kiểm tra dữ liệu đầu vào
        if not all([exam_code, exam_title, subject_name, question_count, duration]):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            question_count = int(question_count)
            duration = int(duration)

            if question_count <= 0:
                messagebox.showwarning("Cảnh báo", "Số câu hỏi phải lớn hơn 0!")
                return

            if duration < 15 or duration > 180:
                messagebox.showwarning("Cảnh báo", "Thời gian làm bài phải từ 15 đến 180 phút!")
                return

        except ValueError:
            messagebox.showwarning("Cảnh báo", "Số câu hỏi và thời gian phải là số!")
            return

        subject_id = self.subject_dict.get(subject_name)

        try:
            # Kiểm tra mã đề đã tồn tại chưa
            existing_exam = exam_service.get_exam_by_code(exam_code)

            if existing_exam:
                messagebox.showerror("Lỗi", "Mã đề đã tồn tại!")
                return

            # Kiểm tra số câu hỏi có sẵn
            available_questions = question_service.get_available_questions_count(subject_id)

            if not available_questions or available_questions['count'] < question_count:
                messagebox.showerror("Lỗi", f"Không đủ câu hỏi cho môn {subject_name}! "
                                            f"Cần {question_count} câu, có sẵn {available_questions['count'] if available_questions else 0} câu.")
                return

            # Lấy user_id tạo đề
            user_id = self.current_user['id'] if self.current_user and 'id' in self.current_user else None
            if not user_id:
                messagebox.showerror("Lỗi",
                                     "Không xác định được người tạo đề. Vui lòng đăng nhập lại hoặc liên hệ quản trị viên.")
                return

            # Tạo đề thi
            exam_id = exam_service.create_exam(exam_code, subject_id, exam_title, duration, question_count, user_id)

            # Chọn câu hỏi ngẫu nhiên và xáo trộn
            questions = question_service.get_random_questions(subject_id, question_count)

            # Thêm câu hỏi vào đề thi với thứ tự ngẫu nhiên
            exam_questions = []
            # Nếu exam_id là object (dict), lấy trường 'id'
            if isinstance(exam_id, dict):
                exam_id = exam_id.get('id')
            for i, question in enumerate(questions):
                qid = question['id'] if isinstance(question, dict) else question
                exam_questions.append((exam_id, qid, i + 1))
            question_service.add_questions_to_exam(exam_questions)

            messagebox.showinfo("🎯 Thành công",
                                f"✅ Đã tạo đề thi {exam_code} thành công!\n\n"
                                f"📝 Thông tin đề thi:\n"
                                f"• Tên đề: {exam_title}\n"
                                f"• Môn học: {subject_name}\n"
                                f"• Số câu: {question_count} câu\n"
                                f"• Thời gian: {duration} phút\n"
                                f"• Câu hỏi đã được xáo trộn ngẫu nhiên\n\n"
                                f"🎲 Mỗi lần làm bài, thứ tự câu hỏi sẽ khác nhau!")

            # Xóa form
            self.exam_code_var.set("")
            self.exam_title_var.set("")
            self.question_count_var.set("20")
            self.duration_var.set("30")

            # Cập nhật danh sách ngay lập tức với thông báo
            from services.api_client import clear_cache
            clear_cache()
            clear_cache()  # Clear cache 2 lần để đảm bảo
            self.window.after(50, self.load_exams)  # Giảm delay xuống 50ms

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo đề thi: {str(e)}")

    def view_exam_details(self):
        """Xem chi tiết đề thi"""
        selection = self.exams_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đề thi!")
            return

        exam_id = self.exams_tree.item(selection[0], "tags")[0]

        try:
            # Lấy thông tin đề thi
            exam_info = exam_service.get_exam_by_id(exam_id)

            if not exam_info:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin đề thi!")
                return

            exam = exam_info

            # Lấy danh sách câu hỏi
            questions = question_service.get_exam_questions(exam_id)

            # Hiển thị dialog chi tiết
            self.show_exam_details_dialog(exam, questions)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xem chi tiết đề thi: {str(e)}")

    def show_exam_details_dialog(self, exam, questions):
        """Hiển thị dialog chi tiết đề thi với hình ảnh"""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Chi tiết đề thi: {exam['exam_code']}")
        dialog.geometry("800x600")  # Tăng kích thước dialog để chứa ảnh
        dialog.transient(self.window)
        dialog.grab_set()

        # Danh sách để lưu tham chiếu đến các đối tượng PhotoImage, tránh bị garbage collector xóa
        self.image_references = []

        # Frame chính
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Thông tin đề thi
        info_frame = ttk.LabelFrame(main_frame, text="Thông tin đề thi", padding="10")
        info_frame.pack(fill="x", pady=(0, 10))

        created_at = exam.get('created_at')
        if isinstance(created_at, str):
            try:
                created_date = datetime.datetime.fromisoformat(created_at).strftime('%d/%m/%Y %H:%M')
            except Exception:
                created_date = created_at
        else:
            created_date = created_at.strftime('%d/%m/%Y %H:%M')

        info_text = f"""
        Mã đề: {exam['exam_code']}
        Tên đề: {exam['title']}
        Môn học: {exam['subject_name']}
        Thời gian: {exam['duration']} phút
        Số câu hỏi: {exam['total_questions']}
        Ngày tạo: {created_date}
        """

        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor="w")

        # Frame câu hỏi
        questions_frame = ttk.LabelFrame(main_frame, text="Danh sách câu hỏi", padding="10")
        questions_frame.pack(fill="both", expand=True)

        # Text widget cho câu hỏi
        text_widget = tk.Text(questions_frame, wrap="word", state="disabled", padx=5, pady=5)
        text_widget.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(questions_frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Hiển thị câu hỏi
        text_widget.config(state="normal")
        for i, question in enumerate(questions, 1):
            question_id = question.get('id')
            image_path = None

            if question_id:
                possible_extensions = ['.png', '.jpg', '.jpeg', '.gif']
                for ext in possible_extensions:
                    path_to_check = os.path.join('pictures', f"{question_id}{ext}")
                    if os.path.exists(path_to_check):
                        image_path = path_to_check
                        break

            # Image
            if image_path:
                try:
                    img = Image.open(image_path)
                    max_width = 400
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.LANCZOS)

                    photo_image = ImageTk.PhotoImage(img)
                    self.image_references.append(photo_image)  # Lưu tham chiếu

                    text_widget.image_create(tk.END, image=photo_image)
                    text_widget.insert(tk.END, '\n')
                except Exception as e:
                    print(f"Lỗi khi xử lý ảnh {image_path}: {e}")

            text_widget.insert(tk.END, f"Câu {i}: {question['question_text']}\n")
            text_widget.insert(tk.END, f"A. {question['option_a']}\n")
            text_widget.insert(tk.END, f"B. {question['option_b']}\n")
            text_widget.insert(tk.END, f"C. {question['option_c']}\n")
            text_widget.insert(tk.END, f"D. {question['option_d']}\n")
            text_widget.insert(tk.END, f"Đáp án đúng: {question['correct_answer']}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        text_widget.config(state="disabled")

    def on_exam_tree_click(self, event):
        """Xử lý click vào treeview đề thi"""
        region = self.exams_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.exams_tree.identify_column(event.x)
            if column == "#7":  # Cột "Thao tác"
                item = self.exams_tree.identify_row(event.y)
                if item:
                    exam_id = self.exams_tree.item(item, "tags")[0]
                    self.delete_exam_by_id(exam_id)

    def delete_exam_by_id(self, exam_id):
        """Xóa đề thi theo ID"""
        try:
            # Lấy thông tin đề thi
            exam_info = exam_service.get_exam_by_id(exam_id)
            if not exam_info:
                messagebox.showerror("Lỗi", "Không tìm thấy thông tin đề thi!")
                return

            exam_code = exam_info['exam_code']

            result = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa đề thi {exam_code}?")

            if result:
                # Xóa đề thi (API sẽ tự động xóa các bản ghi liên quan)
                exam_service.delete_exam(exam_id)

                messagebox.showinfo("✅ Thành công",
                                    f"Đã xóa đề thi {exam_code} thành công!\n\n🔄 Đang làm mới danh sách đề thi...")
                # Cập nhật danh sách ngay lập tức với nhiều lần clear cache
                from services.api_client import clear_cache
                clear_cache()
                clear_cache()  # Clear cache 2 lần để đảm bảo
                self.window.after(50, self.load_exams)  # Giảm delay xuống 50ms

        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể xóa đề thi: {str(e)}")

    def delete_exam(self):
        """Xóa đề thi được chọn"""
        selection = self.exams_tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn một đề thi để xóa!")
            return

        # Lấy thông tin đề thi từ dòng được chọn
        item = selection[0]
        values = self.exams_tree.item(item, "values")
        exam_id = self.exams_tree.item(item, "tags")[0]
        exam_code = values[0]  # Mã đề
        exam_title = values[1]  # Tên đề

        # Hiển thị thông tin xác nhận chi tiết hơn
        result = messagebox.askyesno(
            "🗑️ Xác nhận xóa đề thi",
            f"Bạn có chắc chắn muốn xóa đề thi này?\n\n"
            f"📝 Mã đề: {exam_code}\n"
            f"📋 Tên đề: {exam_title}\n\n"
            f"⚠️ Lưu ý: Hành động này không thể hoàn tác!"
        )

        if result:
            self.delete_exam_by_id(exam_id)

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

    def open_subject_management_dialog(self):
        """Mở dialog quản lý môn học với tất cả chức năng"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Quản lý môn học")
        dialog.geometry("900x700")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.resizable(True, True)

        # Căn giữa dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"900x700+{x}+{y}")

        # Main container frame
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_label = ttk.Label(main_frame, text="📚 Quản lý môn học", font=("Arial", 18, "bold"))
        header_label.pack(pady=(0, 20))

        # Frame chứa các nút chức năng
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 15))

        # Nút tạo môn học mới
        ttk.Button(button_frame, text="➕ Tạo môn học mới",
                   command=lambda: self.create_subject(dialog),
                   width=20).pack(side=tk.LEFT, padx=(0, 10))

        # Không có nút xóa môn học và refresh

        # Nút đóng
        ttk.Button(button_frame, text="❌ Đóng",
                   command=dialog.destroy,
                   width=15).pack(side=tk.RIGHT)

        # Frame tìm kiếm
        search_frame = ttk.LabelFrame(main_frame, text="🔍 Tìm kiếm môn học")
        search_frame.pack(fill="x", pady=(0, 15))

        # Tìm kiếm theo tên (real-time)
        ttk.Label(search_frame, text="🔍 Tìm kiếm (gõ để tìm real-time):").pack(side=tk.LEFT, padx=(10, 5))
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))

        # Thêm placeholder text bằng cách sử dụng bind
        def on_focus_in(event):
            if search_var.get() == "Nhập tên, mã hoặc mô tả môn học...":
                search_var.set("")
                search_entry.config(foreground="black")

        def on_focus_out(event):
            if search_var.get() == "":
                search_var.set("Nhập tên, mã hoặc mô tả môn học...")
                search_entry.config(foreground="gray")

        # Thiết lập placeholder ban đầu
        search_var.set("Nhập tên, mã hoặc mô tả môn học...")
        search_entry.config(foreground="gray")

        # Bind events cho placeholder
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)

        # Bind key release để tìm kiếm real-time
        search_var.trace('w', lambda *args: self.search_subjects_realtime(dialog, search_var.get()))

        # Bind Enter key để xóa tìm kiếm
        search_entry.bind('<Return>', lambda e: self.clear_search(dialog))
        search_entry.bind('<Escape>', lambda e: self.clear_search(dialog))

        # Hint cho người dùng
        hint_label = ttk.Label(search_frame, text="💡 Enter/Escape: Xóa tìm kiếm",
                               font=("Arial", 8), foreground="gray")
        hint_label.pack(side=tk.LEFT, padx=(10, 0))

        # Thêm separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)

        # Frame hiển thị danh sách môn học hiện tại
        list_frame = ttk.LabelFrame(main_frame, text="Danh sách môn học hiện tại")
        list_frame.pack(fill="both", expand=True)

        # Treeview cho danh sách môn học với kích thước lớn hơn
        columns = ("ID", "Tên môn học", "Mã môn học", "Mô tả", "Số câu hỏi", "Ngày tạo", "Thao tác")
        self.subjects_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)

        # Cấu hình cột với kích thước phù hợp
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

        self.subjects_tree.pack(fill="both", expand=True, padx=10, pady=10)
        # Đảm bảo cột "Thao tác" luôn hiển thị và có thể nhìn thấy
        self.subjects_tree.column("Thao tác", stretch=False, anchor="center")
        self.subjects_tree.grid(row=0, column=0, sticky="nsew")
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.subjects_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.subjects_tree.configure(yscrollcommand=scrollbar.set)

        # Bind double-click để chỉnh sửa môn học
        self.subjects_tree.bind("<Double-1>", lambda e: self.edit_subject_from_dialog(dialog))

        # Load danh sách môn học
        self.load_subjects_for_dialog()

        # Focus vào ô tìm kiếm
        search_entry.focus()

        # Lưu trữ danh sách gốc để tìm kiếm
        self.all_subjects = []
        self.subjects_tree.bind("<Button-1>", self.on_tree_click)

    def search_subjects(self, dialog, search_term):
        """Tìm kiếm môn học theo tên (không phân biệt chữ hoa/thường)"""
        if not search_term.strip():
            self.load_subjects_for_dialog()
            return

        try:
            # Chuẩn hóa từ khóa tìm kiếm
            search_term_normalized = search_term.strip().lower()

            # Lọc danh sách môn học theo từ khóa
            filtered_subjects = []
            for subject in self.all_subjects:
                # Chuẩn hóa tên môn học để so sánh
                subject_name_normalized = subject['name'].lower()
                subject_code_normalized = subject.get('code', '').lower()
                subject_desc_normalized = subject.get('description', '').lower()

                # Tìm kiếm trong tên, mã và mô tả môn học
                if (search_term_normalized in subject_name_normalized or
                        search_term_normalized in subject_code_normalized or
                        search_term_normalized in subject_desc_normalized):
                    filtered_subjects.append(subject)

            # Cập nhật treeview với kết quả tìm kiếm
            self._update_subjects_tree(filtered_subjects)

            if filtered_subjects:
                messagebox.showinfo("Kết quả tìm kiếm",
                                    f"Tìm thấy {len(filtered_subjects)} môn học!\n"
                                    f"Từ khóa: '{search_term}'")
            else:
                messagebox.showinfo("Kết quả tìm kiếm",
                                    f"Không tìm thấy môn học nào!\n"
                                    f"Từ khóa: '{search_term}'")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {str(e)}")

    def search_subjects_realtime(self, dialog, search_term):
        """Tìm kiếm real-time khi gõ (không hiển thị thông báo)"""
        # Kiểm tra nếu đang hiển thị placeholder thì không tìm kiếm
        if (not search_term.strip() or
                search_term == "Nhập tên, mã hoặc mô tả môn học..."):
            self.load_subjects_for_dialog()
            return

        try:
            # Chuẩn hóa từ khóa tìm kiếm
            search_term_normalized = search_term.strip().lower()

            # Lọc danh sách môn học theo từ khóa
            filtered_subjects = []
            for subject in self.all_subjects:
                # Chuẩn hóa tên môn học để so sánh
                subject_name_normalized = subject['name'].lower()
                subject_code_normalized = subject.get('code', '').lower()
                subject_desc_normalized = subject.get('description', '').lower()

                # Tìm kiếm trong tên, mã và mô tả môn học
                if (search_term_normalized in subject_name_normalized or
                        search_term_normalized in subject_code_normalized or
                        search_term_normalized in subject_desc_normalized):
                    filtered_subjects.append(subject)

            # Cập nhật treeview với kết quả tìm kiếm (không hiển thị thông báo)
            self._update_subjects_tree(filtered_subjects)

        except Exception as e:
            # Không hiển thị lỗi cho real-time search
            pass

    def clear_search(self, dialog):
        """Xóa tìm kiếm và hiển thị lại tất cả môn học"""
        # Tìm search_entry trong dialog
        for widget in dialog.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ttk.Entry):
                                # Reset placeholder
                                grandchild.delete(0, tk.END)
                                grandchild.insert(0, "Nhập tên, mã hoặc mô tả môn học...")
                                grandchild.config(foreground="gray")
                                break

        self.load_subjects_for_dialog()

    def edit_subject_from_dialog(self, dialog):
        """Chỉnh sửa môn học từ dialog"""
        selection = self.subjects_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học để chỉnh sửa!")
            return

        subject_id = self.subjects_tree.item(selection[0], "values")[0]
        subject_name = self.subjects_tree.item(selection[0], "values")[1]

        # Mở dialog chỉnh sửa môn học
        self._open_edit_subject_dialog(dialog, subject_id, subject_name)

    def _open_edit_subject_dialog(self, parent_dialog, subject_id, subject_name):
        """Mở dialog chỉnh sửa môn học"""
        try:
            from services import subject_service
            subject = subject_service.get_subject(subject_id)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin môn học: {str(e)}")
            return

        edit_dialog = tk.Toplevel(parent_dialog)
        edit_dialog.title(f"Chỉnh sửa môn học - {subject_name}")
        edit_dialog.geometry("500x400")
        edit_dialog.transient(parent_dialog)
        edit_dialog.grab_set()

        # Căn giữa dialog
        edit_dialog.update_idletasks()
        x = (edit_dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (edit_dialog.winfo_screenheight() // 2) - (400 // 2)
        edit_dialog.geometry(f"500x400+{x}+{y}")

        frame = ttk.Frame(edit_dialog, padding="20")
        frame.pack(fill="both", expand=True)

        # Form fields
        ttk.Label(frame, text="Tên môn học:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8,
                                                                               padx=(0, 10))
        name_var = tk.StringVar(value=subject['name'])
        ttk.Entry(frame, textvariable=name_var, width=35, font=("Arial", 10)).grid(row=0, column=1, sticky="ew", pady=8)

        ttk.Label(frame, text="Mã môn học:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8,
                                                                              padx=(0, 10))
        code_var = tk.StringVar(value=subject.get('code', ''))
        ttk.Entry(frame, textvariable=code_var, width=35, font=("Arial", 10)).grid(row=1, column=1, sticky="ew", pady=8)

        ttk.Label(frame, text="Mô tả:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=8,
                                                                         padx=(0, 10))
        desc_var = tk.StringVar(value=subject.get('description', ''))
        ttk.Entry(frame, textvariable=desc_var, width=35, font=("Arial", 10)).grid(row=2, column=1, sticky="ew", pady=8)

        def save_edit():
            try:
                subject_service.update_subject(subject_id, {
                    "name": name_var.get().strip(),
                    "code": code_var.get().strip(),
                    "description": desc_var.get().strip()
                })
                messagebox.showinfo("Thành công", "Đã cập nhật môn học thành công!")
                edit_dialog.destroy()
                self.load_subjects_for_dialog()
                self._load_subjects_silently()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật môn học: {str(e)}")

        def cancel_edit():
            edit_dialog.destroy()

        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(button_frame, text="❌ Hủy", command=cancel_edit, width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="✅ Lưu thay đổi", command=save_edit, width=18).pack(side=tk.RIGHT)

        # Cấu hình grid
        frame.columnconfigure(1, weight=1)

    def create_subject(self, dialog):
        """Tạo môn học mới"""
        from gui.admin_window import SubjectManagementWindow
        SubjectManagementWindow(self)
        dialog.destroy()

    def delete_subject_from_dialog(self, dialog):
        """Xóa môn học từ dialog"""
        selection = self.subjects_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học để xóa!")
            return

        subject_id = self.subjects_tree.item(selection[0], "values")[0]
        subject_name = self.subjects_tree.item(selection[0], "values")[1]

        result = messagebox.askyesno("Xác nhận",
                                     f"Bạn có chắc chắn muốn xóa môn học {subject_name}?\n\n"
                                     f"⚠️ Cảnh báo: Việc xóa môn học sẽ xóa tất cả câu hỏi và đề thi liên quan!")

        if result:
            try:
                from services import subject_service
                from services.api_client import clear_cache

                # Xóa môn học
                subject_service.delete_subject(subject_id)

                # Xóa cache để đảm bảo dữ liệu mới
                clear_cache()

                messagebox.showinfo("Thành công", f"Đã xóa môn học {subject_name}!")

                # Cập nhật lại tất cả dữ liệu
                self.load_subjects_for_dialog()  # Cập nhật dialog
                self._load_subjects_silently()  # Cập nhật main window
                self.load_exams()  # Cập nhật danh sách đề thi

                # Đảm bảo treeview được cập nhật
                self.subjects_tree.update()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa môn học: {str(e)}")

    def refresh_subjects(self, dialog):
        """Làm mới danh sách môn học"""
        try:
            from services.api_client import clear_cache

            # Xóa cache để đảm bảo dữ liệu mới
            clear_cache()

            # Cập nhật lại tất cả dữ liệu
            self.load_subjects_for_dialog()  # Cập nhật dialog
            self._load_subjects_silently()  # Cập nhật main window

            # Đảm bảo treeview được cập nhật
            self.subjects_tree.update()

            # Không hiển thị thông báo làm mới
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể làm mới danh sách môn học: {str(e)}")

    def _load_subjects_silently(self):
        """Tải danh sách môn học mà không hiển thị thông báo"""
        try:
            from services.api_client import clear_cache
            from services import subject_service

            # Xóa cache trước khi tải dữ liệu mới
            clear_cache()

            subjects = subject_service.get_subjects()

            subject_dict = {}
            subject_names = []

            for subject in subjects:
                subject_dict[subject['name']] = subject['id']
                subject_names.append(subject['name'])

            self.subject_combo['values'] = subject_names
            self.subject_dict = subject_dict

            if subject_names:
                self.subject_combo.set(subject_names[0])

        except Exception as e:
            # Không hiển thị thông báo lỗi cho silent loading
            pass

    def load_subjects_for_dialog(self):
        """Tải danh sách môn học cho dialog"""
        try:
            from services.api_client import clear_cache
            from services import subject_service

            # Xóa cache trước khi tải dữ liệu mới
            clear_cache()

            subjects = subject_service.get_subjects()

            # Lưu trữ danh sách gốc để tìm kiếm
            self.all_subjects = subjects

            # Cập nhật treeview
            self._update_subjects_tree(subjects)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {str(e)}")

    def _update_subjects_tree(self, subjects):
        """Cập nhật treeview với danh sách môn học"""
        # Xóa dữ liệu cũ
        for item in self.subjects_tree.get_children():
            self.subjects_tree.delete(item)

        # Thêm dữ liệu mới
        for subject in subjects:
            created_at = subject.get('created_at')
            if created_at:
                created_at = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                created_at = created_at.strftime('%d/%m/%Y %H:%M')
            else:
                created_at = "N/A"

            self.subjects_tree.insert("", "end", values=(
                subject['id'],
                subject['name'],
                subject.get('code', 'N/A'),
                subject.get('description', 'N/A'),
                subject.get('question_count', 0),
                created_at,
            ))
