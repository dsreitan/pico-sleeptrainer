"""
Font rendering for clock display
Simple 8x8 bitmap font for numbers and basic characters
"""

def draw_text_simple(lcd, text, x, y, color, scale=1, scale_y=None, mirrored=False):
    """Simple text drawing for clock (numbers and colon only)
    
    Args:
        lcd: LCD display object
        text: Text string to draw
        x, y: Starting position
        color: Text color
        scale: Horizontal scale factor
        scale_y: Vertical scale factor (if None, uses scale for both)
        mirrored: If True, mirrors text horizontally
    """
    if scale_y is None:
        scale_y = scale
    
    # Simple 8x8 font for digits
    font = {
        '0': [0x3E, 0x63, 0x73, 0x7B, 0x6F, 0x67, 0x63, 0x3E],
        '1': [0x18, 0x1C, 0x18, 0x18, 0x18, 0x18, 0x18, 0x7E],
        '2': [0x3E, 0x63, 0x60, 0x38, 0x0E, 0x03, 0x63, 0x7F],
        '3': [0x3E, 0x63, 0x60, 0x3C, 0x60, 0x60, 0x63, 0x3E],
        '4': [0x30, 0x38, 0x3C, 0x36, 0x33, 0x7F, 0x30, 0x30],
        '5': [0x7F, 0x03, 0x03, 0x3F, 0x60, 0x60, 0x63, 0x3E],
        '6': [0x3E, 0x63, 0x03, 0x3F, 0x63, 0x63, 0x63, 0x3E],
        '7': [0x7F, 0x63, 0x60, 0x30, 0x18, 0x0C, 0x0C, 0x0C],
        '8': [0x3E, 0x63, 0x63, 0x3E, 0x63, 0x63, 0x63, 0x3E],
        '9': [0x3E, 0x63, 0x63, 0x63, 0x7E, 0x60, 0x63, 0x3E],
        ':': [0x00, 0x00, 0x18, 0x18, 0x00, 0x18, 0x18, 0x00],
        '/': [0x00, 0x60, 0x30, 0x18, 0x0C, 0x06, 0x03, 0x00],
    }
    
    x_pos = x
    for char in text:
        if char in font:
            bitmap = font[char]
            for row in range(8):
                byte = bitmap[row]
                for col in range(8):
                    # Handle mirroring by reversing column
                    draw_col = (7 - col) if mirrored else col
                    if byte & (1 << (7 - col)):
                        if scale == 1 and scale_y == 1:
                            lcd.pixel(x_pos + draw_col, y + row, color)
                        else:
                            lcd.fill_rect(x_pos + draw_col * scale, y + row * scale_y, scale, scale_y, color)
        x_pos += (8 + 1) * scale

