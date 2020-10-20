#!/bin/python


import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#Daha sonrasında systemctl ekleniceği için stdin üzerinden veri okumak yerine keyboard hit üzerinden almayı seçtim
from pynput.keyboard import Listener, Key

from subprocess import Popen, PIPE
import socket,threading,time


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
 

shellOut=[]

cursor_x=0
cursor_y=0
#shellden gelen veriyi oled ekrana basmak için
def shell2oled( p):
    global s
    while True:
        try:
            temp=p.stdout.read(1)
            print (temp) #print debug
            """
            #print oled
            
            draw.text((x, top), temp,  font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(.1)
            """
        except :
            return

# bash yerine sh' tercih ettim daha az print çıktısı sebebiyle

#bu satırda subprocess oluşturup onu thread üzerinde tutmakta
p=Popen(['sh'],shell=True, stdout=PIPE, stdin=PIPE,stderr=PIPE)
shell2oled_thread = threading.Thread(target=shell2oled, args=[p])
shell2oled_thread.start()
# shellden verileri okumak için ve yazmak için olarak 2 ayrı thread oluşturdum
#threadlere processi gönderiyorum
def keyPressed(key):
    
    try:
        
        if key==Key.enter:
            data="\n\r" # bitiş karakteri gönder
        else :
            data=str(key.char)
        
        p.stdin.write(data.encode())
        p.stdin.flush()

        print(data,end="") #debug için
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

with Listener(on_press=keyPressed) as l:
    l.join()