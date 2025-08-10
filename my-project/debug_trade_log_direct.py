#!/usr/bin/env python3
"""
Direct Trade_Log debugging script.
This will test exactly why Trade_Log sheet isn't receiving data.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import traceback

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_direct_trade_log():
    """Test Trade_Log specifically with minimal dependencies."""
    print("🎯 DIRECT TRADE_LOG DEBUG TEST")
    print("=" * 60)
    
    # Step 1: Test basic imports
    print("1️⃣ Testing imports...")
    try:
        from src.config import Config
        print("✅ Config imported")
        
        # Check configuration
        print(f"   Credentials file: {getattr(Config, 'GOOGLE_SHEETS_CREDENTIALS_FILE', 'NOT SET')}")
        print(f"   Spreadsheet ID: {getattr(Config, 'GOOGLE_SHEETS_SPREADSHEET_ID', 'NOT SET')}")
        
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    # Step 2: Test Google Sheets logger import
    print("\n2️⃣ Testing Google Sheets Logger import...")
    try:
        from src.utils.sheets_logger import GoogleSheetsLogger
        print("✅ GoogleSheetsLogger imported")
    except Exception as e:
        print(f"❌ GoogleSheetsLogger import failed: {e}")
        print("Trying mock logger...")
        try:
            from src.utils.mock_sheets_logger import MockGoogleSheetsLogger as GoogleSheetsLogger
            print("✅ Mock logger will be used")
        except Exception as e2:
            print(f"❌ Mock logger also failed: {e2}")
            return False
    
    # Step 3: Initialize logger
    print("\n3️⃣ Initializing logger...")
    try:
        logger = GoogleSheetsLogger()
        print("✅ Logger initialized")
        
        # Check connection
        if hasattr(logger, 'is_connected'):
            connected = logger.is_connected()
            print(f"   Connection status: {'✅ Connected' if connected else '❌ Not connected'}")
            if not connected:
                print("   ⚠️  Using mock mode or credentials not configured")
        
    except Exception as e:
        print(f"❌ Logger initialization failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 4: Test Trade_Log worksheet access
    print("\n4️⃣ Testing Trade_Log worksheet access...")
    try:
        if hasattr(logger, 'worksheets') and 'Trade_Log' in logger.worksheets:
            print("✅ Trade_Log worksheet found")
        elif hasattr(logger, 'spreadsheet') and logger.spreadsheet:
            print("   Checking spreadsheet for Trade_Log...")
            try:
                worksheet = logger.spreadsheet.worksheet('Trade_Log')
                print("✅ Trade_Log worksheet exists")
            except:
                print("❌ Trade_Log worksheet not found - creating...")
                # Attempt to create
                try:
                    headers = ['Timestamp', 'Symbol', 'Action', 'Quantity', 'Entry_Price', 
                             'Exit_Price', 'Entry_Date', 'Exit_Date', 'Exit_Reason', 'PnL']
                    worksheet = logger.spreadsheet.add_worksheet(title='Trade_Log', rows=1000, cols=len(headers))
                    worksheet.append_row(headers)
                    print("✅ Trade_Log worksheet created")
                except Exception as e:
                    print(f"❌ Failed to create Trade_Log: {e}")
        else:
            print("⚠️  Cannot access worksheets (mock mode or no connection)")
    
    except Exception as e:
        print(f"❌ Worksheet access failed: {e}")
        traceback.print_exc()
    
    # Step 5: Test direct data writing
    print("\n5️⃣ Testing direct Trade_Log data writing...")
    
    # Create super simple trade data
    simple_trade = {
        'timestamp': datetime.now(),
        'symbol': 'TEST.BSE',
        'action': 'BUY',
        'quantity': 10,
        'entry_price': 100.0,
        'exit_price': 105.0,
        'pnl': 50.0,
        'exit_reason': 'TEST'
    }
    
    print(f"   Test trade data: {simple_trade['symbol']} - P&L: ₹{simple_trade['pnl']}")
    
    try:
        result = logger.log_trade(simple_trade)
        print("✅ log_trade() completed")
        print(f"   Return value: {result}")
        
        # If real Google Sheets, try to read back
        if hasattr(logger, 'spreadsheet') and logger.spreadsheet and hasattr(logger, 'is_connected') and logger.is_connected():
            try:
                worksheet = logger.spreadsheet.worksheet('Trade_Log')
                all_values = worksheet.get_all_values()
                print(f"   Current Trade_Log rows: {len(all_values)}")
                if len(all_values) > 1:  # More than just headers
                    print(f"   Last row: {all_values[-1]}")
                else:
                    print("   ⚠️  Only headers found, no data rows")
            except Exception as e:
                print(f"   ❌ Failed to read back data: {e}")
        
    except Exception as e:
        print(f"❌ log_trade() failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 6: Test with exact backtest format
    print("\n6️⃣ Testing with exact backtest data format...")
    
    # Format exactly like main.py does
    backtest_trade = {
        'timestamp': datetime.now() - timedelta(days=1),
        'symbol': 'RELIANCE.BSE',
        'action': 'BUY',
        'quantity': 50,
        'entry_price': 2450.50,
        'exit_price': 2485.75,
        'entry_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
        'exit_date': datetime.now().strftime('%Y-%m-%d'),
        'exit_reason': 'RSI_OVERBOUGHT',
        'pnl': 1762.50,
        'stop_loss': 2350.0,
        'take_profit': 2550.0,
        'entry_timestamp': datetime.now() - timedelta(days=1),
        'exit_timestamp': datetime.now()
    }
    
    print(f"   Backtest format trade: {backtest_trade['symbol']} - P&L: ₹{backtest_trade['pnl']}")
    
    try:
        result = logger.log_trade(backtest_trade)
        print("✅ Backtest format log_trade() completed")
        
        # Check if data appeared
        if hasattr(logger, 'spreadsheet') and logger.spreadsheet and hasattr(logger, 'is_connected') and logger.is_connected():
            try:
                worksheet = logger.spreadsheet.worksheet('Trade_Log')
                all_values = worksheet.get_all_values()
                print(f"   Trade_Log rows after backtest format: {len(all_values)}")
                if len(all_values) > 1:
                    print(f"   Latest row: {all_values[-1]}")
                    
                    # Check if our test data is there
                    found_test_data = False
                    for row in all_values[1:]:  # Skip header
                        if 'RELIANCE.BSE' in str(row) or 'TEST.BSE' in str(row):
                            found_test_data = True
                            print(f"   ✅ Found test data in row: {row}")
                            break
                    
                    if not found_test_data:
                        print("   ❌ Test data not found in any rows")
                        print("   📋 Current sheet contents:")
                        for i, row in enumerate(all_values[:5]):  # Show first 5 rows
                            print(f"      Row {i}: {row}")
                else:
                    print("   ❌ Still only headers, no data rows")
            except Exception as e:
                print(f"   ❌ Failed to verify data: {e}")
    
    except Exception as e:
        print(f"❌ Backtest format failed: {e}")
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("🔍 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    return True

def manual_worksheet_test():
    """Test worksheet creation and access manually."""
    print("\n🛠️  MANUAL WORKSHEET TEST")
    print("=" * 60)
    
    try:
        from src.utils.sheets_logger import GoogleSheetsLogger
        logger = GoogleSheetsLogger()
        
        if not (hasattr(logger, 'is_connected') and logger.is_connected()):
            print("❌ Not connected to Google Sheets - cannot perform manual test")
            return False
        
        print("✅ Connected to Google Sheets")
        
        # Get spreadsheet
        spreadsheet = logger.spreadsheet
        print(f"📊 Spreadsheet title: {spreadsheet.title}")
        
        # List all worksheets
        worksheets = spreadsheet.worksheets()
        print(f"📋 Found {len(worksheets)} worksheets:")
        for ws in worksheets:
            print(f"   - {ws.title} ({ws.row_count} rows, {ws.col_count} cols)")
        
        # Focus on Trade_Log
        try:
            trade_log = spreadsheet.worksheet('Trade_Log')
            print(f"\n🎯 Trade_Log worksheet details:")
            print(f"   Rows: {trade_log.row_count}")
            print(f"   Columns: {trade_log.col_count}")
            
            # Get current content
            all_values = trade_log.get_all_values()
            print(f"   Current data rows: {len(all_values)}")
            
            if all_values:
                print(f"   Headers: {all_values[0]}")
                if len(all_values) > 1:
                    print(f"   Data rows: {len(all_values) - 1}")
                    for i, row in enumerate(all_values[1:6]):  # Show first 5 data rows
                        print(f"      Row {i+1}: {row}")
                else:
                    print("   ❌ No data rows (only headers)")
            
            # Try manual write
            print(f"\n✍️  Testing manual write...")
            test_row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'MANUAL_TEST.BSE',
                'BUY',
                100,
                200.50,
                205.75,
                '2024-01-01',
                '2024-01-02',
                'MANUAL_TEST',
                525.0,
                2.5,
                195.0,
                210.0,
                25.0,
                198.0,
                202.0,
                'STRONG',
                1
            ]
            
            trade_log.append_row(test_row)
            print("✅ Manual row added successfully")
            
            # Verify it was added
            updated_values = trade_log.get_all_values()
            print(f"   Updated row count: {len(updated_values)}")
            if len(updated_values) > len(all_values):
                print(f"   ✅ New row confirmed: {updated_values[-1]}")
            else:
                print(f"   ❌ Row count didn't increase")
                
        except Exception as e:
            print(f"❌ Trade_Log worksheet error: {e}")
            traceback.print_exc()
            return False
        
    except Exception as e:
        print(f"❌ Manual test failed: {e}")
        traceback.print_exc()
        return False
    
    return True

def main():
    """Run comprehensive Trade_Log debugging."""
    print("🚨 TRADE_LOG SPECIFIC DEBUGGING")
    print("This will identify exactly why Trade_Log isn't showing data.\n")
    
    # Test 1: Direct Trade_Log testing
    test1_result = test_direct_trade_log()
    
    # Test 2: Manual worksheet testing (only if connected)
    test2_result = manual_worksheet_test()
    
    print("\n" + "=" * 60)
    print("🎯 FINAL DIAGNOSIS")
    print("=" * 60)
    
    if test1_result and test2_result:
        print("✅ All tests passed - if you still don't see data:")
        print("\n🔧 IMMEDIATE ACTIONS:")
        print("1. Refresh your Google Sheet (Ctrl+R or Cmd+R)")
        print("2. Check if Trade_Log tab exists")
        print("3. Verify you're looking at the correct spreadsheet")
        print("4. Check if data is being written to a different sheet")
        
    else:
        print("❌ Issues found - see error messages above")
        print("\n🔧 NEXT STEPS:")
        print("1. Fix Google Sheets connection issues")
        print("2. Verify credentials and permissions")
        print("3. Check spreadsheet ID is correct")
    
    print("\n💡 PRO TIP:")
    print("If manual test worked but backtest didn't, the issue is in the backtest data formatting.")

if __name__ == "__main__":
    main()