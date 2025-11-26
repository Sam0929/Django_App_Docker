"""
Configuration for tests - conftest.py
This file helps with test setup and fixtures
"""
import os
import django
from django.conf import settings

def pytest_configure():
    """Configure Django settings for pytest"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
    
    if not settings.configured:
        django.setup()
