#!/usr/bin/env python3
"""
Script để sửa tất cả các method back_to_admin cho Admin role
"""

def fix_admin_back_buttons():
    """Sửa file admin_window.py để Admin có thể quay về dashboard chính"""
    with open('gui/admin_window.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sửa method back_to_admin trong AdminWindow
    old_pattern1 = '''    def back_to_admin(self):
        """Quay lại màn hình đăng nhập"""
        self.window.destroy()
        find_exambank_app_and_logout(self.parent)'''
    
    new_pattern1 = '''    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        self.window.destroy()
        # Hiển thị lại cửa sổ admin chính
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()
        else:
            # Nếu parent là ExamBankApp, tạo lại cửa sổ admin
            from gui.admin_window import AdminWindow
            AdminWindow(self.parent, None)'''
    
    content = content.replace(old_pattern1, new_pattern1)
    
    # Sửa method back_to_admin trong UserManagementWindow
    old_pattern2 = '''    def back_to_admin(self):
        """Quay lại màn hình đăng nhập"""
        self.window.destroy()
        find_exambank_app_and_logout(self.parent)'''
    
    new_pattern2 = '''    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        self.window.destroy()
        # Hiển thị lại cửa sổ admin chính
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()
        else:
            # Nếu parent là ExamBankApp, tạo lại cửa sổ admin
            from gui.admin_window import AdminWindow
            AdminWindow(self.parent, None)'''
    
    content = content.replace(old_pattern2, new_pattern2)
    
    # Sửa method back_to_admin trong SubjectManagementWindow
    old_pattern3 = '''    def back_to_admin(self):
        """Quay lại màn hình đăng nhập"""
        self.window.destroy()
        find_exambank_app_and_logout(self.parent)'''
    
    new_pattern3 = '''    def back_to_admin(self):
        """Quay lại màn hình Admin chính"""
        self.window.destroy()
        # Hiển thị lại cửa sổ admin chính
        if hasattr(self.parent, 'window'):
            self.parent.window.deiconify()
        else:
            # Nếu parent là ExamBankApp, tạo lại cửa sổ admin
            from gui.admin_window import AdminWindow
            AdminWindow(self.parent, None)'''
    
    content = content.replace(old_pattern3, new_pattern3)
    
    with open('gui/admin_window.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Đã sửa xong tất cả các method back_to_admin cho Admin role")

if __name__ == "__main__":
    fix_admin_back_buttons() 