#!/usr/bin/env python3
"""
Script test chức năng quản lý môn học
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_subject_management():
    """Test các chức năng quản lý môn học"""
    
    print("🧪 Testing Subject Management API...")
    
    # Test 1: Lấy danh sách môn học
    print("\n1. Lấy danh sách môn học hiện tại:")
    try:
        response = requests.get(f"{BASE_URL}/subjects/")
        if response.status_code == 200:
            subjects = response.json()
            print(f"✅ Thành công! Có {len(subjects)} môn học:")
            for subject in subjects:
                print(f"   - ID: {subject['id']}, Tên: {subject['name']}, Mã: {subject.get('code', 'N/A')}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    # Test 2: Tạo môn học mới
    print("\n2. Tạo môn học mới:")
    new_subject = {
        "name": "Lập trình Python",
        "code": "PYTHON",
        "description": "Môn học về lập trình Python cơ bản và nâng cao"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/subjects/", json=new_subject)
        if response.status_code == 200:
            created_subject = response.json()
            print(f"✅ Thành công! Đã tạo môn học:")
            print(f"   - ID: {created_subject['id']}")
            print(f"   - Tên: {created_subject['name']}")
            print(f"   - Mã: {created_subject['code']}")
            print(f"   - Mô tả: {created_subject['description']}")
            
            subject_id = created_subject['id']
        else:
            print(f"❌ Lỗi tạo môn học: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return
    
    # Test 3: Cập nhật môn học
    print("\n3. Cập nhật môn học:")
    updated_subject = {
        "name": "Lập trình Python Nâng cao",
        "code": "PYTHON_ADV",
        "description": "Môn học về lập trình Python nâng cao với các framework"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/subjects/{subject_id}", json=updated_subject)
        if response.status_code == 200:
            updated = response.json()
            print(f"✅ Thành công! Đã cập nhật môn học:")
            print(f"   - Tên mới: {updated['name']}")
            print(f"   - Mã mới: {updated['code']}")
            print(f"   - Mô tả mới: {updated['description']}")
        else:
            print(f"❌ Lỗi cập nhật: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    # Test 4: Lấy thông tin môn học cụ thể
    print("\n4. Lấy thông tin môn học cụ thể:")
    try:
        response = requests.get(f"{BASE_URL}/subjects/{subject_id}")
        if response.status_code == 200:
            subject = response.json()
            print(f"✅ Thành công! Thông tin môn học:")
            print(f"   - ID: {subject['id']}")
            print(f"   - Tên: {subject['name']}")
            print(f"   - Mã: {subject['code']}")
            print(f"   - Mô tả: {subject['description']}")
        else:
            print(f"❌ Lỗi lấy thông tin: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
    
    # Test 5: Xóa môn học (tùy chọn)
    print("\n5. Xóa môn học (tùy chọn):")
    choice = input("Bạn có muốn xóa môn học vừa tạo không? (y/n): ")
    if choice.lower() == 'y':
        try:
            response = requests.delete(f"{BASE_URL}/subjects/{subject_id}")
            if response.status_code == 200:
                print(f"✅ Thành công! Đã xóa môn học ID {subject_id}")
            else:
                print(f"❌ Lỗi xóa: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")
    else:
        print("⏭️ Bỏ qua việc xóa môn học")
    
    # Test 6: Kiểm tra danh sách cuối cùng
    print("\n6. Danh sách môn học sau khi test:")
    try:
        response = requests.get(f"{BASE_URL}/subjects/")
        if response.status_code == 200:
            subjects = response.json()
            print(f"✅ Có {len(subjects)} môn học:")
            for subject in subjects:
                print(f"   - ID: {subject['id']}, Tên: {subject['name']}, Mã: {subject.get('code', 'N/A')}")
        else:
            print(f"❌ Lỗi: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    test_subject_management() 