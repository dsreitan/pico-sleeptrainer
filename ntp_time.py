"""
NTP Time Synchronization for Raspberry Pi Pico 2 W
Synchronizes the RTC with NTP servers over WiFi
"""

import time
import network
from machine import RTC

def sync_time(ssid, password, timezone_offset=0):
    """
    Connect to WiFi and sync time with NTP server
    
    Args:
        ssid: WiFi network name
        password: WiFi password
        timezone_offset: Timezone offset in hours (e.g., -5 for EST, 0 for UTC)
    
    Returns:
        True if successful, False otherwise
    """
    # Initialize WiFi for Pico 2 W
    wlan = network.WLAN(network.STA_IF)
    
    # Deactivate first to ensure clean state
    if wlan.active():
        wlan.active(False)
        time.sleep(0.5)
    
    # Activate WiFi
    wlan.active(True)
    
    # Wait for WiFi to be ready (Pico 2 W needs time to initialize CYW43)
    time.sleep(1)
    
    # Check if WiFi is actually active
    if not wlan.active():
        print("Failed to activate WiFi")
        return False
    
    # Connect to WiFi
    print(f"Connecting to {ssid}...")
    try:
        wlan.connect(ssid, password)
    except OSError as e:
        print(f"WiFi connection error: {e}")
        # Try once more after a delay
        time.sleep(1)
        try:
            wlan.connect(ssid, password)
        except OSError as e2:
            print(f"WiFi connection failed: {e2}")
            return False
    
    # Wait for connection (max 15 seconds for Pico 2 W)
    max_wait = 15
    while max_wait > 0:
        status = wlan.status()
        if status < 0 or status >= 3:
            break
        max_wait -= 1
        print(f"Waiting for connection... ({max_wait}s remaining)")
        time.sleep(1)
    
    status = wlan.status()
    if status != 3:
        status_messages = {
            0: "Idle",
            1: "Connecting",
            2: "Wrong password",
            3: "Connected",
            -1: "Connection failed",
            -2: "No AP found",
            -3: "Connection timeout"
        }
        print(f"WiFi connection failed. Status: {status_messages.get(status, f'Unknown ({status})')}")
        return False
    
    print(f"Connected to {ssid}")
    print(f"IP address: {wlan.ifconfig()[0]}")
    
    # Sync time with NTP
    try:
        import ntptime
        # Set timezone offset
        ntptime.host = "pool.ntp.org"
        ntptime.settime()
        
        # Apply timezone offset
        if timezone_offset != 0:
            rtc = RTC()
            now = rtc.datetime()
            # Add timezone offset (in hours)
            # RTC datetime: (year, month, day, weekday, hour, minute, second, microsecond)
            new_hour = now[4] + timezone_offset
            new_minute = now[5]
            new_second = now[6]
            new_day = now[2]
            
            # Handle overflow/underflow
            if new_hour >= 24:
                new_day += new_hour // 24
                new_hour = new_hour % 24
            elif new_hour < 0:
                days_back = (-new_hour - 1) // 24 + 1
                new_day -= days_back
                new_hour += days_back * 24
            
            # Calculate weekday (simplified - assumes 7-day week)
            new_weekday = (now[3] + (new_day - now[2])) % 7
            
            rtc.datetime((now[0], now[1], new_day, new_weekday, new_hour, new_minute, new_second, now[7]))
        
        print("Time synchronized successfully")
        return True
        
    except Exception as e:
        print(f"Time sync failed: {e}")
        return False

def get_time_string():
    """Get current time as formatted string"""
    rtc = RTC()
    now = rtc.datetime()
    return f"{now[4]:02d}:{now[5]:02d}:{now[6]:02d}"

def get_date_string():
    """Get current date as formatted string"""
    rtc = RTC()
    now = rtc.datetime()
    # Format: YYYY/MM/DD
    return f"{now[0]}/{now[1]:02d}/{now[2]:02d}"

def get_datetime():
    """Get current datetime tuple"""
    rtc = RTC()
    return rtc.datetime()


