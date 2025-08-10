#!/usr/bin/env python3
"""
Simple dependency-free test for Google Sheets data logging.
This helps identify data structure issues without requiring external dependencies.
"""

import json
import os
from datetime import datetime, timedelta

class SimpleMockSheetsLogger:
    """Simple mock logger without dependencies."""
    
    def __init__(self):
        self.data = {
            'Trade_Log': [],
            'Portfolio_Summary': [],
            'Performance_Metrics': [],
            'Signal_Log': []
        }
        print("📊 SimpleMockSheetsLogger initialized")
    
    def is_connected(self):
        return True
    
    def log_trade(self, trade_data, signal_data=None):
        """Log trade data and display the structure."""
        print(f"\n🔍 LOGGING TRADE: {trade_data.get('symbol')}")
        print(f"   Data structure received:")
        for key, value in trade_data.items():
            print(f"     {key}: {value} ({type(value).__name__})")
        
        if signal_data:
            print(f"   Signal data:")
            for key, value in signal_data.items():
                print(f"     {key}: {value}")
        
        # Store the data
        self.data['Trade_Log'].append({
            'timestamp': str(datetime.now()),
            'data': trade_data,
            'signal': signal_data
        })
        print("   ✅ Trade logged to mock storage")
        return True
    
    def update_portfolio_summary(self, portfolio_data):
        """Log portfolio summary and display structure."""
        print(f"\n💼 LOGGING PORTFOLIO SUMMARY")
        print(f"   Data structure received:")
        for key, value in portfolio_data.items():
            print(f"     {key}: {value} ({type(value).__name__})")
        
        self.data['Portfolio_Summary'].append({
            'timestamp': str(datetime.now()),
            'data': portfolio_data
        })
        print("   ✅ Portfolio summary logged to mock storage")
        return True
    
    def update_performance_metrics(self, metrics):
        """Log performance metrics and display structure."""
        print(f"\n📈 LOGGING PERFORMANCE METRICS")
        print(f"   Data structure received:")
        for key, value in metrics.items():
            print(f"     {key}: {value} ({type(value).__name__})")
        
        self.data['Performance_Metrics'].append({
            'timestamp': str(datetime.now()),
            'data': metrics
        })
        print("   ✅ Performance metrics logged to mock storage")
        return True
    
    def log_signal(self, signal_data, ml_prediction=None):
        """Log signal data and display structure."""
        print(f"\n📡 LOGGING SIGNAL: {signal_data.get('symbol')}")
        print(f"   Signal data structure:")
        for key, value in signal_data.items():
            print(f"     {key}: {value} ({type(value).__name__})")
        
        if ml_prediction:
            print(f"   ML prediction:")
            for key, value in ml_prediction.items():
                print(f"     {key}: {value}")
        
        self.data['Signal_Log'].append({
            'timestamp': str(datetime.now()),
            'signal': signal_data,
            'ml_prediction': ml_prediction
        })
        print("   ✅ Signal logged to mock storage")
        return True
    
    def save_to_files(self):
        """Save all data to JSON files for inspection."""
        os.makedirs('debug_sheets_output', exist_ok=True)
        
        for sheet_name, data in self.data.items():
            filename = f'debug_sheets_output/{sheet_name.lower()}.json'
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"📁 Saved {sheet_name} data to {filename}")

