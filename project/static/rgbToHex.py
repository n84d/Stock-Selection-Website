def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

# Example RGB values (R, G, B)
rgb_values = (200, 255, 205)
hex_value = rgb_to_hex(rgb_values)
print(hex_value)  # Output: #ff0080
