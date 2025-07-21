#!/usr/bin/env python3
"""
Script khởi động API với cấu hình tối ưu hiệu suất
"""
import uvicorn
import multiprocessing

if __name__ == "__main__":
    # Cấu hình tối ưu cho production
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8200,
        reload=True,
        access_log=True,
        log_level="info",
        timeout_keep_alive=30,
        limit_concurrency=1000,  # Giới hạn số connection đồng thời
        limit_max_requests=1000,  # Restart worker sau 1000 requests
        backlog=2048,  # Tăng backlog cho socket
    ) 