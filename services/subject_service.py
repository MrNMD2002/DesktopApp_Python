from services.api_client import get, post, put, delete

def get_subjects():
    """Lấy danh sách môn học với cache"""
    return get("/subjects/", use_cache=True)

def get_subject_by_id(subject_id):
    """Lấy thông tin môn học theo ID với cache"""
    return get(f"/subjects/{subject_id}", use_cache=True)

def get_subject(subject_id):
    """Lấy thông tin môn học theo ID"""
    return get(f"/subjects/{subject_id}")

def create_subject(subject_data):
    """Tạo môn học mới"""
    return post("/subjects/", json=subject_data)

def update_subject(subject_id, subject_data):
    """Cập nhật thông tin môn học"""
    return put(f"/subjects/{subject_id}", json=subject_data)

def delete_subject(subject_id):
    """Xóa môn học"""
    return delete(f"/subjects/{subject_id}") 