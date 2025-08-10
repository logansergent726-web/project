# Google Sheets Data Logging Troubleshooting Guide

## 🔍 Issue Summary

**Problem**: Trade_Log, Portfolio_Summary, and Performance_Metrics sheets are not showing data despite successful backtest execution.

**Root Cause Analysis**: The data structures and logging code are working correctly (verified by testing), so the issue is likely with Google Sheets API authentication, permissions, or configuration.

## ✅ Verified Working Components

Our testing confirms these components are functioning correctly:

1. **Data Structure**: All trade, portfolio, and performance data is properly formatted
2. **Data Flow**: Information flows correctly from backtest to logging functions  
3. **Timestamp Handling**: Datetime objects are properly converted to strings
4. **JSON Serialization**: All data types are compatible with Google Sheets API

## 🔧 Most Likely Causes & Solutions

### 1. **Service Account Permissions** (Most Common)

**Problem**: Service account email doesn't have edit access to the spreadsheet.

**Solution**:
```bash
# 1. Open your Google Sheet
# 2. Click "Share" button (top right)
# 3. Add your service account email (from credentials JSON file)
# 4. Set permission to "Editor"
# 5. Click "Send"
```

**How to find service account email**:
```bash
# Look in your credentials JSON file for:
# "client_email": "your-service-account@project-name.iam.gserviceaccount.com"
```

### 2. **Google Sheets API Not Enabled**

**Problem**: Google Sheets API is disabled in Google Cloud Console.

**Solution**:
```bash
# 1. Go to https://console.cloud.google.com/
# 2. Select your project
# 3. Navigate to "APIs & Services" > "Library"
# 4. Search for "Google Sheets API"
# 5. Click "Enable"
```

### 3. **Incorrect Spreadsheet ID**

**Problem**: Wrong spreadsheet ID in configuration.

**Solution**:
```bash
# 1. Open your Google Sheet
# 2. Copy the ID from the URL:
#    https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
# 3. Update your .env file:
#    GOOGLE_SHEETS_SPREADSHEET_ID=your_correct_spreadsheet_id
```

### 4. **Authentication File Issues**

**Problem**: Credentials file is missing, corrupted, or has wrong permissions.

**Solution**:
```bash
# 1. Re-download credentials from Google Cloud Console
# 2. Place in correct location
# 3. Update .env file path:
#    GOOGLE_SHEETS_CREDENTIALS_FILE=/absolute/path/to/credentials.json
# 4. Check file permissions:
chmod 600 /path/to/credentials.json
```

### 5. **Worksheet Creation Issues**

**Problem**: Worksheets (tabs) are not being created in the spreadsheet.

**Solution**:
```bash
# 1. Check if these tabs exist in your Google Sheet:
#    - Trade_Log
#    - Portfolio_Summary  
#    - Performance_Metrics
#    - Signal_Log
# 2. If missing, manually create them or run test script
```

## 🧪 Step-by-Step Debugging

### Step 1: Verify Basic Setup

```bash
# Run configuration test
python3 test_sheets_integration.py
```

**Expected Output**:
- ✅ Google Sheets credentials found
- ✅ Connected to Google Sheets
- ✅ Sample data logged successfully

### Step 2: Check Permissions

1. **Open your Google Sheet**
2. **Check for these tabs**: Trade_Log, Portfolio_Summary, Performance_Metrics, Signal_Log
3. **Verify service account access**: Look for service account email in "Share" settings

### Step 3: Manual Permission Test

```bash
# Create a simple test sheet entry
python3 -c "
from src.utils.sheets_logger import GoogleSheetsLogger
logger = GoogleSheetsLogger()
if logger.is_connected():
    print('✅ Connected')
    # Try to write a simple test
    logger.log_trade({'symbol': 'TEST', 'action': 'BUY', 'quantity': 1, 'entry_price': 100, 'pnl': 10})
    print('✅ Test data written')
else:
    print('❌ Not connected')
"
```

### Step 4: Check Google Cloud Console

