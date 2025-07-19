#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test đơn giản để kiểm tra ứng dụng có chạy được không
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test import cơ bản"""
    print("=" * 50)
    print("TEST IMPORT CƠ BẢN")
    print("=" * 50)
    
    try:
        # Test tkinter
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("✅ tkinter imported successfully")
        
        # Test bcrypt
        import bcrypt
        print("✅ bcrypt imported successfully")
        
        # Test mysql-connector
        import mysql.connector
        print("✅ mysql-connector imported successfully")
        
        # Test python-docx
        from docx import Document
        print("✅ python-docx imported successfully")
        
        # Test các module của ứng dụng
        from database.database_manager import DatabaseManager
        print("✅ DatabaseManager imported successfully")
        
        from utils.auth import AuthManager
        print("✅ AuthManager imported successfully")
        
        from utils.docx_reader import DocxReader
        print("✅ DocxReader imported successfully")
        
        print("\n🎉 Tất cả import thành công!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Khắc phục: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test kết nối database"""
    print("\n" + "=" * 50)
    print("TEST KẾT NỐI DATABASE")
    print("=" * 50)
    
    try:
        from database.database_manager import DatabaseManager
        db = DatabaseManager()
        
        # Test query đơn giản
        result = db.execute_query("SELECT 1 as test")
        print("✅ Database connection successful")
        
        # Test bảng users
        users = db.execute_query("SELECT COUNT(*) as count FROM users")
        print(f"✅ Users table: {users[0]['count']} records")
        
        # Test bảng subjects
        subjects = db.execute_query("SELECT COUNT(*) as count FROM subjects")
        print(f"✅ Subjects table: {subjects[0]['count']} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("🔧 Khắc phục:")
        print("   1. Kiểm tra MySQL Server đã chạy chưa")
        print("   2. Kiểm tra config/database_config.py")
        print("   3. Đảm bảo database 'exam_bank' đã được tạo")
        return False

def test_auth_manager():
    """Test AuthManager"""
    print("\n" + "=" * 50)
    print("TEST AUTH MANAGER")
    print("=" * 50)
    
    try:
        from utils.auth import AuthManager
        auth = AuthManager()
        
        # Test tạo token
        success, result = auth.generate_reset_token("student1")
        if success:
            print(f"✅ Token generation successful: {result[:20]}...")
            
            # Test decode token
            token_info = auth.decode_token_info(result)
            if token_info:
                print(f"✅ Token decode successful: {token_info['username']}")
            else:
                print("❌ Token decode failed")
        else:
            print(f"❌ Token generation failed: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ AuthManager error: {e}")
        return False

def test_docx_reader():
    """Test DocxReader"""
    print("\n" + "=" * 50)
    print("TEST DOCX READER")
    print("=" * 50)
    
    try:
        from utils.docx_reader import DocxReader
        docx_reader = DocxReader()
        
        # Test các hàm parse
        test_question = "QN=1: Test question?"
        is_question = docx_reader._is_question_start(test_question)
        print(f"✅ Question parsing: {is_question}")
        
        test_option = "a. Test option"
        is_option = docx_reader._is_option(test_option)
        print(f"✅ Option parsing: {is_option}")
        
        test_answer = "ANSWER: A"
        is_answer = docx_reader._is_correct_answer(test_answer)
        print(f"✅ Answer parsing: {is_answer}")
        
        return True
        
    except Exception as e:
        print(f"❌ DocxReader error: {e}")
        return False

def main():
    """Hàm main"""
    print("🚀 TEST ỨNG DỤNG ĐƠN GIẢN")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_basic_imports():
        all_tests_passed = False
        print("\n⚠️ Vui lòng khắc phục lỗi import trước khi tiếp tục")
        return
    
    # Test database
    if not test_database_connection():
        all_tests_passed = False
        print("\n⚠️ Vui lòng khắc phục lỗi database trước khi tiếp tục")
        return
    
    # Test AuthManager
    if not test_auth_manager():
        all_tests_passed = False
    
    # Test DocxReader
    if not test_docx_reader():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 TẤT CẢ TEST THÀNH CÔNG!")
        print("✅ Ứng dụng sẵn sàng chạy")
        print("\n💡 Chạy ứng dụng:")
        print("   python main.py")
    else:
        print("❌ CÓ LỖI XẢY RA!")
        print("🔧 Vui lòng khắc phục các lỗi trên trước khi sử dụng")
    
    print("\n📋 HƯỚNG DẪN KHẮC PHỤC:")
    print("1. Cài đặt thư viện: pip install -r requirements.txt")
    print("2. Kiểm tra MySQL Server đã chạy chưa")
    print("3. Kiểm tra config/database_config.py")
    print("4. Chạy lại test: python test_simple.py")

if __name__ == "__main__":
    main() 