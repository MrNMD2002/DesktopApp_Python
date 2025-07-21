#!/usr/bin/env python3
"""
Performance Monitor cho ứng dụng Exam Bank
"""
import time
import threading
import psutil
import logging
from typing import Dict, List, Any
from collections import defaultdict

class PerformanceMonitor:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(PerformanceMonitor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.request_times = defaultdict(list)
            self.api_calls = defaultdict(int)
            self.cache_hits = 0
            self.cache_misses = 0
            self.start_time = time.time()
            self.monitoring = False
            self.initialized = True
    
    def start_monitoring(self):
        """Bắt đầu monitoring"""
        self.monitoring = True
        logging.info("Performance monitoring đã được bật")
    
    def stop_monitoring(self):
        """Dừng monitoring"""
        self.monitoring = False
        logging.info("Performance monitoring đã được tắt")
    
    def record_request(self, endpoint: str, duration: float):
        """Ghi lại thời gian request"""
        if self.monitoring:
            self.request_times[endpoint].append(duration)
            self.api_calls[endpoint] += 1
    
    def record_cache_hit(self):
        """Ghi lại cache hit"""
        if self.monitoring:
            self.cache_hits += 1
    
    def record_cache_miss(self):
        """Ghi lại cache miss"""
        if self.monitoring:
            self.cache_misses += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Lấy thống kê performance"""
        stats = {
            'uptime': time.time() - self.start_time,
            'total_requests': sum(self.api_calls.values()),
            'cache_stats': {
                'hits': self.cache_hits,
                'misses': self.cache_misses,
                'hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses) if (self.cache_hits + self.cache_misses) > 0 else 0
            },
            'system_stats': self._get_system_stats(),
            'endpoint_stats': {}
        }
        
        # Thống kê theo endpoint
        for endpoint, times in self.request_times.items():
            if times:
                stats['endpoint_stats'][endpoint] = {
                    'count': len(times),
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_time': sum(times)
                }
        
        return stats
    
    def _get_system_stats(self) -> Dict[str, Any]:
        """Lấy thống kê hệ thống"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'disk_percent': disk.percent,
                'disk_free': disk.free
            }
        except Exception as e:
            logging.warning(f"Không thể lấy thống kê hệ thống: {e}")
            return {}
    
    def get_slowest_endpoints(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Lấy danh sách endpoint chậm nhất"""
        endpoint_stats = []
        
        for endpoint, times in self.request_times.items():
            if times:
                avg_time = sum(times) / len(times)
                endpoint_stats.append({
                    'endpoint': endpoint,
                    'avg_time': avg_time,
                    'count': len(times)
                })
        
        # Sắp xếp theo thời gian trung bình giảm dần
        endpoint_stats.sort(key=lambda x: x['avg_time'], reverse=True)
        return endpoint_stats[:limit]
    
    def clear_stats(self):
        """Xóa thống kê"""
        self.request_times.clear()
        self.api_calls.clear()
        self.cache_hits = 0
        self.cache_misses = 0
        self.start_time = time.time()
    
    def print_summary(self):
        """In tóm tắt performance"""
        stats = self.get_performance_stats()
        
        print("\n" + "="*50)
        print("PERFORMANCE SUMMARY")
        print("="*50)
        print(f"Uptime: {stats['uptime']:.2f} seconds")
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Cache Hit Rate: {stats['cache_stats']['hit_rate']:.2%}")
        print(f"CPU Usage: {stats['system_stats'].get('cpu_percent', 'N/A')}%")
        print(f"Memory Usage: {stats['system_stats'].get('memory_percent', 'N/A')}%")
        
        print("\nSlowest Endpoints:")
        slowest = self.get_slowest_endpoints(3)
        for i, endpoint in enumerate(slowest, 1):
            print(f"  {i}. {endpoint['endpoint']}: {endpoint['avg_time']:.3f}s ({endpoint['count']} calls)")
        print("="*50)

# Decorator để monitor function
def monitor_performance(func):
    """Decorator để monitor performance của function"""
    def wrapper(*args, **kwargs):
        monitor = PerformanceMonitor()
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            monitor.record_request(func.__name__, duration)
            return result
        except Exception as e:
            duration = time.time() - start_time
            monitor.record_request(f"{func.__name__}_error", duration)
            raise
    
    return wrapper 