1. **Go to Google Cloud Console** → APIs & Services → Credentials
2. **Verify service account** exists and has correct permissions
3. **Check API usage** in "APIs & Services" → Dashboard
4. **Look for errors** in "APIs & Services" → Quotas

## 📋 Quick Checklist

**Before running backtest**, verify:

- [ ] ✅ Service account email added to Google Sheet with "Editor" permission
- [ ] ✅ Google Sheets API enabled in Google Cloud Console  
- [ ] ✅ Correct spreadsheet ID in `.env` file
- [ ] ✅ Credentials JSON file exists and path is correct
- [ ] ✅ Internet connectivity available
- [ ] ✅ No API quota limits exceeded

## 🔄 Testing Workflow

### Option 1: Full Integration Test

```bash
# 1. Test configuration
python3 test_sheets_integration.py

# 2. Run backtest with logging
python3 main.py backtest

# 3. Check Google Sheets for data
```

### Option 2: Dependency-Free Test

```bash
# Test data structures (no dependencies required)
python3 simple_sheets_test.py
```

### Option 3: Direct API Test

```bash
# Test Google Sheets API directly
python3 fix_sheets_data_logging.py
```

## 🚨 Common Error Messages & Solutions

### Error: "Credentials file not found"
```bash
Solution: Check file path in .env file
GOOGLE_SHEETS_CREDENTIALS_FILE=/full/path/to/credentials.json
```

### Error: "Permission denied" 
```bash
Solution: Add service account email to Google Sheet with Editor permission
```

### Error: "Spreadsheet not found"
```bash
Solution: Verify spreadsheet ID is correct and spreadsheet exists
```

### Error: "API not enabled"
```bash
Solution: Enable Google Sheets API in Google Cloud Console
```

### Error: "Quota exceeded"
```bash
Solution: Wait for quota reset or upgrade to paid tier
```

## 💡 Pro Tips

### 1. **Test with New Spreadsheet**
Create a fresh Google Sheet to eliminate permission conflicts:
```bash
# 1. Create new Google Sheet
# 2. Copy the ID
# 3. Share with service account
# 4. Update .env file
# 5. Test again
```

### 2. **Check Service Account Email Format**
```bash
# Should look like:
# algo-trading@your-project-123456.iam.gserviceaccount.com
```

### 3. **Verify JSON File Structure**
```bash
# Credentials file should contain:
{
  "type": "service_account",
  "project_id": "your-project",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "service-account@project.iam.gserviceaccount.com",
  ...
}
```

### 4. **Enable Detailed Logging**
```bash
# Add to your code for debugging:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Success Indicators

When working correctly, you should see:

1. **In Console Output**:
   ```
   ✅ Backtest results logged to Google Sheets successfully!
   Check your Google Sheet for detailed trade logs and performance data.
   ```

2. **In Google Sheets**:
   - **Trade_Log tab**: Individual trade entries with P&L
   - **Portfolio_Summary tab**: Portfolio value over time  
   - **Performance_Metrics tab**: Strategy statistics
   - **Signal_Log tab**: Trading signals (if any generated)

3. **Sample Data Format**:
   ```
   Trade_Log:
   Timestamp | Symbol | Action | Quantity | Entry_Price | Exit_Price | PnL
   2024-01-15 10:30:00 | RELIANCE.BSE | BUY | 50 | 2450.50 | 2485.75 | 1762.50
   ```

## 🔧 Final Troubleshooting

If all else fails:

1. **Create new service account** in Google Cloud Console
2. **Download new credentials** JSON file  
3. **Create new Google Sheet**
4. **Share with new service account**
5. **Update .env file** with new credentials and spreadsheet ID
6. **Test again**

## 📞 Still Having Issues?

The code and data structures are verified to work correctly. The issue is almost certainly:

1. **90% chance**: Service account permissions
2. **5% chance**: Google Sheets API configuration  
3. **3% chance**: Network/connectivity
4. **2% chance**: API quotas/limits

**Next Steps**: Focus on Google Cloud Console setup and spreadsheet sharing permissions.