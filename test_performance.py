#!/usr/bin/env python3
"""
Script test performance cho ứng dụng Exam Bank
"""
import time
import threading
import requests
from utils.performance_monitor import PerformanceMonitor
import json

def test_api_endpoints():
    """Test các API endpoints"""
    base_url = "http://localhost:8000"
    endpoints = [
        "/",
        "/subjects/",
        "/questions/",
        "/users/",
        "/exams/"
    ]
    
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    print("🚀 Bắt đầu test performance...")
    print(f"Base URL: {base_url}")
    
    # Test single requests
    print("\n📊 Test single requests:")
    for endpoint in endpoints:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            duration = time.time() - start_time
            
            status = "✅" if response.status_code == 200 else "❌"
            print(f"  {status} {endpoint}: {duration:.3f}s ({response.status_code})")
            
        except Exception as e:
            print(f"  ❌ {endpoint}: Error - {e}")
    
    # Test concurrent requests
    print("\n⚡ Test concurrent requests:")
    def make_request(endpoint):
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            duration = time.time() - start_time
            return endpoint, duration, response.status_code
        except Exception as e:
            return endpoint, 0, f"Error: {e}"
    
    # Test 10 concurrent requests
    threads = []
    results = []
    
    for i in range(10):
        endpoint = endpoints[i % len(endpoints)]
        thread = threading.Thread(target=lambda: results.append(make_request(endpoint)))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Tính toán thống kê
    successful_requests = [r for r in results if isinstance(r[2], int) and r[2] == 200]
    if successful_requests:
        avg_time = sum(r[1] for r in successful_requests) / len(successful_requests)
        min_time = min(r[1] for r in successful_requests)
        max_time = max(r[1] for r in successful_requests)
        
        print(f"  ✅ Successful requests: {len(successful_requests)}/10")
        print(f"  📈 Average time: {avg_time:.3f}s")
        print(f"  📉 Min time: {min_time:.3f}s")
        print(f"  📊 Max time: {max_time:.3f}s")
    
    # Test cache performance
    print("\n💾 Test cache performance:")
    cache_endpoints = ["/subjects/", "/questions/"]
    
    for endpoint in cache_endpoints:
        print(f"\n  Testing {endpoint}:")
        
        # First request (cache miss)
        start_time = time.time()
        response1 = requests.get(f"{base_url}{endpoint}", timeout=10)
        first_duration = time.time() - start_time
        
        # Second request (should be cached)
        start_time = time.time()
        response2 = requests.get(f"{base_url}{endpoint}", timeout=10)
        second_duration = time.time() - start_time
        
        improvement = ((first_duration - second_duration) / first_duration) * 100
        
        print(f"    First request: {first_duration:.3f}s")
        print(f"    Second request: {second_duration:.3f}s")
        print(f"    Improvement: {improvement:.1f}%")
    
    # Print performance summary
    print("\n" + "="*60)
    monitor.print_summary()
    
    # Get detailed stats
    stats = monitor.get_performance_stats()
    
    print("\n📋 Detailed Statistics:")
    print(f"  Total API calls: {stats['total_requests']}")
    print(f"  Cache hit rate: {stats['cache_stats']['hit_rate']:.2%}")
    print(f"  Cache hits: {stats['cache_stats']['hits']}")
    print(f"  Cache misses: {stats['cache_stats']['misses']}")
    
    if stats['system_stats']:
        print(f"  CPU usage: {stats['system_stats'].get('cpu_percent', 'N/A')}%")
        print(f"  Memory usage: {stats['system_stats'].get('memory_percent', 'N/A')}%")
    
    monitor.stop_monitoring()
    
    print("\n✅ Performance test completed!")

def test_database_performance():
    """Test database performance"""
    print("\n🗄️ Testing database performance...")
    
    try:
        from database.database_manager import DatabaseManager
        
        db = DatabaseManager()
        
        # Test basic queries
        print("  Testing basic queries:")
        
        start_time = time.time()
        subjects = db.execute_query("SELECT * FROM subjects", use_cache=True)
        first_query_time = time.time() - start_time
        
        start_time = time.time()
        subjects_cached = db.execute_query("SELECT * FROM subjects", use_cache=True)
        cached_query_time = time.time() - start_time
        
        print(f"    First query: {first_query_time:.3f}s")
        print(f"    Cached query: {cached_query_time:.3f}s")
        print(f"    Cache improvement: {((first_query_time - cached_query_time) / first_query_time * 100):.1f}%")
        
        # Test complex queries
        print("  Testing complex queries:")
        
        start_time = time.time()
        questions_with_subjects = db.execute_query("""
            SELECT q.*, s.name as subject_name 
            FROM questions q 
            JOIN subjects s ON q.subject_id = s.id 
            ORDER BY q.created_at DESC
        """, use_cache=True)
        complex_query_time = time.time() - start_time
        
        print(f"    Complex query: {complex_query_time:.3f}s")
        print(f"    Results: {len(questions_with_subjects)} records")
        
        # Get cache stats
        cache_stats = db.get_cache_stats()
        print(f"    Cache entries: {cache_stats['size']}")
        
    except Exception as e:
        print(f"  ❌ Database test error: {e}")

if __name__ == "__main__":
    print("🎯 Exam Bank Performance Test")
    print("="*60)
    
    # Test API performance
    test_api_endpoints()
    
    # Test database performance
    test_database_performance()
    
    print("\n🎉 All tests completed!") 