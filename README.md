# Pico Sleeptrainer

A digital clock application for Raspberry Pi Pico 2 W with Waveshare Pico-LCD-2 display.

## Features

- Large, easy-to-read time display (HH:MM format)
- WiFi time synchronization via NTP
- Automatic timezone adjustment
- Color-coded display (pink 07:00-11:00, black otherwise)
- Button support (pink background when any button pressed)

## Hardware Requirements

- Raspberry Pi Pico 2 W
- Waveshare Pico-LCD-2 display (240x320 ST7789 TFT LCD)

## Software Requirements

- MicroPython firmware for Raspberry Pi Pico 2 W
- Thonny IDE or any MicroPython-compatible IDE

## Project Files

- `clock_main.py` - Main application entry point
- `lcd_driver.py` - LCD display driver (ST7789)
- `clock_font.py` - Font rendering utilities
- `clock_buttons.py` - Button input handling
- `ntp_time.py` - NTP time synchronization
- `config.py` - WiFi and timezone configuration

## Setup Instructions

### 1. Install MicroPython on Pico 2 W

1. Download the latest MicroPython firmware for Pico 2 W from [micropython.org](https://micropython.org/download/rp2-pico-w/)
2. Hold the BOOTSEL button on your Pico 2 W
3. Connect the Pico to your computer via USB
4. Release the BOOTSEL button
5. Copy the `.uf2` file to the Pico drive that appears
6. The Pico will reboot with MicroPython installed

### 2. Upload Project Files

Upload all project files to your Pico 2 W:
- `clock_main.py`
- `lcd_driver.py`
- `clock_font.py`
- `clock_buttons.py`
- `ntp_time.py`
- `config.py`

### 3. Configure WiFi

Edit `config.py` and add your WiFi credentials:
```python
WIFI_SSID = "your_wifi_network"
WIFI_PASSWORD = "your_wifi_password"
TIMEZONE_OFFSET = -5  # Adjust for your timezone
```

### 4. Run the Clock

Run `clock_main.py` on your Pico 2 W. The clock will:
- Initialize the display
- Connect to WiFi (if configured)
- Sync time with NTP server
- Display the current time (updates every second)

**Tip:** Rename `clock_main.py` to `main.py` to automatically run the clock when the Pico boots up.

## Troubleshooting

**Display not working**
- Check all connections between Pico and LCD
- Verify pin assignments in `lcd_driver.py` match your hardware

**WiFi connection fails**
- Verify WiFi credentials in `config.py`
- Check that your WiFi network is 2.4 GHz (Pico 2 W doesn't support 5 GHz)
- Ensure you're within range of the WiFi network

**Time not syncing**
- Check WiFi connection status
- Verify internet connectivity
- Check timezone offset setting in `config.py`
- If NTP fails, the clock will use the default RTC time

## Resources

- [Raspberry Pi Pico Documentation](https://www.raspberrypi.com/documentation/microcontrollers/)
- [MicroPython Documentation](https://docs.micropython.org/)
- [Waveshare Pico-LCD-2 Wiki](https://www.waveshare.com/wiki/Pico-LCD-2)
- [Waveshare Pico LCD example code](https://github.com/waveshare/Pico_code/blob/main/Python/Pico-LCD-2/Pico-LCD-2.py)
