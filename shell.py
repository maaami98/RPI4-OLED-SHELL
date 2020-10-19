#!/bin/python
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
font_size=9
font_name='./fonts/kkberkbm.ttf'
# Load  font.
font = ImageFont.truetype(font=font_name, size=font_size, index=0, encoding='utf-8')
 

from pynput.keyboard import Listener, Key

screen_Text=[]
screen_Text.append('# ')
def keyPressed(key):
    
    
    try:
        if key==Key.space:
            screen_Text.append(' ')
        screen_Text.append(key.char)
        print (type(screen_Text))
        draw.text((x, top), ''.join(screen_Text),  font=font, fill=255)
        draw.text((x, top+10), "Linux raspi 5.4.51-v7l+ #1333 SMP Mon Aug 10 16:51:40 BST 2020 armv7l GNU/Linux",  font=font, fill=255)
        
        disp.image(image)
        disp.display()
        time.sleep(.1)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

with Listener(on_press=keyPressed) as l:
    l.join()