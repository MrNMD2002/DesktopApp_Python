import os
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8200")

# Tạo session với connection pooling và retry strategy
session = requests.Session()

# Cấu hình retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504],
)

# Cấu hình adapter với connection pooling tối ưu
adapter = HTTPAdapter(
    max_retries=retry_strategy,
    pool_connections=20,  # Tăng số lượng connection pool
    pool_maxsize=50,      # Tăng max size
    pool_block=False      # Không block khi hết connection
)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Cache cho các request thường xuyên
_cache = {}
_cache_timeout = 30  # Tăng lên 30 giây

def _get_cache_key(endpoint, **kwargs):
    """Tạo cache key từ endpoint và parameters"""
    return f"{endpoint}:{hash(str(kwargs))}"

def _is_cache_valid(cache_key):
    """Kiểm tra cache có còn hợp lệ không"""
    if cache_key in _cache:
        timestamp, _ = _cache[cache_key]
        return time.time() - timestamp < _cache_timeout
    return False

def get(endpoint, use_cache=True, **kwargs):
    """GET request với caching"""
    if use_cache:
        cache_key = _get_cache_key(endpoint, **kwargs)
        if _is_cache_valid(cache_key):
            return _cache[cache_key][1]
    
    url = f"{API_BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        resp = session.get(url, timeout=5, **kwargs)  # Giảm timeout
        resp.raise_for_status()
        result = resp.json()
        
        # Cache kết quả
        if use_cache:
            cache_key = _get_cache_key(endpoint, **kwargs)
            _cache[cache_key] = (time.time(), result)
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"API Error ({endpoint}): {e}")
        raise

def post(endpoint, json=None, **kwargs):
    """POST request"""
    url = f"{API_BASE_URL}{endpoint}"
    start_time = time.time()
    
    try:
        resp = session.post(url, json=json, timeout=5, **kwargs)  # Giảm timeout
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error ({endpoint}): {e}")
        raise

def put(endpoint, json=None, **kwargs):
    """PUT request"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        resp = session.put(url, json=json, timeout=5, **kwargs)  # Giảm timeout
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error ({endpoint}): {e}")
        raise

def patch(endpoint, json=None, **kwargs):
    """PATCH request"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        resp = session.patch(url, json=json, timeout=5, **kwargs)  # Giảm timeout
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error ({endpoint}): {e}")
        raise

def delete(endpoint, **kwargs):
    """DELETE request"""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        resp = session.delete(url, timeout=5, **kwargs)  # Giảm timeout
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error ({endpoint}): {e}")
        raise

def clear_cache():
    """Xóa cache"""
    global _cache
    _cache.clear()
    print("Cache đã được xóa thành công")

def get_cache_stats():
    """Lấy thống kê cache"""
    return {
        'size': len(_cache),
        'keys': list(_cache.keys())
    } 