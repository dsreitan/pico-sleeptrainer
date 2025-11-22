"""
Button handling for Pico-LCD-2
The display has 4 buttons on GPIO 15, 17, 2, 3
"""

from machine import Pin

# Button pins from Waveshare example
KEY0_PIN = 15
KEY1_PIN = 17
KEY2_PIN = 2
KEY3_PIN = 3

class Buttons:
    """Handle button input for Pico-LCD-2"""
    
    def __init__(self):
        self.key0 = Pin(KEY0_PIN, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(KEY1_PIN, Pin.IN, Pin.PULL_UP)
        self.key2 = Pin(KEY2_PIN, Pin.IN, Pin.PULL_UP)
        self.key3 = Pin(KEY3_PIN, Pin.IN, Pin.PULL_UP)
    
    def any_pressed(self):
        """Check if any button is pressed (buttons are active LOW)"""
        return (self.key0.value() == 0 or 
                self.key1.value() == 0 or 
                self.key2.value() == 0 or 
                self.key3.value() == 0)
    
    def get_pressed(self):
        """Get list of pressed buttons"""
        pressed = []
        if self.key0.value() == 0:
            pressed.append(0)
        if self.key1.value() == 0:
            pressed.append(1)
        if self.key2.value() == 0:
            pressed.append(2)
        if self.key3.value() == 0:
            pressed.append(3)
        return pressed

