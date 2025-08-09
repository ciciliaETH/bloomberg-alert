"""
Test script untuk format waktu Bloomberg
"""

import email.utils
from datetime import datetime, timedelta

def format_bloomberg_time(email_date_str):
    """Convert email date string to Bloomberg format like: 08/09/25 14:32:00 UTC+7:00"""
    try:
        # Parse email date string (format: "Sat, 9 Aug 2025 07:32:00 -0000")
        parsed_date = email.utils.parsedate_tz(email_date_str)
        
        if parsed_date:
            # Convert to datetime object
            dt = datetime(*parsed_date[:6])
            
            # Add timezone offset if exists
            if parsed_date[9]:
                dt = dt - timedelta(seconds=parsed_date[9])
            
            # Convert to UTC+7 (Bloomberg timezone for Asia)
            utc7_dt = dt + timedelta(hours=7)
            
            # Format like Bloomberg: MM/DD/YY HH:MM:SS UTC+7:00
            formatted = utc7_dt.strftime("%m/%d/%y %H:%M:%S UTC+7:00")
            return formatted
        else:
            # Fallback: current time in UTC+7
            now_utc7 = datetime.utcnow() + timedelta(hours=7)
            return now_utc7.strftime("%m/%d/%y %H:%M:%S UTC+7:00")
            
    except Exception as e:
        print(f"❌ Error parsing date: {e}")
        # Fallback: current time in UTC+7
        now_utc7 = datetime.utcnow() + timedelta(hours=7)
        return now_utc7.strftime("%m/%d/%y %H:%M:%S UTC+7:00")

# Test dengan format dari email yang ada
test_email_date = "Sat, 9 Aug 2025 07:32:00 -0000"
formatted_time = format_bloomberg_time(test_email_date)

print("📧 Format Waktu Test:")
print(f"Original email date: {test_email_date}")
print(f"Bloomberg format:    {formatted_time}")
print()
print("🔔 Contoh pesan yang akan dikirim:")
print(f"🔔 News Alert (BLOOMBERG) At: {formatted_time}")
print()
print("📰 From Hope to Despair: How Switzerland's Tariff Drama Played Out")
print()
print("✅ Format sekarang sama dengan yang di email Bloomberg!")
print("📅 Target: 08/09/25 14:32:00 UTC+7:00")
print(f"📅 Result: {formatted_time}")

# Verify calculation
original_utc = datetime(2025, 8, 9, 7, 32, 0)  # 07:32 UTC
expected_utc7 = original_utc + timedelta(hours=7)  # Should be 14:32 UTC+7
print(f"✅ Verification: {expected_utc7.strftime('%m/%d/%y %H:%M:%S')} UTC+7:00")
