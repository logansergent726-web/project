#!/usr/bin/env python3
# Logging Verification Script
# Run this after each command to check Google Sheets logging

import sys
from pathlib import Path
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_sheets_after_command(command_name):
    """Check Google Sheets for new data after running a command."""
    print(f"🔍 Checking Google Sheets after '{command_name}' command...")
    
    try:
        from src.utils.sheets_logger import GoogleSheetsLogger
        logger = GoogleSheetsLogger()
        
        if not logger.is_connected():
            print("❌ Not connected to Google Sheets")
            return False
        
        # Get all worksheets
        spreadsheet = logger.spreadsheet
        worksheets = spreadsheet.worksheets()
        
        print(f"📊 Found {len(worksheets)} worksheets:")
        
        for ws in worksheets:
            if ws.title in ['Trade_Log', 'Portfolio_Summary', 'Performance_Metrics', 'Signal_Log']:
                all_values = ws.get_all_values()
                data_rows = len(all_values) - 1 if all_values else 0
                print(f"   {ws.title}: {data_rows} data rows")
                
                # Show recent entries if any
                if data_rows > 0:
                    recent_entries = all_values[-min(3, data_rows):]
                    print(f"     Recent entries:")
                    for entry in recent_entries:
                        timestamp = entry[0] if entry else "No timestamp"
                        print(f"       {timestamp}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking sheets: {e}")
        return False

# Usage examples:
# check_sheets_after_command('backtest')
# check_sheets_after_command('scan')
# check_sheets_after_command('run')
