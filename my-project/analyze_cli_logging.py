#!/usr/bin/env python3
"""
Comprehensive analysis of all CLI commands and their Google Sheets logging behavior.
This will identify which commands should log to Google Sheets and verify if they do.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def analyze_cli_commands():
    """Analyze all CLI commands and their expected logging behavior."""
    print("🔍 ANALYZING ALL CLI COMMANDS FOR GOOGLE SHEETS LOGGING")
    print("=" * 80)
    
    commands_analysis = {
        'config': {
            'description': 'Show configuration status',
            'expected_logging': False,
            'reason': 'Display only - no trades or signals generated',
            'sheets_interaction': 'None'
        },
        'test': {
            'description': 'Test API connections',
            'expected_logging': False,
            'reason': 'Testing only - no actual trading data generated',
            'sheets_interaction': 'Connection test only'
        },
        'backtest': {
            'description': 'Run strategy backtest for 6 months',
            'expected_logging': True,
            'reason': 'Generates trades, portfolio data, and performance metrics',
            'sheets_interaction': 'Trade_Log, Portfolio_Summary, Performance_Metrics'
        },
        'train-ml': {
            'description': 'Train ML prediction model',
            'expected_logging': False,
            'reason': 'Model training only - no trading data generated',
            'sheets_interaction': 'None (could log model metrics)'
        },
        'scan': {
            'description': 'Run single market scan',
            'expected_logging': True,
            'reason': 'Generates trading signals that should be logged',
            'sheets_interaction': 'Signal_Log'
        },
        'run': {
            'description': 'Start automated trading engine',
            'expected_logging': True,
            'reason': 'Continuous operation - generates signals and trades',
            'sheets_interaction': 'All sheets - Signal_Log, Trade_Log, Portfolio_Summary'
        }
    }
    
    print("📊 COMMAND ANALYSIS:")
    print("-" * 80)
    
    for command, info in commands_analysis.items():
        status = "🟢 SHOULD LOG" if info['expected_logging'] else "🔵 NO LOGGING"
        print(f"\n{command.upper()}: {status}")
        print(f"   Description: {info['description']}")
        print(f"   Logging Expected: {'Yes' if info['expected_logging'] else 'No'}")
        print(f"   Reason: {info['reason']}")
        print(f"   Sheets Interaction: {info['sheets_interaction']}")
    
    return commands_analysis

def create_test_commands():
    """Create test commands for each CLI function."""
    print("\n🧪 CREATING TEST COMMANDS")
    print("=" * 80)
    
    test_commands = {
        'config': {
            'command': 'python3 main.py config',
            'expected_output': 'Configuration display',
            'should_log': False,
            'verification': 'Check console output only'
        },
        'test': {
            'command': 'python3 main.py test',
            'expected_output': 'API connection status',
            'should_log': False,
            'verification': 'Check console output only'
        },
        'backtest': {
            'command': 'python3 main.py backtest',
            'expected_output': 'Backtest results + Google Sheets logging',
            'should_log': True,
            'verification': 'Check Trade_Log, Portfolio_Summary, Performance_Metrics tabs'
        },
        'train-ml': {
            'command': 'python3 main.py train-ml',
            'expected_output': 'ML model training results',
            'should_log': False,
            'verification': 'Check console output and models/ directory'
        },
        'scan': {
            'command': 'python3 main.py scan',
            'expected_output': 'Market scan results + signal logging',
            'should_log': True,
            'verification': 'Check Signal_Log tab for new entries'
        },
        'run': {
            'command': 'python3 main.py run',
            'expected_output': 'Continuous trading engine operation',
            'should_log': True,
            'verification': 'Check all sheets for ongoing logging'
        }
    }
    
    print("🔧 TEST COMMANDS TO RUN:")
    print("-" * 80)
    
    for command, info in test_commands.items():
        print(f"\n{command.upper()}:")
        print(f"   Command: {info['command']}")
        print(f"   Expected: {info['expected_output']}")
        print(f"   Should Log: {'Yes' if info['should_log'] else 'No'}")
        print(f"   Verification: {info['verification']}")
    
    return test_commands

def identify_logging_gaps():
    """Identify potential gaps in logging functionality."""
    print("\n🔍 IDENTIFYING POTENTIAL LOGGING GAPS")
    print("=" * 80)
    
    potential_gaps = {
        'train-ml': {
            'current_logging': 'None',
            'potential_improvement': 'Could log model training metrics',
            'suggestion': 'Add Performance_Metrics logging for model accuracy, training time'
        },
        'scan': {
            'current_logging': 'Signal_Log only',
            'potential_improvement': 'Complete signal logging implementation',
            'suggestion': 'Verify signals are actually being logged to Signal_Log'
        },
        'run': {
            'current_logging': 'Should log everything',
            'potential_improvement': 'Continuous operation logging',
            'suggestion': 'Verify real-time logging during automated trading'
        },
        'test': {
            'current_logging': 'None',
            'potential_improvement': 'Could log test results',
            'suggestion': 'Add test results to a separate log or Performance_Metrics'
        }
    }
    
    print("📋 POTENTIAL IMPROVEMENTS:")
    print("-" * 80)
    
    for command, info in potential_gaps.items():
        print(f"\n{command.upper()}:")
        print(f"   Current: {info['current_logging']}")
        print(f"   Potential: {info['potential_improvement']}")
        print(f"   Suggestion: {info['suggestion']}")

def create_logging_verification_script():
    """Create a script to verify logging for each command."""
    print("\n📝 CREATING LOGGING VERIFICATION SCRIPT")
    print("=" * 80)
    
    verification_script = """#!/usr/bin/env python3
