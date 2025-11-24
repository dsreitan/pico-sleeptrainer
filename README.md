# Pico Sleeptrainer

A digital clock application for Raspberry Pi Pico 2 W with Waveshare Pico-LCD-2 display.

## Features

- Large, easy-to-read time display (HH:MM format)
- Button-based time setting (no WiFi needed)
- Color-coded display (pink 07:00-11:00, black otherwise)
- Button support (pink background when any button pressed)

## Hardware Requirements

- Raspberry Pi Pico 2 W (or regular Pico)
- Waveshare Pico-LCD-2 display (240x320 ST7789 TFT LCD)

## Software Requirements

- MicroPython firmware for Raspberry Pi Pico 2 W
- Thonny IDE or any MicroPython-compatible IDE

## Project Files

- `clock_main.py` - Main application entry point
- `lcd_driver.py` - LCD display driver (ST7789)
- `clock_font.py` - Font rendering utilities
- `clock_buttons.py` - Button input handling
- `rtc_time.py` - RTC time functions

## Setup Instructions

### 1. Install MicroPython on Pico 2 W

1. Download the latest MicroPython firmware for Pico 2 W from [micropython.org](https://micropython.org/download/rp2-pico-w/)
2. Hold the BOOTSEL button on your Pico 2 W
3. Connect the Pico to your computer via USB (while holding BOOTSEL)
4. Release the BOOTSEL button
5. Copy the `.uf2` file to the Pico drive that appears (named "RPI-RP2" or similar)
6. The Pico will automatically reboot with MicroPython installed

### 2. Upload Project Files

Upload all project files to your Pico 2 W:
- `clock_main.py`
- `lcd_driver.py`
- `clock_font.py`
- `clock_buttons.py`
- `rtc_time.py`

### 3. Run the Clock

Run `clock_main.py` on your Pico 2 W. The clock will:
- Initialize the display
- Display the current time (updates every second)
- Allow time setting via buttons

**Tip:** Rename `clock_main.py` to `main.py` to automatically run the clock when the Pico boots up.

## Setting the Time

### Using Buttons

1. **Enter time setting mode:** Hold KEY0 (button 0) for 2 seconds
2. **Adjust hour:**
   - KEY1 (button 1): Increase hour
   - KEY2 (button 2): Decrease hour
   - KEY3 (button 3): Switch to minute editing (or cancel)
3. **Adjust minute:**
   - KEY1 (button 1): Increase minute
   - KEY2 (button 2): Decrease minute
   - KEY3 (button 3): Cancel
4. **Save:** Press KEY0 (button 0) to confirm and save

### Button Layout

- **KEY0 (button 0):** Enter time setting (hold 2s) / Confirm
- **KEY1 (button 1):** Increase value
- **KEY2 (button 2):** Decrease value
- **KEY3 (button 3):** Next field / Cancel

## Troubleshooting

**Display not working**
- Check all connections between Pico and LCD
- Verify pin assignments in `lcd_driver.py` match your hardware

**Time resets after power loss**
- This is normal - the RTC needs power to maintain time
- Set the time again after powering on using the button method above

**Buttons not working**
- Check button connections
- Verify pin assignments in `clock_buttons.py` match your hardware
- Buttons are active LOW (pressed = 0)

**Time setting mode not entering**
- Make sure to hold KEY0 for a full 2 seconds
- Release all buttons before trying again

## Resources

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Waveshare Pico-LCD-2 Wiki](https://www.waveshare.com/wiki/Pico-LCD-2)
- [Waveshare Pico LCD example code](https://github.com/waveshare/Pico_code/blob/main/Python/Pico-LCD-2/Pico-LCD-2.py)
