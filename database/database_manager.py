import mysql.connector
from mysql.connector import Error, pooling
from config.database_config import DB_CONFIG
import logging
from typing import Optional, List, Any
import threading
import time

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_pool = None
            self.last_insert_id = None
            self.query_cache = {}
            self.cache_timeout = 60  # Tăng lên 60 giây
            self.initialize_pool()
            self.initialized = True
    
    def initialize_pool(self):
        """Khởi tạo connection pool"""
        try:
            pool_config = {
                'pool_name': 'exam_bank_pool',
                'pool_size': 20,  # Tăng pool size
                'pool_reset_session': True,
                **DB_CONFIG
            }
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(**pool_config)
            logging.info("Connection pool đã được khởi tạo thành công")
        except Error as e:
            logging.error(f"Lỗi khởi tạo connection pool: {e}")
            raise
    
    def get_connection(self):
        """Lấy connection từ pool"""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            logging.error(f"Lỗi lấy connection từ pool: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[tuple] = None, use_cache: bool = False) -> Any:
        """Thực thi câu lệnh SQL với caching và connection pooling"""
        # Kiểm tra cache cho SELECT queries
        if use_cache and query.strip().upper().startswith('SELECT'):
            cache_key = f"{query}:{hash(str(params))}"
            if self._is_cache_valid(cache_key):
                return self.query_cache[cache_key]['data']
        
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                result = cursor.fetchall()
                self.last_insert_id = None
                
                # Cache kết quả
                if use_cache:
                    cache_key = f"{query}:{hash(str(params))}"
                    self.query_cache[cache_key] = {
                        'data': result,
                        'timestamp': time.time()
                    }
            else:
                connection.commit()
                result = cursor.rowcount
                self.last_insert_id = cursor.lastrowid
            
            return result
        except Error as e:
            logging.error(f"Lỗi thực thi câu lệnh SQL: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Thực thi nhiều câu lệnh SQL cùng lúc với connection pooling"""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.executemany(query, params_list)
            connection.commit()
            rowcount = cursor.rowcount
            self.last_insert_id = cursor.lastrowid
            return rowcount
        except Error as e:
            logging.error(f"Lỗi thực thi nhiều câu lệnh SQL: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Kiểm tra cache có còn hợp lệ không"""
        if cache_key in self.query_cache:
            timestamp = self.query_cache[cache_key]['timestamp']
            return time.time() - timestamp < self.cache_timeout
        return False
    
    def clear_cache(self):
        """Xóa cache"""
        self.query_cache.clear()
    
    def get_cache_stats(self):
        """Lấy thống kê cache"""
        return {
            'size': len(self.query_cache),
            'keys': list(self.query_cache.keys())
        }
    
    def get_last_insert_id(self) -> Optional[int]:
        """Lấy ID của bản ghi vừa được thêm vào"""
        return self.last_insert_id
    
    def __del__(self):
        """Cleanup khi object bị hủy"""
        if hasattr(self, 'connection_pool') and self.connection_pool:
            self.connection_pool.close() 