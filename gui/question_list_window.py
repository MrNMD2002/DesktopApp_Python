import tkinter as tk
from tkinter import ttk, messagebox
from services import question_service

class QuestionListWindow:
    def __init__(self, parent, subject_id, subject_name):
        self.parent = parent
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.window = tk.Toplevel(parent)
        self.window.title(f"Danh sách câu hỏi - {subject_name}")
        self.window.geometry("900x600")
        self.setup_ui()
        self.load_questions()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text=f"Danh sách câu hỏi môn: {self.subject_name}", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        columns = ("ID", "Nội dung", "A", "B", "C", "D", "Đúng", "Độ khó", "Điểm")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        # Nút xóa, sửa
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Xóa câu hỏi", command=self.delete_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Sửa câu hỏi", command=self.edit_question).pack(side=tk.LEFT, padx=5)
        # Không có nút refresh

        self.tree.bind('<Double-1>', lambda e: self.edit_question())

    def load_questions(self):
        try:
            questions = question_service.get_questions(self.subject_id)
            for item in self.tree.get_children():
                self.tree.delete(item)
            for q in questions:
                self.tree.insert("", "end", values=(
                    q['id'], q['question_text'], q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct_answer'], q.get('difficulty_level', ''), q.get('points', 1.0)
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải câu hỏi: {str(e)}")

    def get_selected_question_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return item['values'][0]

    def delete_question(self):
        qid = self.get_selected_question_id()
        if not qid:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi để xóa!")
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa câu hỏi này?"):
            try:
                question_service.delete_question(qid)
                self.load_questions()
                messagebox.showinfo("Thành công", "Đã xóa câu hỏi!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa câu hỏi: {str(e)}")

    def edit_question(self):
        qid = self.get_selected_question_id()
        if not qid:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn câu hỏi để sửa!")
            return
        # Lấy dữ liệu câu hỏi hiện tại
        questions = question_service.get_questions(self.subject_id)
        question = next((q for q in questions if q['id'] == qid), None)
        if not question:
            messagebox.showerror("Lỗi", "Không tìm thấy câu hỏi!")
            return
        # Tạo dialog sửa
        edit_win = tk.Toplevel(self.window)
        edit_win.title("Sửa câu hỏi")
        edit_win.geometry("600x500")
        frame = ttk.Frame(edit_win, padding="10")
        frame.pack(fill="both", expand=True)
        # Nội dung
        ttk.Label(frame, text="Nội dung câu hỏi:").grid(row=0, column=0, sticky="w")
        question_text_var = tk.StringVar(value=question['question_text'])
        ttk.Entry(frame, textvariable=question_text_var, width=70).grid(row=0, column=1, pady=5)
        # Đáp án
        ttk.Label(frame, text="A:").grid(row=1, column=0, sticky="w")
        a_var = tk.StringVar(value=question['option_a'])
        ttk.Entry(frame, textvariable=a_var, width=50).grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="B:").grid(row=2, column=0, sticky="w")
        b_var = tk.StringVar(value=question['option_b'])
        ttk.Entry(frame, textvariable=b_var, width=50).grid(row=2, column=1, pady=5)
        ttk.Label(frame, text="C:").grid(row=3, column=0, sticky="w")
        c_var = tk.StringVar(value=question['option_c'])
        ttk.Entry(frame, textvariable=c_var, width=50).grid(row=3, column=1, pady=5)
        ttk.Label(frame, text="D:").grid(row=4, column=0, sticky="w")
        d_var = tk.StringVar(value=question['option_d'])
        ttk.Entry(frame, textvariable=d_var, width=50).grid(row=4, column=1, pady=5)
        # Đáp án đúng
        ttk.Label(frame, text="Đáp án đúng (A/B/C/D):").grid(row=5, column=0, sticky="w")
        correct_var = tk.StringVar(value=question['correct_answer'])
        ttk.Entry(frame, textvariable=correct_var, width=5).grid(row=5, column=1, sticky="w", pady=5)
        # Độ khó
        ttk.Label(frame, text="Độ khó:").grid(row=6, column=0, sticky="w")
        diff_var = tk.StringVar(value=question.get('difficulty_level', 'medium'))
        ttk.Combobox(frame, textvariable=diff_var, values=["easy", "medium", "hard"], state="readonly").grid(row=6, column=1, sticky="w", pady=5)
        
        # Điểm số
        ttk.Label(frame, text="Điểm số:").grid(row=7, column=0, sticky="w")
        points_var = tk.StringVar(value=str(question.get('points', 1.0)))
        points_entry = ttk.Entry(frame, textvariable=points_var, width=10)
        points_entry.grid(row=7, column=1, sticky="w", pady=5)
        ttk.Label(frame, text="(0.1 - 10.0 điểm)", font=("Arial", 8), foreground="gray").grid(row=7, column=2, sticky="w", padx=(5, 0))
        
        # Nút lưu
        def save():
            try:
                points = float(points_var.get())
                if points < 0.1 or points > 10.0:
                    messagebox.showwarning("Cảnh báo", "Điểm số phải từ 0.1 đến 10.0!")
                    return
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Điểm số phải là số!")
                return
                
            data = {
                "question_text": question_text_var.get(),
                "option_a": a_var.get(),
                "option_b": b_var.get(),
                "option_c": c_var.get(),
                "option_d": d_var.get(),
                "correct_answer": correct_var.get().upper(),
                "difficulty_level": diff_var.get(),
                "points": points
            }
            try:
                question_service.update_question(qid, data)
                messagebox.showinfo("Thành công", "Đã cập nhật câu hỏi!")
                edit_win.destroy()
                self.load_questions()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
        ttk.Button(frame, text="💾 Lưu thay đổi", command=save).grid(row=8, column=0, columnspan=2, pady=15) 