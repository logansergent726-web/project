#!/usr/bin/env python3
"""
Test script to verify Google Sheets integration and data logging functionality.
"""

import sys
from pathlib import Path
import os
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_config_status():
    """Test configuration status"""
    print("=" * 60)
    print("CONFIGURATION STATUS")
    print("=" * 60)
    
    try:
        from src.config import Config
        
        print("Environment Configuration:")
        print(f"   Alpha Vantage API Key: {'✅ SET' if Config.ALPHA_VANTAGE_API_KEY else '❌ MISSING'}")
        print(f"   Google Sheets Credentials: {Config.GOOGLE_SHEETS_CREDENTIALS_FILE}")
        print(f"   Google Sheets Spreadsheet ID: {Config.GOOGLE_SHEETS_SPREADSHEET_ID}")
        print(f"   Telegram Bot Token: {'✅ SET' if Config.TELEGRAM_BOT_TOKEN else '❌ MISSING'}")
        
        # Check file existence
        creds_exists = os.path.exists(Config.GOOGLE_SHEETS_CREDENTIALS_FILE) if Config.GOOGLE_SHEETS_CREDENTIALS_FILE else False
        print(f"   Credentials File Exists: {'✅ YES' if creds_exists else '❌ NO'}")
        
        if not Config.ALPHA_VANTAGE_API_KEY:
            print("\n⚠️  Alpha Vantage API key is required!")
            print("Get one free at: https://www.alphavantage.co/support/#api-key")
            
        return bool(Config.ALPHA_VANTAGE_API_KEY)
        
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def test_sheets_connection():
    """Test Google Sheets connection and setup"""
    print("\n" + "=" * 60)
    print("TESTING GOOGLE SHEETS INTEGRATION")
    print("=" * 60)
    
    # Check if credentials are configured
    from src.config import Config
    
    print("1. Checking Google Sheets configuration...")
    
    if not Config.GOOGLE_SHEETS_SPREADSHEET_ID:
        print("\n❌ Google Sheets spreadsheet ID not configured!")
        print("\nTo fix this:")
        print("1. Create a Google Service Account:")
        print("   - Go to https://console.cloud.google.com/")
        print("   - Create/select a project")
        print("   - Enable Google Sheets API")
        print("   - Create Service Account credentials")
        print("   - Download the JSON file")
        print("\n2. Create a Google Sheet:")
        print("   - Create a new Google Sheet")
        print("   - Share it with your service account email")
        print("   - Copy the spreadsheet ID from the URL")
        print("\n3. Create a .env file with:")
        print("   GOOGLE_SHEETS_CREDENTIALS_FILE=/path/to/your/credentials.json")
        print("   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id")
        return False
    
    if not Config.GOOGLE_SHEETS_CREDENTIALS_FILE or not os.path.exists(Config.GOOGLE_SHEETS_CREDENTIALS_FILE):
        print(f"\n❌ Credentials file not found: {Config.GOOGLE_SHEETS_CREDENTIALS_FILE}")
        print("\nMake sure the credentials file exists and the path in .env is correct.")
        return False
    
    # Test connection
    print("\n2. Testing Google Sheets connection...")
    try:
        from src.utils.sheets_logger import GoogleSheetsLogger
        
        sheets_logger = GoogleSheetsLogger()
        
        if sheets_logger.is_connected():
            print("✅ Successfully connected to Google Sheets!")
            
            # Get connection status
            status = sheets_logger.get_connection_status()
            print(f"   Spreadsheet ID: {status['spreadsheet_id']}")
            print(f"   Worksheets configured: {status['worksheets_configured']}/{status['expected_worksheets']}")
            
            # Test logging a sample trade
            print("\n3. Testing trade logging...")
            sample_trade = {
                'timestamp': datetime.now(),
                'symbol': 'TEST.BSE',
                'action': 'BUY',
                'quantity': 100,
                'entry_price': 150.50,
                'stop_loss': 145.00,
                'take_profit': 160.00,
                'rsi': 25.5,
                'sma_20': 148.75,
                'sma_50': 152.30,
                'signal_strength': 'STRONG'
            }
            
            try:
                sheets_logger.log_trade(sample_trade)
                print("✅ Sample trade logged successfully!")
                
                # Test signal logging
                print("\n4. Testing signal logging...")
                sample_signal = {
                    'symbol': 'TEST.BSE',
                    'signal': 'BUY',
                    'strength': 'STRONG',
                    'price': 150.50,
                    'rsi': 25.5,
                    'sma_20': 148.75,
                    'sma_50': 152.30,
                    'macd': 0.5,
                    'volume_ratio': 1.2,
                    'action_taken': 'EXECUTED'
                }
                
                ml_prediction = {
                    'prediction': 'UP',
                    'confidence': 0.75
                }
                
                sheets_logger.log_signal(sample_signal, ml_prediction)
                print("✅ Sample signal logged successfully!")
                
                # Test portfolio summary
                print("\n5. Testing portfolio summary...")
                sample_summary = {
                    'date': datetime.now(),
                    'total_capital': 105000.00,
                    'cash': 85000.00,
                    'positions_value': 20000.00,
                    'total_pnl': 5000.00,
                    'cumulative_return': 0.05,
                    'active_positions': 3,
                    'max_drawdown': -0.02,
                    'win_rate': 0.65
                }
                
                sheets_logger.update_portfolio_summary(sample_summary)
                print("✅ Portfolio summary updated successfully!")
                
                # Test performance metrics
                print("\n6. Testing performance metrics...")
                sample_metrics = {
                    'total_return': 0.05,
                    'annualized_return': 0.15,
                    'sharpe_ratio': 1.2,
                    'max_drawdown': -0.02,
                    'win_rate': 0.65,
                    'total_trades': 25
                }
                
                sheets_logger.update_performance_metrics(sample_metrics)
                print("✅ Performance metrics updated successfully!")
                
                print("\n" + "=" * 60)
                print("🎉 ALL GOOGLE SHEETS TESTS PASSED!")
                print("Your Google Sheet should now contain test data in these tabs:")
                print("   - Trade_Log: Sample trade entry")
                print("   - Portfolio_Summary: Sample portfolio data")
                print("   - Performance_Metrics: Sample performance data")
                print("   - Signal_Log: Sample signal entry")
                print("\nThe backtest will now log data to Google Sheets automatically.")
                print("=" * 60)
                return True
                
            except Exception as e:
                print(f"❌ Failed to log data: {e}")
                import traceback
                traceback.print_exc()
                return False
                
        else:
            print("❌ Failed to connect to Google Sheets")
            print("Check the following:")
            print("1. Service account credentials are valid")
            print("2. Google Sheets API is enabled")
            print("3. Spreadsheet is shared with service account email")
            print("4. Spreadsheet ID is correct")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install gspread google-auth")
        return False
    except Exception as e:
        print(f"❌ Error testing Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    try:
        print("🧪 Testing Algo-Trading System Components")
        print("This will verify that your setup is ready for the 6-month backtest.")
        
        # Test configuration
        config_ok = test_config_status()
        
        if not config_ok:
            print("\n⚠️  Configuration issues found.")
            print("Please fix the Alpha Vantage API configuration before running backtests.")
            return
        
        # Test Google Sheets (optional but recommended)
        sheets_ok = test_sheets_connection()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        if config_ok:
            print("✅ Core configuration is ready")
            print("✅ Can run backtest with console output")
            
        if sheets_ok:
            print("✅ Google Sheets integration is working")
            print("✅ Backtest results will be logged to Google Sheets")
        else:
            print("⚠️  Google Sheets integration not available")
            print("📝 Backtest results will be displayed in console only")
        
        print("\n🚀 Next steps:")
        print("   Run: python3 main.py backtest")
        print("   This will execute a 6-month backtest of the RSI+MA strategy")
        
        if sheets_ok:
            print("   Results will be automatically logged to your Google Sheet")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()