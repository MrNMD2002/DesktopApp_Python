import bcrypt
import logging
import datetime
import secrets
import string
from database.database_manager import DatabaseManager

class AuthManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None
    
    def login(self, username, password):
        """Đăng nhập người dùng"""
        try:
            # Kiểm tra username
            query = """
                SELECT * FROM users 
                WHERE username = %s AND is_active = 1
            """
            user = self.db.execute_query(query, (username,))
            
            if not user:
                return False, "Tài khoản không tồn tại hoặc đã bị khóa"
            
            user = user[0]
            
            # Kiểm tra mật khẩu
            if not self.verify_password(password, user['password_hash']):
                return False, "Mật khẩu không đúng"
            
            # Cập nhật thời gian đăng nhập cuối
            self.db.execute_query(
                "UPDATE users SET last_login = NOW() WHERE id = %s",
                (user['id'],)
            )
            
            # Lưu thông tin user hiện tại
            self.current_user = user
            
            logging.info(f"User {username} đăng nhập thành công")
            return True, "Đăng nhập thành công"
            
        except Exception as e:
            logging.error(f"Lỗi đăng nhập: {e}")
            return False, f"Lỗi đăng nhập: {str(e)}"
    
    def logout(self):
        """Đăng xuất"""
        if self.current_user:
            logging.info(f"User {self.current_user['username']} đăng xuất")
        self.current_user = None
    
    def get_current_user(self):
        """Lấy thông tin user hiện tại"""
        return self.current_user
    
    def verify_password(self, password, hashed):
        """Xác thực mật khẩu"""
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    
    def hash_password(self, password):
        """Mã hóa mật khẩu"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def change_password(self, user_id, old_password, new_password):
        """Đổi mật khẩu"""
        try:
            # Lấy mật khẩu hiện tại
            user = self.db.execute_query("SELECT password_hash FROM users WHERE id = %s", (user_id,))
            if not user:
                return False, "Người dùng không tồn tại"
            
            current_hash = user[0]['password_hash']
            
            # Kiểm tra mật khẩu cũ
            if not self.verify_password(old_password, current_hash):
                return False, "Mật khẩu cũ không đúng"
            
            # Mã hóa mật khẩu mới
            new_hash = self.hash_password(new_password)
            
            # Cập nhật mật khẩu
            self.db.execute_query(
                "UPDATE users SET password_hash = %s, updated_at = NOW() WHERE id = %s",
                (new_hash, user_id)
            )
            
            logging.info(f"User {user_id} đã đổi mật khẩu")
            return True, "Đổi mật khẩu thành công"
            
        except Exception as e:
            logging.error(f"Lỗi đổi mật khẩu: {e}")
            return False, f"Lỗi đổi mật khẩu: {str(e)}"
    
    def generate_reset_token(self, username):
        """Tạo token reset mật khẩu có ý nghĩa"""
        try:
            # Kiểm tra user tồn tại
            user = self.db.execute_query("SELECT id, username FROM users WHERE username = %s AND is_active = 1", (username,))
            if not user:
                return False, "Tài khoản không tồn tại hoặc đã bị khóa"
            
            user = user[0]
            
            # Tạo token có ý nghĩa: RESET-USERNAME-TIMESTAMP-RANDOM
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            token = f"RESET-{username}-{timestamp}-{random_part}"
            
            # Lưu token vào database
            self.db.execute_query(
                "UPDATE users SET reset_token = %s, reset_token_expires = DATE_ADD(NOW(), INTERVAL 1 HOUR) WHERE id = %s",
                (token, user['id'])
            )
            
            logging.info(f"Tạo token reset cho user {username}: {token}")
            return True, token
            
        except Exception as e:
            logging.error(f"Lỗi tạo token reset: {e}")
            return False, f"Lỗi tạo token: {str(e)}"
    
    def verify_reset_token(self, token):
        """Xác thực token reset"""
        try:
            # Kiểm tra token trong database
            user = self.db.execute_query(
                "SELECT id, username, reset_token_expires FROM users WHERE reset_token = %s AND is_active = 1",
                (token,)
            )
            
            if not user:
                return False, "Token không hợp lệ"
            
            user = user[0]
            
            # Kiểm tra token hết hạn
            if user['reset_token_expires'] < datetime.datetime.now():
                return False, "Token đã hết hạn"
            
            return True, user['username']
            
        except Exception as e:
            logging.error(f"Lỗi xác thực token: {e}")
            return False, f"Lỗi xác thực token: {str(e)}"
    
    def reset_password_with_token(self, token, new_password):
        """Reset mật khẩu bằng token"""
        try:
            # Xác thực token
            success, result = self.verify_reset_token(token)
            if not success:
                return False, result
            
            username = result
            
            # Mã hóa mật khẩu mới
            new_hash = self.hash_password(new_password)
            
            # Cập nhật mật khẩu và xóa token
            self.db.execute_query(
                "UPDATE users SET password_hash = %s, reset_token = NULL, reset_token_expires = NULL, updated_at = NOW() WHERE reset_token = %s",
                (new_hash, token)
            )
            
            logging.info(f"Reset mật khẩu thành công cho user {username}")
            return True, "Reset mật khẩu thành công"
            
        except Exception as e:
            logging.error(f"Lỗi reset mật khẩu: {e}")
            return False, f"Lỗi reset mật khẩu: {str(e)}"
    
    def decode_token_info(self, token):
        """Giải mã thông tin từ token"""
        try:
            if not token.startswith("RESET-"):
                return None
            
            parts = token.split("-")
            if len(parts) != 4:
                return None
            
            username = parts[1]
            timestamp = parts[2]
            random_part = parts[3]
            
            # Parse timestamp
            try:
                dt = datetime.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
                formatted_time = dt.strftime("%d/%m/%Y %H:%M:%S")
            except:
                formatted_time = "Không xác định"
            
            return {
                'username': username,
                'timestamp': formatted_time,
                'random_part': random_part,
                'is_valid': self.verify_reset_token(token)[0]
            }
            
        except Exception as e:
            logging.error(f"Lỗi giải mã token: {e}")
            return None
    
    def has_role(self, role):
        """Kiểm tra vai trò của người dùng"""
        if self.current_user:
            return self.current_user['role'] == role
        return False
    
    def is_authenticated(self):
        """Kiểm tra người dùng đã đăng nhập chưa"""
        return self.current_user is not None
    
    def is_admin(self):
        """Kiểm tra người dùng có phải admin không"""
        return self.has_role('admin') 