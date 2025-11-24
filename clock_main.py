"""
Pico Sleeptrainer - Main Application
Displays time on Waveshare Pico-LCD-2 display
Time can be set using buttons
"""
from machine import Pin, PWM
import time
from lcd_driver import LCD_2inch, BL
from clock_font import draw_text_simple
from clock_buttons import Buttons
from rtc_time import get_datetime, set_time_simple

# Button assignments for time setting:
# KEY0 (button 0): Enter time setting mode / Confirm
# KEY1 (button 1): Increase value
# KEY2 (button 2): Decrease value
# KEY3 (button 3): Next field / Cancel

def get_background_color(hour, buttons, lcd):
    """Determine background color based on time and button state"""
    # Check if any button is held (overrides time-based logic)
    if buttons.any_pressed():
        return lcd.PINK, lcd.WHITE  # Pink background, white text
    
    # Pink from 07:00 to 11:00
    if 7 <= hour < 11:
        return lcd.PINK, lcd.WHITE  # Pink background, white text
    else:
        return lcd.BLACK, lcd.DIM_GRAY  # Black background, dim gray text

def draw_clock(lcd, time_str, bg_color, text_color):
    """Draw the clock display"""
    # Fill screen with background color
    lcd.fill(bg_color)
    
    # Draw time (large and tall) - adjusted to fit within 320x240
    time_scale_x = 6  # Horizontal scale
    time_scale_y = 10  # Even taller vertical scale
    time_width = len(time_str) * (8 + 1) * time_scale_x
    time_x = (320 - time_width) // 2 + 7  # Move slightly to the right
    if time_x < 10:
        time_x = 10  # Ensure margin
    time_y = 70  # Centered vertically
    
    # Draw mirrored to fix orientation (since display is mirrored)
    draw_text_simple(lcd, time_str, time_x, time_y, text_color, 
                   scale=time_scale_x, scale_y=time_scale_y, mirrored=True)
    
    # Send to display
    lcd.show()

def draw_time_setting(lcd, hour, minute, editing_hour):
    """Draw time setting screen"""
    lcd.fill(lcd.BLACK)
    
    # Draw "SET TIME" at top
    draw_text_simple(lcd, "SET TIME", 50, 20, lcd.WHITE, scale=2, scale_y=3, mirrored=True)
    
    # Draw time with cursor
    time_str = f"{hour:02d}:{minute:02d}"
    time_scale_x = 5
    time_scale_y = 8
    time_width = len(time_str) * (8 + 1) * time_scale_x
    time_x = (320 - time_width) // 2
    time_y = 100
    
    # Draw hour (highlighted if editing)
    hour_color = lcd.PINK if editing_hour else lcd.WHITE
    draw_text_simple(lcd, f"{hour:02d}", time_x, time_y, hour_color, 
                   scale=time_scale_x, scale_y=time_scale_y, mirrored=True)
    
    # Draw colon
    colon_x = time_x + (8 + 1) * time_scale_x * 2
    draw_text_simple(lcd, ":", colon_x, time_y, lcd.WHITE, 
                   scale=time_scale_x, scale_y=time_scale_y, mirrored=True)
    
    # Draw minute (highlighted if editing)
    minute_x = colon_x + (8 + 1) * time_scale_x
    minute_color = lcd.PINK if not editing_hour else lcd.WHITE
    draw_text_simple(lcd, f"{minute:02d}", minute_x, time_y, minute_color, 
                   scale=time_scale_x, scale_y=time_scale_y, mirrored=True)
    
    # Draw instructions at bottom
    draw_text_simple(lcd, "B1:+ B2:- B3:Next B0:OK", 20, 200, lcd.DIM_GRAY, 
                   scale=1, scale_y=2, mirrored=True)
    
    lcd.show()

def wait_for_release(buttons):
    """Wait for all buttons to be released"""
    while buttons.any_pressed():
        time.sleep(0.1)

