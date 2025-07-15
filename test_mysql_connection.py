#!/usr/bin/env python3
"""
Test script to verify MySQL connection
"""

def test_mysql_connection():
    """Test MySQL connection"""
    try:
        print("Testing MySQL connection...")
        
        # Import required modules
        from database.database_manager import DatabaseManager
        from config.database_config import DB_CONFIG
        
        print(f"Database config: {DB_CONFIG}")
        
        # Test connection
        db = DatabaseManager()
        print("✓ DatabaseManager initialized successfully")
        
        # Test simple query
        result = db.execute_query("SELECT 1 as test")
        print(f"✓ Test query result: {result}")
        
        # Test database name
        result = db.execute_query("SELECT DATABASE() as current_db")
        print(f"✓ Current database: {result[0]['current_db']}")
        
        # Test if tables exist
        result = db.execute_query("SHOW TABLES")
        print(f"✓ Tables in database: {[row['Tables_in_exam_bank'] for row in result]}")
        
        # Test users table
        result = db.execute_query("SELECT COUNT(*) as user_count FROM users")
        print(f"✓ Users count: {result[0]['user_count']}")
        
        # Test subjects table
        result = db.execute_query("SELECT COUNT(*) as subject_count FROM subjects")
        print(f"✓ Subjects count: {result[0]['subject_count']}")
        
        print("\n✅ MySQL connection successful! All tests passed.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure MySQL server is running")
        print("2. Check database_config.py has correct credentials")
        print("3. Ensure 'exam_bank' database exists")
        print("4. Verify user has proper permissions")
        return False

if __name__ == "__main__":
    test_mysql_connection() 