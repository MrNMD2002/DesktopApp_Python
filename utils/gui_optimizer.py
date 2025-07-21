#!/usr/bin/env python3
"""
GUI Optimizer - Tối ưu hóa hiệu suất giao diện
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
from typing import Callable, Any

class GUIOptimizer:
    """Tối ưu hóa hiệu suất GUI"""
    
    @staticmethod
    def lazy_load_treeview(tree: ttk.Treeview, load_function: Callable, 
                          batch_size: int = 50, delay: float = 0.1):
        """Load dữ liệu vào Treeview theo batch để tránh lag"""
        
        def load_batch():
            try:
                items = load_function()
                if not items:
                    return
                
                # Load theo batch
                for i in range(0, len(items), batch_size):
                    batch = items[i:i + batch_size]
                    for item in batch:
                        tree.insert("", "end", values=item)
                    
                    # Cập nhật GUI và nghỉ một chút
                    tree.update()
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"Lỗi lazy loading: {e}")
        
        # Chạy trong thread riêng để không block GUI
        thread = threading.Thread(target=load_batch, daemon=True)
        thread.start()
    
    @staticmethod
    def debounce(func: Callable, delay: float = 0.3):
        """Debounce function để tránh gọi quá nhiều lần"""
        timer = None
        
        def debounced(*args, **kwargs):
            nonlocal timer
            if timer:
                timer.cancel()
            
            def delayed():
                func(*args, **kwargs)
            
            timer = threading.Timer(delay, delayed)
            timer.start()
        
        return debounced
    
    @staticmethod
    def throttle(func: Callable, delay: float = 0.1):
        """Throttle function để giới hạn tần suất gọi"""
        last_called = 0
        
        def throttled(*args, **kwargs):
            nonlocal last_called
            current_time = time.time()
            
            if current_time - last_called >= delay:
                last_called = current_time
                return func(*args, **kwargs)
        
        return throttled
    
    @staticmethod
    def optimize_treeview(tree: ttk.Treeview):
        """Tối ưu hóa Treeview"""
        # Tắt animation
        tree.configure(selectmode="browse")
        
        # Tối ưu scroll
        def on_scroll(*args):
            tree.yview(*args)
            tree.update_idletasks()
        
        return on_scroll
    
    @staticmethod
    def create_loading_indicator(parent, text="Đang tải..."):
        """Tạo loading indicator"""
        frame = ttk.Frame(parent)
        frame.pack(expand=True, fill="both")
        
        label = ttk.Label(frame, text=text, font=("Arial", 12))
        label.pack(expand=True)
        
        progress = ttk.Progressbar(frame, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()
        
        return frame, progress
    
    @staticmethod
    def remove_loading_indicator(loading_frame):
        """Xóa loading indicator"""
        if loading_frame:
            loading_frame.destroy()

class PerformanceMonitor:
    """Monitor hiệu suất GUI"""
    
    def __init__(self):
        self.start_time = None
        self.operations = {}
    
    def start_operation(self, name: str):
        """Bắt đầu đo thời gian operation"""
        self.operations[name] = time.time()
    
    def end_operation(self, name: str) -> float:
        """Kết thúc đo thời gian operation"""
        if name in self.operations:
            duration = time.time() - self.operations[name]
            del self.operations[name]
            return duration
        return 0
    
    def log_operation(self, name: str, duration: float):
        """Log thời gian operation"""
        if duration > 1.0:  # Chỉ log những operation chậm
            print(f"⚠️ Slow operation: {name} took {duration:.2f}s") 