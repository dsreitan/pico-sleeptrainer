"""
Simple RTC time functions - no WiFi needed
"""
from machine import RTC

def get_datetime():
    """Get current datetime tuple from RTC"""
    rtc = RTC()
    return rtc.datetime()

def set_time(year, month, day, hour, minute, second=0, weekday=None):
    """Set RTC time"""
    rtc = RTC()
    if weekday is None:
        weekday = day % 7  # Simple approximation
    rtc.datetime((year, month, day, weekday, hour, minute, second, 0))
    return rtc.datetime()

def set_time_simple(hour, minute):
    """Set time (hour:minute) keeping current date"""
    rtc = RTC()
    now = rtc.datetime()
    rtc.datetime((now[0], now[1], now[2], now[3], hour, minute, 0, 0))
    return rtc.datetime()

