import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from services import exam_service, question_service, answer_service, student_exam_service
from gui.styles import ModernStyles

class StudentWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.current_user = self.parent.current_user
        
        # Xác định parent window đúng cách
        if hasattr(parent, 'root'):
            # Nếu parent có thuộc tính root (ExamBankApp)
            parent_window = parent.root
        elif hasattr(parent, 'window'):
            # Nếu parent có thuộc tính window (AdminWindow, etc.)
            parent_window = parent.window
        else:
            # Fallback
            parent_window = parent
        
        self.window = tk.Toplevel(parent_window)
        self.window.title("👨‍🎓 Giao diện học sinh - Hệ thống Quản lý Đề thi")
        self.window.geometry("1000x700")
        
        # Apply modern styling
        ModernStyles.apply_modern_style()
        self.window.configure(bg=ModernStyles.COLORS['light'])
        
        # Center window
        ModernStyles.center_window(self.window, 1000, 700)
        
        # Ngăn đóng cửa sổ khi đang làm bài
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
        self.load_available_exams()
    
    def setup_ui(self):
        """Thiết lập giao diện học sinh"""
        self.window.title("👨‍🎓 Học sinh - Hệ thống Quản lý Đề thi")
        self.window.geometry("1000x700")
        
        # Tạo style cho student window
        style = ttk.Style()
        style.configure('Student.TFrame', background='#f8f9fa')
        style.configure('StudentHeader.TLabel', 
                       font=('Arial', 16, 'bold'), 
                       foreground='#2c3e50',
                       background='#f8f9fa')
        style.configure('Timer.TLabel',
                       font=('Arial', 14, 'bold'),
                       foreground='#e74c3c',
                       background='#f8f9fa')
        
        # Frame chính
        self.main_frame = ttk.Frame(self.window, padding="20", style='Student.TFrame')
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình grid
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Header với thông tin học sinh
        header_frame = ttk.Frame(self.main_frame, style='Student.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        # Thông tin học sinh
        user_info = self.current_user
        student_info_frame = ttk.Frame(header_frame, style='Student.TFrame')
        student_info_frame.pack(side=tk.LEFT)
        
        # Icon và tên học sinh
        student_icon = ttk.Label(student_info_frame, text="👨‍🎓", 
                                font=("Arial", 24), background='#f8f9fa')
        student_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        student_text_frame = ttk.Frame(student_info_frame, style='Student.TFrame')
        student_text_frame.pack(side=tk.LEFT)
        
        ttk.Label(student_text_frame, text="Giao diện học sinh", 
                 style="StudentHeader.TLabel").pack(anchor="w")
        
        ttk.Label(student_text_frame, text=f"Học sinh: {user_info['full_name']}", 
                 font=("Arial", 12), foreground="#7f8c8d",
                 background='#f8f9fa').pack(anchor="w")
        
        # Nút đăng xuất
        logout_frame = ttk.Frame(header_frame, style='Student.TFrame')
        logout_frame.pack(side=tk.RIGHT)
        
        ttk.Button(logout_frame, text="🚪 Đăng xuất", 
                  command=self.logout).pack(side=tk.RIGHT)
        
        # Frame chọn đề thi
        self.exam_selection_frame = ttk.LabelFrame(self.main_frame, text="Chọn đề thi", padding="10")
        self.exam_selection_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        
        # Danh sách đề thi
        ttk.Label(self.exam_selection_frame, text="Đề thi có sẵn:").grid(row=0, column=0, sticky="w")
        
        # Treeview cho danh sách đề thi
        columns = ("Mã đề", "Tên đề", "Môn học", "Thời gian", "Số câu", "Trạng thái")
        self.exam_tree = ttk.Treeview(self.exam_selection_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            self.exam_tree.heading(col, text=col)
            self.exam_tree.column(col, width=120)
        
        self.exam_tree.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Scrollbar cho treeview
        scrollbar = ttk.Scrollbar(self.exam_selection_frame, orient="vertical", command=self.exam_tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.exam_tree.configure(yscrollcommand=scrollbar.set)
        
        # Nút bắt đầu làm bài
        ttk.Button(self.exam_selection_frame, text="Bắt đầu làm bài", 
                  command=self.start_exam).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame làm bài thi (ẩn ban đầu)
        self.exam_frame = ttk.LabelFrame(self.main_frame, text="📝 Làm bài thi", 
                                        padding="15", style='Student.TFrame')
        
        # Header làm bài thi với timer nổi bật
        exam_header_frame = ttk.Frame(self.exam_frame, style='Student.TFrame')
        exam_header_frame.pack(fill="x", pady=(0, 15))
        
        # Thông tin đề thi bên trái
        exam_info_left = ttk.Frame(exam_header_frame, style='Student.TFrame')
        exam_info_left.pack(side=tk.LEFT)
        
        self.exam_title_label = ttk.Label(exam_info_left, text="", 
                                         font=("Arial", 14, "bold"), 
                                         foreground="#2c3e50",
                                         background='#f8f9fa')
        self.exam_title_label.pack(anchor="w")
        
        # Bộ đếm thời gian nổi bật bên phải
        timer_frame = ttk.Frame(exam_header_frame, style='Student.TFrame')
        timer_frame.pack(side=tk.RIGHT)
        
        timer_icon = ttk.Label(timer_frame, text="⏰", 
                              font=("Arial", 20), background='#f8f9fa')
        timer_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.time_label = ttk.Label(timer_frame, text="00:00", 
                                   style="Timer.TLabel")
        self.time_label.pack(side=tk.LEFT)
        
        # Frame thông tin câu hỏi
        question_info_frame = ttk.Frame(self.exam_frame, style='Student.TFrame')
        question_info_frame.pack(fill="x", pady=(0, 10))
        
        self.question_counter_label = ttk.Label(question_info_frame, 
                                               text="Câu 1/1", 
                                               font=("Arial", 12, "bold"),
                                               foreground="#3498db",
                                               background='#f8f9fa')
        self.question_counter_label.pack(side=tk.LEFT)
        
        # Nút nộp bài
        submit_button = ttk.Button(question_info_frame, text="📤 Nộp bài", 
                                  command=lambda: self.submit_exam(auto_submit=False),
                                  style="AdminButton.TButton")
        submit_button.pack(side=tk.RIGHT)
        
        # Frame câu hỏi
        self.question_frame = ttk.Frame(self.exam_frame)
        self.question_frame.pack(fill="both", expand=True, pady=10)
        
        self.question_text = tk.Text(self.question_frame, height=6, wrap="word", state="disabled")
        self.question_text.pack(fill="x", pady=(0, 10))
        
        # Frame đáp án
        self.options_frame = ttk.Frame(self.question_frame)
        self.options_frame.pack(fill="x")
        
        self.answer_var = tk.StringVar()
        self.option_buttons = {}
        
        for i, option in enumerate(['A', 'B', 'C', 'D']):
            btn = ttk.Radiobutton(self.options_frame, text="", variable=self.answer_var, 
                                 value=option, command=self.save_answer)
            btn.grid(row=i, column=0, sticky="w", pady=2)
            self.option_buttons[option] = btn
        
        # Frame điều hướng
        navigation_frame = ttk.Frame(self.exam_frame)
        navigation_frame.pack(fill="x", pady=10)
        
        ttk.Button(navigation_frame, text="Câu trước", 
                  command=self.previous_question).pack(side=tk.LEFT)
        
        self.question_counter_label = ttk.Label(navigation_frame, text="")
        self.question_counter_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(navigation_frame, text="Câu tiếp", 
                  command=self.next_question).pack(side=tk.LEFT)
        
        ttk.Button(navigation_frame, text="Nộp bài", 
                  command=self.submit_exam).pack(side=tk.RIGHT)
        
        # Bind events
        self.exam_tree.bind("<Double-1>", self.on_exam_double_click)
    
    def load_available_exams(self):
        """Tải danh sách đề thi có sẵn và trạng thái đã làm"""
        try:
            exams = exam_service.get_exams()
            student_exams = student_exam_service.get_student_exams(student_id=self.current_user['id'])
            exam_status_map = {}  # exam_id -> (status, student_exam_id, score)
            for se in student_exams:
                if se['status'] != 'in_progress':
                    exam_status_map[se['exam_id']] = (se['status'], se['id'], se.get('score'))
            # Xóa dữ liệu cũ
            for item in self.exam_tree.get_children():
                self.exam_tree.delete(item)
            # Thêm dữ liệu mới
            for exam in exams:
                status = "Chưa làm"
                student_exam_id = None
                score = None
                if exam['id'] in exam_status_map:
                    st, se_id, sc = exam_status_map[exam['id']]
                    status = f"Đã làm ({st})"
                    student_exam_id = se_id
                    score = sc
                self.exam_tree.insert("", "end", values=(
                    exam['exam_code'],
                    exam['title'],
                    exam['subject_name'],
                    f"{exam['duration']} phút",
                    exam['total_questions'],
                    status
                ), tags=(exam['id'], student_exam_id if student_exam_id else "", score if score else ""))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách đề thi: {str(e)}")

    def on_exam_double_click(self, event):
        selection = self.exam_tree.selection()
        if not selection:
            return
        item = self.exam_tree.item(selection[0])
        tags = item['tags']
        exam_id = tags[0]
        student_exam_id = tags[1] if len(tags) > 1 and tags[1] else None
        if student_exam_id:
            self.show_exam_review(exam_id, student_exam_id)
        else:
            self.start_exam()

    def show_exam_review(self, exam_id, student_exam_id):
        """Hiển thị cửa sổ xem lại bài thi đã làm"""
        import tkinter as tk
        from tkinter import Toplevel, Label, Frame, Text, Scrollbar, VERTICAL, RIGHT, Y, END
        review_win = Toplevel(self.window)
        review_win.title("Xem lại bài thi")
        review_win.geometry("900x700")
        # Lấy dữ liệu
        exam = exam_service.get_exam(exam_id)
        questions = question_service.get_exam_questions(exam_id)
        answers = answer_service.get_answers(student_exam_id=student_exam_id)
        answer_map = {a['question_id']: a for a in answers}
        # Thống kê
        correct_count = sum(1 for q in questions if answer_map.get(q['id'], {}).get('is_correct'))
        total_questions = len(questions)
        score = None
        for se in student_exam_service.get_student_exams(student_id=self.current_user['id']):
            if se['id'] == int(student_exam_id):
                score = se.get('score')
                break
        # Header
        Label(review_win, text=f"Đề: {exam['title']} - {exam['subject_name']}", font=("Arial", 14, "bold")).pack(pady=10)
        Label(review_win, text=f"Điểm: {score if score is not None else 0:.2f}/10 | Số câu đúng: {correct_count}/{total_questions}", font=("Arial", 12)).pack(pady=5)
        # Scrollable frame
        canvas = tk.Canvas(review_win)
        scrollbar = Scrollbar(review_win, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas)
        scroll_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Hiển thị từng câu hỏi
        for idx, q in enumerate(questions):
            qf = Frame(scroll_frame, bd=2, relief="groove", padx=8, pady=8)
            qf.pack(fill="x", pady=6, padx=8)
            Label(qf, text=f"Câu {idx+1}: {q['question_text']}", font=("Arial", 11, "bold"), wraplength=800, justify="left").pack(anchor="w")
            # Đáp án đúng
            Label(qf, text=f"Đáp án đúng: {q['correct_answer']}", fg="green").pack(anchor="w")
            # Đáp án học sinh
            ans = answer_map.get(q['id'])
            if ans:
                selected = ans.get('selected_answer')
                is_correct = ans.get('is_correct')
                color = "green" if is_correct else "red"
                Label(qf, text=f"Bạn chọn: {selected if selected else 'Không trả lời'}", fg=color).pack(anchor="w")
            else:
                Label(qf, text="Bạn chọn: Không trả lời", fg="red").pack(anchor="w")
        # Đóng
        tk.Button(review_win, text="Đóng", command=review_win.destroy).pack(pady=10)
    
    def start_exam(self):
        """Bắt đầu làm bài thi hoặc xem lại nếu đã làm"""
        selection = self.exam_tree.selection()
        if not selection:
            messagebox.showwarning("⚠️ Cảnh báo", "Vui lòng chọn một đề thi!")
            return
        item = self.exam_tree.item(selection[0])
        tags = item['tags']
        exam_id = tags[0]
        student_exam_id = tags[1] if len(tags) > 1 and tags[1] else None
        if student_exam_id:
            messagebox.showinfo("📋 Thông báo", "Bạn đã làm đề này rồi. Chuyển sang màn hình xem lại chi tiết bài thi.")
            self.show_exam_review(exam_id, student_exam_id)
            return
        
        # Xác nhận bắt đầu làm bài
        try:
            exam_info = exam_service.get_exam(exam_id)
            
            # Lấy số câu hỏi từ API
            questions = question_service.get_exam_questions(exam_id)
            question_count = len(questions) if questions else 0
            
            confirm_message = (
                f"📝 Bạn sắp bắt đầu làm bài thi:\n\n"
                f"📚 Tên đề: {exam_info.get('title', 'N/A')}\n"
                f"📖 Môn học: {exam_info.get('subject_name', 'N/A')}\n"
                f"⏰ Thời gian: {exam_info.get('duration', 0)} phút\n"
                f"❓ Số câu: {question_count} câu\n\n"
                f"⚠️ Lưu ý:\n"
                f"• Không thể thoát ra ngoài khi đang làm bài\n"
                f"• Bài thi sẽ tự động nộp khi hết giờ\n"
                f"• Hãy đảm bảo kết nối internet ổn định\n\n"
                f"Bạn có chắc chắn muốn bắt đầu làm bài?"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể lấy thông tin đề thi: {str(e)}")
            return
        
        result = messagebox.askyesno("🚀 Bắt đầu làm bài", confirm_message, icon='question')
        if not result:
            return
            
        try:
            exam = exam_service.get_exam(exam_id)
            self.current_exam = exam
            # Lấy đúng danh sách câu hỏi của đề thi
            questions = question_service.get_exam_questions(exam_id)
            self.questions = questions
            if not self.questions:
                messagebox.showerror("❌ Lỗi", "Đề thi không có câu hỏi!")
                return
            student_exam = student_exam_service.create_student_exam(self.current_user['id'], exam_id)
            self.student_exam_id = student_exam['id']
            # Khởi tạo
            self.current_question_index = 0
            self.answers = {}
            self.start_time = datetime.datetime.now()
            # Hiển thị giao diện làm bài
            self.exam_selection_frame.grid_remove()
            self.exam_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
            # Hiển thị câu hỏi đầu tiên
            self.display_question()
            # Bắt đầu đếm thời gian
            self.update_timer()
            
            # Thông báo bắt đầu
            duration = exam.get('duration', 0)
            messagebox.showinfo("🎯 Bắt đầu!", 
                              f"📝 Bài thi đã bắt đầu!\n"
                              f"⏰ Thời gian: {duration} phút\n"
                              f"❓ Số câu: {len(self.questions)} câu\n\n"
                              f"Chúc bạn làm bài tốt! 🍀")
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể bắt đầu bài thi: {str(e)}")
    
    def display_question(self):
        """Hiển thị câu hỏi hiện tại"""
        if not self.questions or self.current_question_index >= len(self.questions):
            return
        
        question = self.questions[self.current_question_index]
        
        # Cập nhật thông tin đề thi
        if self.current_exam:
            title = self.current_exam.get('title', 'N/A')
            subject_name = self.current_exam.get('subject_name', 'N/A')
            self.exam_title_label.config(text=f"{title} - {subject_name}")
        
        # Hiển thị câu hỏi
        self.question_text.config(state="normal")
        self.question_text.delete(1.0, tk.END)
        question_text = question.get('question_text', 'Không có nội dung câu hỏi')
        self.question_text.insert(1.0, f"Câu {self.current_question_index + 1}: {question_text}")
        self.question_text.config(state="disabled")
        
        # Hiển thị đáp án
        options = [
            ('A', question.get('option_a', 'Không có đáp án')),
            ('B', question.get('option_b', 'Không có đáp án')),
            ('C', question.get('option_c', 'Không có đáp án')),
            ('D', question.get('option_d', 'Không có đáp án'))
        ]
        
        for option, text in options:
            if option in self.option_buttons:
                self.option_buttons[option].config(text=f"{option}. {text}")
        
        # Cập nhật câu trả lời đã chọn
        question_id = question.get('id')
        if question_id and question_id in self.answers:
            self.answer_var.set(self.answers[question_id])
        else:
            self.answer_var.set("")
        
        # Cập nhật số câu
        self.question_counter_label.config(
            text=f"Câu {self.current_question_index + 1}/{len(self.questions)}"
        )
    
    def save_answer(self):
        """Lưu câu trả lời"""
        if not self.questions or self.current_question_index >= len(self.questions):
            return
        
        question = self.questions[self.current_question_index]
        question_id = question.get('id')
        selected_answer = self.answer_var.get()
        
        if question_id and selected_answer:
            self.answers[question_id] = selected_answer
    
    def next_question(self):
        """Chuyển đến câu hỏi tiếp theo"""
        self.save_answer()
        
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_question()
    
    def previous_question(self):
        """Chuyển đến câu hỏi trước"""
        self.save_answer()
        
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.display_question()
    
    def update_timer(self):
        if not self.start_time or not self.current_exam:
            return

        elapsed = datetime.datetime.now() - self.start_time
        duration = self.current_exam.get('duration', 0)
        remaining = datetime.timedelta(minutes=duration) - elapsed

        if remaining.total_seconds() <= 0:
            messagebox.showinfo("⏰ Hết giờ", "Đã hết thời gian làm bài, hệ thống sẽ tự động nộp bài!")
            self.submit_exam(auto_submit=True)
            return

        minutes = int(remaining.total_seconds() // 60)
        seconds = int(remaining.total_seconds() % 60)
        
        # Đổi màu timer dựa trên thời gian còn lại
        if remaining.total_seconds() <= 300:  # 5 phút cuối
            self.time_label.config(
                text=f"{minutes:02d}:{seconds:02d}",
                foreground="#e74c3c",  # Đỏ
                font=("Arial", 16, "bold")
            )
        elif remaining.total_seconds() <= 600:  # 10 phút cuối
            self.time_label.config(
                text=f"{minutes:02d}:{seconds:02d}",
                foreground="#f39c12",  # Cam
                font=("Arial", 15, "bold")
            )
        else:
            self.time_label.config(
                text=f"{minutes:02d}:{seconds:02d}",
                foreground="#27ae60",  # Xanh
                font=("Arial", 14, "bold")
            )

        self.window.after(1000, self.update_timer)
    
    def submit_exam(self, auto_submit=False):
        self.save_answer()

        if not self.questions:
            messagebox.showwarning("Cảnh báo", "Không có câu hỏi nào trong đề!")
            return

        total_questions = len(self.questions)
        answered_questions = len(self.answers)
        unanswered_questions = total_questions - answered_questions
        unanswered_list = [f"Câu {i+1}" for i, q in enumerate(self.questions) if q['id'] not in self.answers]

        # Nếu là auto_submit (hết giờ), chỉ thông báo hết giờ và nộp luôn
        if auto_submit:
            messagebox.showinfo("Hết thời gian", "⏰ Đã hết thời gian làm bài. Hệ thống sẽ tự động nộp bài của bạn.")
        else:
            # Nếu còn câu chưa trả lời, cảnh báo riêng, nếu bấm tiếp mới nộp thật
            if unanswered_questions > 0:
                confirm_message = (
                    f"Bạn còn {unanswered_questions} câu hỏi chưa trả lời.\n"
                    f"Bạn có chắc chắn muốn nộp bài không?\n\n"
                    f"❓ Câu hỏi chưa trả lời:\n• " + "\n• ".join(unanswered_list[:5])
                )
                if len(unanswered_list) > 5:
                    confirm_message += f"\n• ... và {len(unanswered_list) - 5} câu khác"
                confirm_message += "\n\n⚠️ Sau khi nộp bài, bạn không thể sửa đổi câu trả lời!"
                result = messagebox.askyesno("Cảnh báo", confirm_message, icon='warning')
                if not result:
                    return
            else:
                # Nếu đã trả lời hết, xác nhận nộp bài như bình thường
                result = messagebox.askyesno(
                    "Xác nhận nộp bài",
                    "Bạn có chắc chắn muốn nộp bài không? Sau khi nộp, bạn không thể sửa đổi câu trả lời!",
                    icon='question'
                )
                if not result:
                    return

        try:
            correct_count = 0
            for question in self.questions:
                question_id = question.get('id')
                correct_answer = question.get('correct_answer')
                selected_answer = self.answers.get(question_id)
                
                if question_id and correct_answer:
                    is_correct = (selected_answer == correct_answer) if selected_answer else False
                    if is_correct:
                        correct_count += 1
                    answer_service.create_answer(self.student_exam_id, question_id, selected_answer, is_correct)
            
            # Tính điểm dựa trên điểm số từng câu
            score = student_exam_service.calculate_score(self.student_exam_id)
            student_exam_service.update_student_exam_score(self.student_exam_id, score)
            
            messagebox.showinfo("🎯 Kết quả", 
                              f"✅ Điểm của bạn: {score:.2f}/10\n"
                              f"📝 Số câu đúng: {correct_count}/{total_questions}\n"
                              f"📊 Tỷ lệ đúng: {(correct_count/total_questions)*100:.1f}%")
            self.back_to_exam_selection()
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể nộp bài: {str(e)}")
    
    def back_to_exam_selection(self):
        """Quay lại màn hình chọn đề thi"""
        # Dừng timer nếu đang chạy
        if hasattr(self, 'start_time') and self.start_time:
            self.start_time = None
        
        self.exam_frame.grid_remove()
        self.exam_selection_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        self.load_available_exams()
    
    def back_to_login(self):
        """Quay lại cửa sổ đăng nhập"""
        # Chỉ đóng window hiện tại, parent window vẫn hiển thị
        self.window.destroy()
    
    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        # Kiểm tra xem có đang làm bài thi không
        if hasattr(self, 'start_time') and self.start_time:
            result = messagebox.askyesno(
                "⚠️ Cảnh báo", 
                "Bạn đang làm bài thi!\n\n"
                "Nếu đóng cửa sổ này, bài thi sẽ bị hủy và bạn sẽ mất tất cả câu trả lời.\n\n"
                "Bạn có chắc chắn muốn thoát?",
                icon='warning'
            )
            if result:
                # Nộp bài trước khi thoát
                self.submit_exam(auto_submit=True)
            else:
                return  # Không đóng cửa sổ
        
        # Nếu không làm bài thi, thoát bình thường
        self.parent.current_user = None
        self.window.destroy()
        messagebox.showinfo("👋 Thông báo", "Đã đăng xuất thành công!")
    
    def logout(self):
        """Đăng xuất và quay về cửa sổ đăng nhập"""
        # Kiểm tra xem có đang làm bài thi không
        if hasattr(self, 'start_time') and self.start_time:
            result = messagebox.askyesno(
                "⚠️ Cảnh báo", 
                "Bạn đang làm bài thi!\n\n"
                "Nếu đăng xuất, bài thi sẽ bị hủy và bạn sẽ mất tất cả câu trả lời.\n\n"
                "Bạn có chắc chắn muốn đăng xuất?",
                icon='warning'
            )
            if not result:
                return
        
        # Chỉ đóng dialog này, không đóng parent window
        self.window.destroy()
        
        # Nếu parent là ExamBankApp, quay về login
        if hasattr(self.parent, 'show_login_after_logout'):
            self.parent.show_login_after_logout()
            messagebox.showinfo("Thông báo", "Đã đăng xuất thành công!") 