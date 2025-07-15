import mysql.connector
from mysql.connector import Error
from config.database_config import DB_CONFIG
import logging
from typing import Optional, List, Any

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.last_insert_id = None
        self.connect()
    
    def connect(self):
        """Kết nối đến cơ sở dữ liệu MySQL"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection and self.connection.is_connected():
                logging.info("Kết nối cơ sở dữ liệu thành công")
        except Error as e:
            logging.error(f"Lỗi kết nối cơ sở dữ liệu: {e}")
            raise
    
    def disconnect(self):
        """Ngắt kết nối cơ sở dữ liệu"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Đã ngắt kết nối cơ sở dữ liệu")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Any:
        """Thực thi câu lệnh SQL và trả về kết quả"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            if not self.connection:
                raise Error("Không thể kết nối đến cơ sở dữ liệu")
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                self.last_insert_id = None
            else:
                self.connection.commit()
                result = cursor.rowcount
                self.last_insert_id = cursor.lastrowid
            
            return result
        except Error as e:
            logging.error(f"Lỗi thực thi câu lệnh SQL: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Thực thi nhiều câu lệnh SQL cùng lúc"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            if not self.connection:
                raise Error("Không thể kết nối đến cơ sở dữ liệu")
            
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            rowcount = cursor.rowcount
            self.last_insert_id = cursor.lastrowid
            return rowcount
        except Error as e:
            logging.error(f"Lỗi thực thi nhiều câu lệnh SQL: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def get_last_insert_id(self) -> Optional[int]:
        """Lấy ID của bản ghi vừa được thêm vào"""
        return self.last_insert_id 