# Logging Verification Script
# Run this after each command to check Google Sheets logging

import sys
from pathlib import Path
from datetime import datetime

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def check_sheets_after_command(command_name):
    \"\"\"Check Google Sheets for new data after running a command.\"\"\"
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
"""
    
    # Save the verification script
    with open('verify_logging.py', 'w') as f:
        f.write(verification_script)
    
    print("✅ Created 'verify_logging.py' - use this to check logging after each command")

def main():
    """Main analysis function."""
    print("🚀 CLI COMMANDS LOGGING ANALYSIS")
    print("This analyzes which commands should log to Google Sheets and how.\n")
    
    # Step 1: Analyze all commands
    commands_analysis = analyze_cli_commands()
    
    # Step 2: Create test commands
    test_commands = create_test_commands()
    
    # Step 3: Identify gaps
    identify_logging_gaps()
    
    # Step 4: Create verification script
    create_logging_verification_script()
    
    print("\n" + "=" * 80)
    print("📋 SUMMARY OF FINDINGS")
    print("=" * 80)
    
    logging_commands = [cmd for cmd, info in commands_analysis.items() if info['expected_logging']]
    non_logging_commands = [cmd for cmd, info in commands_analysis.items() if not info['expected_logging']]
    
    print(f"\n🟢 COMMANDS THAT SHOULD LOG TO GOOGLE SHEETS ({len(logging_commands)}):")
    for cmd in logging_commands:
        print(f"   - {cmd}: {commands_analysis[cmd]['sheets_interaction']}")
    
    print(f"\n🔵 COMMANDS THAT DON'T NEED LOGGING ({len(non_logging_commands)}):")
    for cmd in non_logging_commands:
        print(f"   - {cmd}: {commands_analysis[cmd]['reason']}")
    
    print(f"\n🔧 RECOMMENDED TESTING ORDER:")
    print("1. python3 main.py config    # Should show no logging")
    print("2. python3 main.py test      # Should test Google Sheets connection")
    print("3. python3 main.py scan      # Should log signals to Signal_Log")
    print("4. python3 main.py backtest  # Should log trades, portfolio, metrics")
    print("5. python3 main.py train-ml  # No logging expected")
    print("6. python3 main.py run       # Full logging (for testing only)")
    
    print(f"\n💡 AFTER EACH TEST:")
    print("   Run: python3 verify_logging.py")
    print("   Check your Google Sheets manually")
    print("   Look for console messages: '✅ Logged to Google Sheets'")

if __name__ == "__main__":
    main()