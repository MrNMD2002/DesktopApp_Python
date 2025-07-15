import bcrypt
from database.database_manager import DatabaseManager
import logging

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def hash_password(self, password):
        """Mã hóa mật khẩu bằng bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)
    
    def verify_password(self, password, hashed):
        """Xác thực mật khẩu"""
        print("Password nhập:", password)
        print("Hash trong DB:", hashed)
        print("So sánh:", bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')))
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def login(self, username, password):
        """Đăng nhập người dùng"""
        try:
            query = "SELECT * FROM users WHERE username = %s"
            result = self.db.execute_query(query, (username,))
            
            if result and len(result) > 0:
                user = result[0]
                if self.verify_password(password, user['password_hash']):
                    self.current_user = user
                    logging.info(f"Đăng nhập thành công: {username}")
                    return True, "Đăng nhập thành công"
                else:
                    return False, "Mật khẩu không đúng"
            else:
                return False, "Tài khoản không tồn tại"
        except Exception as e:
            logging.error(f"Lỗi đăng nhập: {e}")
            return False, "Lỗi hệ thống"
    
    def logout(self):
        """Đăng xuất người dùng"""
        self.current_user = None
        logging.info("Đã đăng xuất")
    
    def get_current_user(self):
        """Lấy thông tin người dùng hiện tại"""
        return self.current_user
    
    def has_role(self, role):
        """Kiểm tra vai trò của người dùng"""
        if self.current_user:
            return self.current_user['role'] == role
        return False
    
    def is_authenticated(self):
        """Kiểm tra người dùng đã đăng nhập chưa"""
        return self.current_user is not None
    
    def create_user(self, username, password, full_name, role):
        """Tạo tài khoản mới"""
        try:
            # Kiểm tra username đã tồn tại chưa
            check_query = "SELECT id FROM users WHERE username = %s"
            existing = self.db.execute_query(check_query, (username,))
            
            if existing:
                return False, "Tên đăng nhập đã tồn tại"
            
            # Mã hóa mật khẩu
            password_hash = self.hash_password(password)
            
            # Thêm người dùng mới
            insert_query = """
                INSERT INTO users (username, password_hash, full_name, role)
                VALUES (%s, %s, %s, %s)
            """
            self.db.execute_query(insert_query, (username, password_hash.decode('utf-8'), full_name, role))
            
            logging.info(f"Tạo tài khoản thành công: {username}")
            return True, "Tạo tài khoản thành công"
        except Exception as e:
            logging.error(f"Lỗi tạo tài khoản: {e}")
            return False, "Lỗi hệ thống" 