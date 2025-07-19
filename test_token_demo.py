#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo chức năng Token Reset Mật khẩu có ý nghĩa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.auth import AuthManager
import datetime
import secrets
import string

def demo_token_structure():
    """Demo cấu trúc token"""
    print("=" * 60)
    print("🔑 DEMO CẤU TRÚC TOKEN RESET MẬT KHẨU")
    print("=" * 60)
    
    # Tạo token mẫu
    username = "student1"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    token = f"RESET-{username}-{timestamp}-{random_part}"
    
    print(f"Token mẫu: {token}")
    print()
    print("📋 Cấu trúc token:")
    print(f"   RESET-{username}-{timestamp}-{random_part}")
    print("   │     │        │         │")
    print("   │     │        │         └── 6 ký tự ngẫu nhiên")
    print("   │     │        └── Timestamp (YYYYMMDDHHMMSS)")
    print("   │     └── Username")
    print("   └── Prefix cố định")
    print()
    
    # Giải mã thông tin
    auth = AuthManager()
    token_info = auth.decode_token_info(token)
    
    if token_info:
        print("🔍 Thông tin giải mã từ token:")
        print(f"   Username: {token_info['username']}")
        print(f"   Thời gian tạo: {token_info['timestamp']}")
        print(f"   Random part: {token_info['random_part']}")
        print(f"   Trạng thái: {'✅ Hợp lệ' if token_info['is_valid'] else '❌ Không hợp lệ'}")
    else:
        print("❌ Không thể giải mã token")

def demo_multiple_tokens():
    """Demo tạo nhiều token cho các user khác nhau"""
    print("\n" + "=" * 60)
    print("👥 DEMO TOKEN CHO NHIỀU USER")
    print("=" * 60)
    
    users = [
        ("student1", "Học sinh 1"),
        ("creator1", "Người tạo câu hỏi 1"),
        ("admin", "Administrator"),
        ("teacher1", "Giáo viên 1")
    ]
    
    auth = AuthManager()
    
    for username, full_name in users:
        # Tạo token mẫu
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        token = f"RESET-{username}-{timestamp}-{random_part}"
        
        print(f"\n👤 {full_name} ({username}):")
        print(f"   Token: {token}")
        
        # Giải mã thông tin
        token_info = auth.decode_token_info(token)
        if token_info:
            print(f"   Thời gian: {token_info['timestamp']}")
            print(f"   Random: {token_info['random_part']}")

def demo_token_validation():
    """Demo kiểm tra tính hợp lệ của token"""
    print("\n" + "=" * 60)
    print("✅ DEMO KIỂM TRA TÍNH HỢP LỆ TOKEN")
    print("=" * 60)
    
    # Token hợp lệ
    valid_token = "RESET-student1-20241201143022-ABC123"
    
    # Token không hợp lệ
    invalid_tokens = [
        "INVALID-student1-20241201143022-ABC123",  # Sai prefix
        "RESET-student1-ABC123",                   # Thiếu phần
        "RESET-student1-20241201143022",           # Thiếu random
        "student1-20241201143022-ABC123",          # Thiếu RESET
        "RESET-student1-20241201143022-ABC123-EXTRA",  # Thừa phần
        "reset-student1-20241201143022-ABC123",    # Sai case
    ]
    
    auth = AuthManager()
    
    print(f"✅ Token hợp lệ: {valid_token}")
    token_info = auth.decode_token_info(valid_token)
    if token_info:
        print(f"   Kết quả: {token_info}")
    else:
        print("   Kết quả: Không thể giải mã")
    
    print("\n❌ Các token không hợp lệ:")
    for i, token in enumerate(invalid_tokens, 1):
        print(f"\n{i}. {token}")
        token_info = auth.decode_token_info(token)
        if token_info:
            print(f"   Kết quả: {token_info}")
        else:
            print("   Kết quả: Token không đúng định dạng")

def demo_token_expiration():
    """Demo token hết hạn"""
    print("\n" + "=" * 60)
    print("⏰ DEMO TOKEN HẾT HẠN")
    print("=" * 60)
    
    # Token cũ (quá 1 giờ)
    old_timestamp = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y%m%d%H%M%S")
    expired_token = f"RESET-student1-{old_timestamp}-ABC123"
    
    # Token mới (trong 1 giờ)
    new_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    valid_token = f"RESET-student1-{new_timestamp}-ABC123"
    
    auth = AuthManager()
    
    print(f"⏰ Token cũ (quá 1 giờ): {expired_token}")
    token_info = auth.decode_token_info(expired_token)
    if token_info:
        print(f"   Thời gian tạo: {token_info['timestamp']}")
        print(f"   Trạng thái: {'✅ Hợp lệ' if token_info['is_valid'] else '❌ Hết hạn'}")
    
    print(f"\n✅ Token mới (trong 1 giờ): {valid_token}")
    token_info = auth.decode_token_info(valid_token)
    if token_info:
        print(f"   Thời gian tạo: {token_info['timestamp']}")
        print(f"   Trạng thái: {'✅ Hợp lệ' if token_info['is_valid'] else '❌ Hết hạn'}")

def demo_real_token_generation():
    """Demo tạo token thật từ database"""
    print("\n" + "=" * 60)
    print("🎯 DEMO TẠO TOKEN THẬT TỪ DATABASE")
    print("=" * 60)
    
    try:
        auth = AuthManager()
        
        # Thử tạo token cho user có trong database
        test_users = ["student1", "creator1", "admin"]
        
        for username in test_users:
            print(f"\n👤 Thử tạo token cho: {username}")
            
            success, result = auth.generate_reset_token(username)
            
            if success:
                token = result
                print(f"   ✅ Token tạo thành công: {token}")
                
                # Giải mã thông tin
                token_info = auth.decode_token_info(token)
                if token_info:
                    print(f"   📋 Thông tin: {token_info}")
                
                # Kiểm tra tính hợp lệ
                is_valid, message = auth.verify_reset_token(token)
                print(f"   🔍 Kiểm tra hợp lệ: {'✅ Có' if is_valid else '❌ Không'}")
                
            else:
                print(f"   ❌ Lỗi: {result}")
                
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        print("💡 Đảm bảo MySQL đang chạy và database đã được setup")

def main():
    """Hàm main"""
    print("🚀 DEMO CHỨC NĂNG TOKEN RESET MẬT KHẨU")
    print("=" * 60)
    print("Chức năng này cho phép tạo token có ý nghĩa để reset mật khẩu")
    print("Token có cấu trúc: RESET-USERNAME-TIMESTAMP-RANDOM")
    print("Hạn sử dụng: 1 giờ")
    print("=" * 60)
    
    # Demo các chức năng
    demo_token_structure()
    demo_multiple_tokens()
    demo_token_validation()
    demo_token_expiration()
    demo_real_token_generation()
    
    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH DEMO")
    print("=" * 60)
    print("💡 Để sử dụng trong ứng dụng:")
    print("   1. Vào màn hình đăng nhập")
    print("   2. Chọn 'Quên mật khẩu'")
    print("   3. Nhập username để nhận token")
    print("   4. Sử dụng token để reset mật khẩu")
    print("=" * 60)

if __name__ == "__main__":
    main() 