# api/models/util.py
# Utility functions for model templates

from datetime import datetime

def timelog() -> str:
    """
    Return the current timestamp as a string in the format:
    'HH:MM:SS DD-MM-YYYY'.

    Example:
        '22:45:01 11-01-2026'
    """
    return datetime.now().strftime('%H:%M:%S %d-%m-%Y')
