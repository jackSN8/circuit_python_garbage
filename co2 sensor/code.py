# SPDX-FileCopyrightText: 2020 by Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import math
import random

import board
import displayio
import terminalio
from adafruit_display_text import label
from fourwire import FourWire

from adafruit_st7789 import ST7789
import adafruit_scd4x

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""


# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D6

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

display = ST7789(display_bus, width=240, height=240, rowstart=80, bgr=True, invert=True)

# Setup the file as the bitmap data source

pick=random.randint(1,9)

bitmap = displayio.OnDiskBitmap(f"/{pick}.bmp")

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

# Create a Group to hold the TileGrid
group = displayio.Group()

# Add the TileGrid to the Group
group.append(tile_grid)


# Add the Group to the Display
display.root_group = group

# for i in range(1):
#     time.sleep(1)
#     pick=random.randint(1,7)
#     bitmap = displayio.OnDiskBitmap(f"/{pick}.bmp")
#     # Create a TileGrid to hold the bitmap
#     tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
#     # Create a Group to hold the TileGrid
#     group = displayio.Group()
#     # Add the TileGrid to the Group
#     group.append(tile_grid)
#     # Add the Group to the Display
#     display.root_group = group

# Loop forever so you can enjoy your image
while True:
    time.sleep(1)
    bitmap = displayio.OnDiskBitmap(f"6.bmp")
    # Create a TileGrid to hold the bitmap
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    # Create a Group to hold the TileGrid
    group = displayio.Group()
    # Add the TileGrid to the Group
    group.append(tile_grid)
    # Add the Group to the Display
    # display.root_group = group
    if scd4x.data_ready:
        text1 = f"CO2 {scd4x.CO2:.0f}ppm"
        
        text_area_1 = label.Label(terminalio.FONT, text=text1, color=0xFFFF00,scale=2)
        # Set the location
        text_area_1.x = 60
        text_area_1.y = 80
        text2=f"Temp {scd4x.temperature:.1f}C"
        text_area_2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00,scale=2)
        # Set the location
        text_area_2.x = 60
        text_area_2.y = 100
        text3=f"Humidity:{scd4x.relative_humidity:.1f}%"
        text_area_3 = label.Label(terminalio.FONT, text=text3, color=0xFFFF00,scale=2)
        # Set the location
        text_area_3.x = 60
        text_area_3.y = 120
        text4="Important information:"
        text_area_4 = label.Label(terminalio.FONT, text=text4, color=0x000000,scale=2)
        # Set the location
        text_area_4.x = 0
        text_area_4.y = 30
        
        group.append(text_area_1)
        group.append(text_area_2)
        group.append(text_area_3)
        group.append(text_area_4)

        # Show it
        display.root_group = group#,text_area_2
    time.sleep(3)

    pass