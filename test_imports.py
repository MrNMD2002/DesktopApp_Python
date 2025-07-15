#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

def test_imports():
    """Test all required imports"""
    try:
        print("Testing imports...")
        
        # Test bcrypt
        import bcrypt
        print("✓ bcrypt imported successfully")
        
        # Test mysql-connector
        import mysql.connector
        print("✓ mysql-connector imported successfully")
        
        # Test python-docx
        from docx import Document
        print("✓ python-docx imported successfully")
        
        # Test tkinter
        import tkinter as tk
        from tkinter import ttk, messagebox
        print("✓ tkinter imported successfully")
        
        # Test other standard libraries
        import logging
        import datetime
        import re
        import random
        print("✓ Standard libraries imported successfully")
        
        print("\nAll imports successful! The application should work correctly.")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 