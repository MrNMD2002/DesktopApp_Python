# Cấu hình hiệu suất cho ứng dụng Exam Bank

# Database Configuration
DB_POOL_SIZE = 20
DB_CACHE_TIMEOUT = 60  # seconds
DB_PRE_PING = True
DB_AUTOCOMMIT = True

# API Configuration
API_TIMEOUT = 5  # seconds
API_CACHE_TIMEOUT = 30  # seconds
API_POOL_CONNECTIONS = 20
API_POOL_MAXSIZE = 50

# GUI Configuration
GUI_LAZY_LOADING = True
GUI_BATCH_SIZE = 50  # Số lượng item load mỗi lần

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_PERFORMANCE = True

# Cache Configuration
ENABLE_CACHE = True
CACHE_MAX_SIZE = 1000  # Số lượng cache entries tối đa

# Performance Monitoring
ENABLE_PERFORMANCE_MONITORING = True
PERFORMANCE_LOG_INTERVAL = 60  # seconds 