def set_time_with_buttons(lcd, buttons):
    """Set time using buttons"""
    # Get current time
    now = get_datetime()
    hour = now[4]
    minute = now[5]
    editing_hour = True
    
    print("Entering time setting mode...")
    draw_time_setting(lcd, hour, minute, editing_hour)
    wait_for_release(buttons)
    
    last_button_check = time.time()
    debounce_time = 0.2  # 200ms debounce
    
    while True:
        current_time = time.time()
        
        # Check buttons with debouncing
        if current_time - last_button_check >= debounce_time:
            pressed = buttons.get_pressed()
            
            if 1 in pressed:  # KEY1 - Increase
                if editing_hour:
                    hour = (hour + 1) % 24
                else:
                    minute = (minute + 1) % 60
                draw_time_setting(lcd, hour, minute, editing_hour)
                last_button_check = current_time
                wait_for_release(buttons)
                
            elif 2 in pressed:  # KEY2 - Decrease
                if editing_hour:
                    hour -= 1
                    if hour < 0:
                        hour = 23  # Wrap around to 23 when going below 0
                else:
                    minute -= 1
                    if minute < 0:
                        minute = 59  # Wrap around to 59 when going below 0
                draw_time_setting(lcd, hour, minute, editing_hour)
                last_button_check = current_time
                wait_for_release(buttons)
                
            elif 3 in pressed:  # KEY3 - Next field / Cancel
                if editing_hour:
                    editing_hour = False  # Switch to minute
                else:
                    # Cancel - exit without saving
                    print("Time setting cancelled")
                    return False
                draw_time_setting(lcd, hour, minute, editing_hour)
                last_button_check = current_time
                wait_for_release(buttons)
                
            elif 0 in pressed:  # KEY0 - Confirm
                if editing_hour:
                    editing_hour = False  # First press: switch to minute
                    draw_time_setting(lcd, hour, minute, editing_hour)
                    last_button_check = current_time
                    wait_for_release(buttons)
                else:
                    # Second press: confirm and save
                    set_time_simple(hour, minute)
                    print(f"Time set to {hour:02d}:{minute:02d}")
                    return True
        
        time.sleep(0.05)

def main():
    """Main clock application"""
    print("Initializing Pico Clock...")
    
    # Initialize backlight
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)  # 50% brightness
    
    # Power bank keep-alive: periodically pulse backlight to maintain power draw
    # This prevents power banks from auto-shutting off due to low current draw
    # Adjust these values if your power bank still shuts off:
    # - Decrease power_pulse_interval for more frequent pulses (e.g., 20.0)
    # - Increase power_pulse_brightness for higher power draw (max 65535)
    # - Increase power_pulse_duration for longer pulses (e.g., 0.2)
    last_power_pulse = time.time()
    power_pulse_interval = 30.0  # Pulse every 30 seconds
    power_pulse_duration = 0.1  # Pulse duration in seconds
    power_pulse_brightness = 49152  # 75% brightness for pulse (higher draw)
    
    # Initialize display
    lcd = LCD_2inch()
    print("Display initialized")
    
    # Initialize buttons
    buttons = Buttons()
    print("Buttons initialized")
    
    # Initialize RTC with default time if needed
    from machine import RTC
    rtc = RTC()
    if rtc.datetime()[0] <= 2021:
        rtc.datetime((2024, 1, 1, 0, 0, 0, 0, 0))
        print("RTC initialized with default time")
    
    # Clear screen
    lcd.fill(lcd.BLACK)
    lcd.show()
    
    print("Starting clock...")
    print("Hold KEY0 (button 0) for 2 seconds to enter time setting mode")
    
    last_second = -1
    time_setting_hold_start = None
    time_setting_hold_duration = 2.0  # Hold for 2 seconds
    
    try:
        while True:
            try:
                # Check for time setting mode (hold KEY0 for 2 seconds)
                if buttons.key0.value() == 0:  # KEY0 pressed
                    if time_setting_hold_start is None:
                        time_setting_hold_start = time.time()
                    elif time.time() - time_setting_hold_start >= time_setting_hold_duration:
                        # Enter time setting mode
                        if set_time_with_buttons(lcd, buttons):
                            # Time was set, continue with clock
                            pass
                        # Clear the hold timer
                        time_setting_hold_start = None
                        wait_for_release(buttons)
                else:
                    time_setting_hold_start = None
                
                # Power bank keep-alive: pulse backlight periodically
                current_time = time.time()
                if current_time - last_power_pulse >= power_pulse_interval:
                    # Brief pulse to higher brightness to increase power draw
                    pwm.duty_u16(power_pulse_brightness)
                    time.sleep(power_pulse_duration)
                    pwm.duty_u16(32768)  # Back to normal brightness
                    last_power_pulse = current_time
                
                # Normal clock display
                now = get_datetime()
                current_second = now[6]
                
                # Update only when second changes
                if current_second != last_second:
                    # Get time without seconds (HH:MM format)
                    time_str = f"{now[4]:02d}:{now[5]:02d}"
                    current_hour = now[4]
                    
                    # Get background and text colors
                    bg_color, text_color = get_background_color(current_hour, buttons, lcd)
                    
                    # Draw clock
                    draw_clock(lcd, time_str, bg_color, text_color)
                    
                    last_second = current_second
                    # Show full time with seconds in log
                    full_time = f"{now[4]:02d}:{now[5]:02d}:{now[6]:02d}"
                    bg_status = "PINK (button)" if buttons.any_pressed() else ("PINK (07:00-11:00)" if 7 <= current_hour < 11 else "BLACK")
                    print(f"Time: {full_time} | Display: {time_str} | BG: {bg_status}")
                
                # Sleep to prevent CPU spinning
                time.sleep(0.1)
                
            except Exception as e:
                # Catch any errors to prevent crash
                print(f"Error in loop: {e}")
                time.sleep(1)
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
