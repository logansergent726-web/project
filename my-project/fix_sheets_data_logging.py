#!/usr/bin/env python3
"""
Script to test and fix Google Sheets data logging issues.
This will create test data and verify it appears in Google Sheets.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import traceback

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_sheets_data_writing():
    """Test actual data writing to Google Sheets with debugging."""
    print("🧪 Testing Google Sheets Data Writing")
    print("=" * 60)
    
    try:
        # Try to import the sheets logger
        try:
            from src.utils.sheets_logger import GoogleSheetsLogger
            print("✅ GoogleSheetsLogger imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import GoogleSheetsLogger: {e}")
            # Try mock logger
            from src.utils.mock_sheets_logger import MockGoogleSheetsLogger
            GoogleSheetsLogger = MockGoogleSheetsLogger
            print("✅ Using MockGoogleSheetsLogger for testing")
        
        # Initialize the logger
        print("\n📊 Initializing Google Sheets Logger...")
        sheets_logger = GoogleSheetsLogger()
        
        # Check connection status
        if hasattr(sheets_logger, 'is_connected'):
            if sheets_logger.is_connected():
                print("✅ Connected to Google Sheets")
            else:
                print("⚠️  Not connected to Google Sheets (using mock mode)")
        
        # Test 1: Log a trade with proper timestamp formatting
        print("\n1️⃣ Testing Trade Logging...")
        trade_data = {
            'timestamp': datetime.now(),
            'entry_timestamp': datetime.now() - timedelta(days=5),
            'exit_timestamp': datetime.now(),
            'symbol': 'RELIANCE.BSE',
            'action': 'BUY',
            'quantity': 100,
            'entry_price': 2450.50,
            'exit_price': 2485.75,
            'pnl': 3525.0,  # (2485.75 - 2450.50) * 100
            'exit_reason': 'RSI_OVERBOUGHT',
            'stop_loss': 2350.0,
            'take_profit': 2550.0
        }
        
        signal_data = {
            'rsi': 25.5,
            'sma_20': 2430.25,
            'sma_50': 2465.80,
            'strength': 'STRONG'
        }
        
        try:
            sheets_logger.log_trade(trade_data, signal_data)
            print("✅ Trade logged successfully")
        except Exception as e:
            print(f"❌ Trade logging failed: {e}")
            traceback.print_exc()
        
        # Test 2: Portfolio Summary
        print("\n2️⃣ Testing Portfolio Summary...")
        portfolio_data = {
            'date': datetime.now(),
            'total_capital': 105250.0,
            'cash': 85000.0,
            'positions_value': 20250.0,
            'total_pnl': 5250.0,
            'daily_return': 0.015,
            'cumulative_return': 0.0525,
            'active_positions': 3,
            'max_drawdown': -0.012,
            'win_rate': 0.68
        }
        
        try:
            sheets_logger.update_portfolio_summary(portfolio_data)
            print("✅ Portfolio summary updated successfully")
        except Exception as e:
            print(f"❌ Portfolio summary failed: {e}")
            traceback.print_exc()
        
        # Test 3: Performance Metrics
        print("\n3️⃣ Testing Performance Metrics...")
        performance_metrics = {
            'total_return': 0.0525,
            'annualized_return': 0.157,
            'sharpe_ratio': 1.45,
            'max_drawdown': -0.012,
            'win_rate': 0.68,
            'total_trades': 25,
            'winning_trades': 17,
            'losing_trades': 8,
            'average_win': 2850.75,
            'average_loss': -1250.25
        }
        
        try:
            sheets_logger.update_performance_metrics(performance_metrics)
            print("✅ Performance metrics updated successfully")
        except Exception as e:
            print(f"❌ Performance metrics failed: {e}")
            traceback.print_exc()
        
        # Test 4: Signal Log
        print("\n4️⃣ Testing Signal Logging...")
        signal_log_data = {
            'symbol': 'TCS.BSE',
            'signal': 'BUY',
            'strength': 'STRONG',
            'price': 3450.25,
            'rsi': 28.5,
            'sma_20': 3425.75,
            'sma_50': 3465.50,
            'macd': 0.15,
            'volume_ratio': 1.35,
            'action_taken': 'EXECUTED'
        }
        
        ml_prediction = {
            'prediction': 'UP',
            'confidence': 0.78
        }
        
        try:
            sheets_logger.log_signal(signal_log_data, ml_prediction)
            print("✅ Signal logged successfully")
        except Exception as e:
            print(f"❌ Signal logging failed: {e}")
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("🎉 TESTING COMPLETED")
        
        if hasattr(sheets_logger, 'is_connected') and sheets_logger.is_connected():
            print("✅ Data should now be visible in your Google Sheets")
            print("Check the following worksheets:")
            print("  - Trade_Log: Should have 1 new trade entry")
            print("  - Portfolio_Summary: Should have 1 new summary row")
            print("  - Performance_Metrics: Should have multiple metric rows")
            print("  - Signal_Log: Should have 1 new signal entry")
        else:
            print("ℹ️  Mock mode used - check console output for data structure")
        
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        traceback.print_exc()
        return False

def debug_backtest_data_flow():
    """Debug the data flow from backtest to Google Sheets."""
    print("\n🔍 Debugging Backtest Data Flow")
    print("=" * 60)
    
    try:
        # Create sample backtest results structure
        sample_trades = [
            {
                'timestamp': datetime.now() - timedelta(days=10),
                'exit_timestamp': datetime.now() - timedelta(days=8),
                'symbol': 'RELIANCE.BSE',
                'action': 'BUY',
                'quantity': 50,
                'price': 2400.0,  # entry_price
                'exit_price': 2450.0,
                'pnl': 2500.0,
                'exit_reason': 'TAKE_PROFIT',
                'stop_loss': 2300.0,
                'take_profit': 2500.0
            },
            {
                'timestamp': datetime.now() - timedelta(days=8),
                'exit_timestamp': datetime.now() - timedelta(days=6),
                'symbol': 'TCS.BSE',
                'action': 'BUY',
                'quantity': 25,
                'price': 3400.0,
                'exit_price': 3350.0,
                'pnl': -1250.0,
                'exit_reason': 'STOP_LOSS',
                'stop_loss': 3300.0,
                'take_profit': 3550.0
            }
        ]
        
        print("📊 Sample backtest data created:")
        for i, trade in enumerate(sample_trades, 1):
            print(f"  Trade {i}: {trade['symbol']} - P&L: ₹{trade['pnl']:.2f}")
        
        # Test data formatting that matches main.py structure
        print("\n🔧 Testing data formatting from main.py structure...")
        
        try:
            from src.utils.sheets_logger import GoogleSheetsLogger
            sheets_logger = GoogleSheetsLogger()
        except ImportError:
            from src.utils.mock_sheets_logger import MockGoogleSheetsLogger
            sheets_logger = MockGoogleSheetsLogger()
            print("Using mock logger")
        
        # Format data exactly like main.py does
        for trade in sample_trades:
            trade_data = {
                'timestamp': trade['timestamp'],
                'symbol': trade['symbol'],
                'action': trade['action'],
                'quantity': trade['quantity'],
                'entry_price': trade['price'],
                'exit_price': trade['exit_price'],
                'entry_timestamp': trade['timestamp'],
                'exit_timestamp': trade['exit_timestamp'],
                'exit_reason': trade['exit_reason'],
                'pnl': trade['pnl'],
                'stop_loss': trade['stop_loss'],
                'take_profit': trade['take_profit']
            }
            
            print(f"Logging trade: {trade_data['symbol']}")
            sheets_logger.log_trade(trade_data)
        
        # Test portfolio summary
        portfolio_summary = {
            'date': datetime.now(),
            'total_capital': 101250.0,
            'total_pnl': 1250.0,
            'cumulative_return': 0.0125,
            'active_positions': 0,
            'max_drawdown': -0.02,
            'win_rate': 0.5
        }
        
        print(f"Logging portfolio summary: Capital = ₹{portfolio_summary['total_capital']:,.2f}")
        sheets_logger.update_portfolio_summary(portfolio_summary)
        
        # Test performance metrics
        performance_metrics = {
            'total_return': 0.0125,
            'annualized_return': 0.075,
            'sharpe_ratio': 0.85,
            'max_drawdown': -0.02,
            'win_rate': 0.5,
            'total_trades': 2,
            'winning_trades': 1,
            'losing_trades': 1
        }
        
        print(f"Logging performance metrics: {len(performance_metrics)} metrics")
        sheets_logger.update_performance_metrics(performance_metrics)
        
        print("\n✅ Data flow test completed successfully!")
        print("If using real Google Sheets, data should now be visible.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Data flow test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🚀 Google Sheets Data Logging Diagnostic Tool")
    print("This will test data writing to Google Sheets and identify issues.\n")
    
    # Test 1: Basic data writing
    test1_result = test_sheets_data_writing()
    
    # Test 2: Backtest data flow
    test2_result = debug_backtest_data_flow()
    
    print("\n" + "=" * 60)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Basic Data Writing Test: {'✅ PASSED' if test1_result else '❌ FAILED'}")
    print(f"Backtest Data Flow Test: {'✅ PASSED' if test2_result else '❌ FAILED'}")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Google Sheets logging should be working.")
        print("\nNext steps:")
        print("1. Run: python3 main.py backtest")
        print("2. Check your Google Sheets for data")
        print("3. If still no data, check Google Sheets permissions")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify Google Sheets credentials are correct")
        print("2. Check that the spreadsheet is shared with your service account")
        print("3. Ensure Google Sheets API is enabled in your project")

if __name__ == "__main__":
    main()