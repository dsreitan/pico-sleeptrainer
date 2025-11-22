"""
Pico Sleeptrainer - Main Application
Displays time on Waveshare Pico-LCD-2 display
"""

from machine import Pin, PWM
import time
from lcd_driver import LCD_2inch, BL
from clock_font import draw_text_simple
from clock_buttons import Buttons
from ntp_time import sync_time, get_datetime

# Try to import config
try:
    from config import WIFI_SSID, WIFI_PASSWORD, TIMEZONE_OFFSET
except ImportError:
    WIFI_SSID = ""
    WIFI_PASSWORD = ""
    TIMEZONE_OFFSET = 0

def get_background_color(hour, buttons):
    """Determine background color based on time and button state"""
    # Check if any button is held (overrides time-based logic)
    if buttons.any_pressed():
        return LCD.PINK, LCD.WHITE  # Pink background, white text
    
    # Pink from 07:00 to 11:00
    if 7 <= hour < 11:
        return LCD.PINK, LCD.WHITE  # Pink background, white text
    else:
        return LCD.BLACK, LCD.DIM_GRAY  # Black background, dim gray text

def draw_clock(lcd, time_str, bg_color, text_color):
    """Draw the clock display"""
    # Fill screen with background color
    lcd.fill(bg_color)
    
    # Draw time (large and tall) - adjusted to fit within 320x240
    time_scale_x = 6  # Horizontal scale
    time_scale_y = 10  # Even taller vertical scale
    time_width = len(time_str) * (8 + 1) * time_scale_x
    time_x = (320 - time_width) // 2 + 7  # Move slightly to the right (halved)
    if time_x < 10:
        time_x = 10  # Ensure margin
    time_y = 70  # Centered vertically (adjusted for taller text)
    
    # Draw mirrored to fix orientation (since display is mirrored)
    draw_text_simple(lcd, time_str, time_x, time_y, text_color, 
                   scale=time_scale_x, scale_y=time_scale_y, mirrored=True)
    
    # Send to display (this is the key - all at once!)
    lcd.show()

def main():
    """Main clock application"""
    print("Initializing Pico Clock (Waveshare driver)...")
    
    # Initialize backlight
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # 50% brightness
    
    # Initialize display
    lcd = LCD_2inch()
    print("Display initialized")
    
    # Initialize buttons
    buttons = Buttons()
    print("Buttons initialized")
    
    # Clear screen
    lcd.fill(lcd.BLACK)
    lcd.show()
    
    # Sync time
    if WIFI_SSID and WIFI_PASSWORD:
        print("Syncing time with NTP...")
        if sync_time(WIFI_SSID, WIFI_PASSWORD, TIMEZONE_OFFSET):
            print("Time synchronized")
        else:
            print("Time sync failed, using default time")
            import machine
            rtc = machine.RTC()
            if rtc.datetime()[0] <= 2021:
                rtc.datetime((2024, 11, 22, 12, 0, 0, 0, 0))
    else:
        print("No WiFi, using default time")
        import machine
        rtc = machine.RTC()
        if rtc.datetime()[0] <= 2021:
            rtc.datetime((2024, 11, 22, 12, 0, 0, 0, 0))
    
    print("Starting clock...")
    last_second = -1
    
    try:
        while True:
            try:
                now = get_datetime()
                current_second = now[6]
                
                # Update only when second changes
                if current_second != last_second:
                    # Get time without seconds (HH:MM format)
                    time_str = f"{now[4]:02d}:{now[5]:02d}"
                    current_hour = now[4]
                    
                    # Get background and text colors
                    bg_color, text_color = get_background_color(current_hour, buttons)
                    
                    # Draw clock
                    draw_clock(lcd, time_str, bg_color, text_color)
                    
                    last_second = current_second
                    # Show full time with seconds in log
                    full_time = f"{now[4]:02d}:{now[5]:02d}:{now[6]:02d}"
                    bg_status = "PINK (button)" if buttons.any_pressed() else ("PINK (07:00-11:00)" if 7 <= current_hour < 11 else "BLACK")
                    print(f"Time: {full_time} | Display: {time_str} | BG: {bg_status}")
                
                # Sleep to prevent CPU spinning and allow serial communication
                time.sleep(0.1)
                
            except Exception as e:
                # Catch any errors to prevent crash and blocking
                print(f"Error in loop: {e}")
                time.sleep(1)  # Wait before retrying
                # Try to recover display
                try:
                    lcd.fill(lcd.BLACK)
                    lcd.show()
                except:
                    pass
            
    except KeyboardInterrupt:
        print("\nStopping...")
        try:
            lcd.fill(lcd.BLACK)
            lcd.show()
            print("Display cleared")
        except:
            print("Error clearing display")
    except Exception as e:
        print(f"Fatal error: {e}")
        try:
            lcd.fill(lcd.BLACK)
            lcd.show()
        except:
            pass

if __name__ == "__main__":
    main()