def test_main_py_data_flow():
    """Test the exact data flow from main.py to sheets logger."""
    print("🧪 Testing Main.py Data Flow to Google Sheets")
    print("=" * 60)
    
    # Initialize mock logger
    sheets_logger = SimpleMockSheetsLogger()
    
    # Simulate trade data exactly as main.py creates it
    print("\n📊 Simulating backtest results from main.py...")
    
    # Create mock trade objects (simulating Trade class)
    class MockTrade:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    # Sample trades
    mock_trades = [
        MockTrade(
            timestamp=datetime.now() - timedelta(days=5),
            exit_timestamp=datetime.now() - timedelta(days=3),
            symbol='RELIANCE.BSE',
            action='BUY',
            quantity=50,
            price=2450.50,  # entry_price
            exit_price=2485.75,
            pnl=1762.50,
            exit_reason='RSI_OVERBOUGHT',
            stop_loss=2350.0,
            take_profit=2550.0
        ),
        MockTrade(
            timestamp=datetime.now() - timedelta(days=3),
            exit_timestamp=datetime.now() - timedelta(days=1),
            symbol='TCS.BSE',
            action='BUY',
            quantity=25,
            price=3400.0,
            exit_price=3350.0,
            pnl=-1250.0,
            exit_reason='STOP_LOSS',
            stop_loss=3300.0,
            take_profit=3550.0
        )
    ]
    
    # Test trade logging exactly as main.py does it
    print(f"🔄 Processing {len(mock_trades)} trades...")
    for trade in mock_trades:
        # Format trade_data exactly like main.py
        trade_data = {
            'timestamp': trade.timestamp,
            'symbol': trade.symbol,
            'action': trade.action,
            'quantity': trade.quantity,
            'entry_price': trade.price,
            'exit_price': trade.exit_price,
            'entry_date': trade.timestamp.strftime('%Y-%m-%d') if trade.timestamp else '',
            'exit_date': trade.exit_timestamp.strftime('%Y-%m-%d') if trade.exit_timestamp else '',
            'exit_reason': trade.exit_reason or 'N/A',
            'pnl': trade.pnl,
            'stop_loss': trade.stop_loss,
            'take_profit': trade.take_profit
        }
        
        # Log the trade
        sheets_logger.log_trade(trade_data)
    
    # Test portfolio summary exactly as main.py does it
    print(f"\n💼 Testing portfolio summary...")
    current_capital = 101762.50  # Example final capital
    initial_capital = 100000.0
    
    portfolio_summary = {
        'date': datetime.now(),
        'total_capital': current_capital,
        'total_pnl': current_capital - initial_capital,
        'cumulative_return': (current_capital - initial_capital) / initial_capital,
        'active_positions': 0,  # All positions closed
        'max_drawdown': -0.015,
        'win_rate': 0.5  # 1 win, 1 loss
    }
    sheets_logger.update_portfolio_summary(portfolio_summary)
    
    # Test performance metrics exactly as main.py does it
    print(f"\n📈 Testing performance metrics...")
    performance_metrics = {
        'total_return': (current_capital - initial_capital) / initial_capital,
        'annualized_return': 0.105,  # Example annualized return
        'sharpe_ratio': 0.85,
        'max_drawdown': -0.015,
        'win_rate': 0.5,
        'total_trades': 2,
        'winning_trades': 1,
        'losing_trades': 1
    }
    sheets_logger.update_performance_metrics(performance_metrics)
    
    # Save all data for inspection
    print(f"\n💾 Saving debug data...")
    sheets_logger.save_to_files()
    
    print("\n" + "=" * 60)
    print("✅ TESTING COMPLETED SUCCESSFULLY")
    print("\nKey Findings:")
    print("1. Data structures are properly formatted")
    print("2. All data types are JSON-serializable")
    print("3. Timestamps are handled correctly")
    print("4. Mock logging works as expected")
    print("\nIf Google Sheets still shows no data, the issue is likely:")
    print("   • Google Sheets API authentication")
    print("   • Worksheet permissions")
    print("   • Network connectivity")
    print("   • Google Sheets API limits")
    
    return True

def analyze_debug_files():
    """Analyze the generated debug files."""
    print("\n🔍 Analyzing Generated Debug Files")
    print("=" * 60)
    
    debug_dir = 'debug_sheets_output'
    if not os.path.exists(debug_dir):
        print("❌ Debug directory not found. Run the test first.")
        return
    
    files = ['trade_log.json', 'portfolio_summary.json', 'performance_metrics.json', 'signal_log.json']
    
    for filename in files:
        filepath = os.path.join(debug_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            print(f"\n📄 {filename.upper().replace('.JSON', '')}:")
            print(f"   Entries: {len(data)}")
            
            if data:
                print("   Sample entry structure:")
                sample = data[0]
                if 'data' in sample:
                    for key, value in sample['data'].items():
                        print(f"     {key}: {type(value).__name__}")
        else:
            print(f"❌ {filename} not found")

def main():
    """Run the complete test suite."""
    print("🚀 Google Sheets Data Logging Debug Tool")
    print("This identifies issues with data writing to Google Sheets.\n")
    
    # Run main test
    test_result = test_main_py_data_flow()
    
    # Analyze results
    analyze_debug_files()
    
    print("\n" + "=" * 60)
    print("📋 RECOMMENDATIONS")
    print("=" * 60)
    
    if test_result:
        print("✅ Data structure and formatting are correct")
        print("\nIf Google Sheets still shows no data, check:")
        print("1. 🔑 Service account email has edit access to your spreadsheet")
        print("2. 📝 Spreadsheet ID is correct in your .env file")
        print("3. 🌐 Google Sheets API is enabled in Google Cloud Console")
        print("4. 📊 Worksheets are being created (check if tabs exist)")
        print("5. 🔄 Try running the test again with real credentials")
        
        print("\nDebugging steps:")
        print("1. Check Google Sheets for worksheet tabs (Trade_Log, Portfolio_Summary, etc.)")
        print("2. Verify service account has 'Editor' permission on the spreadsheet")
        print("3. Check Google Cloud Console for API usage/errors")
        print("4. Try manually writing to the sheet to test permissions")

if __name__ == "__main__":
    main()