# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont


# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Raspberry Pi software SPI config:
# SCLK = 4
# DIN = 17
# DC = 23
# RST = 24
# CS = 8

# Beaglebone Black hardware SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Beaglebone Black software SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SCLK = 'P8_7'
# DIN = 'P8_9'
# CS = 'P8_11'


# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
#
## Draw some shapes.
#draw.ellipse((2,2,22,22), outline=0, fill=255)
#draw.rectangle((24,2,44,22), outline=0, fill=255)
#draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
#draw.line((68,22,81,2), fill=0)
#draw.line((68,2,81,22), fill=0)

# Load default font.
# font = ImageFont.load_default()
font_size = 12
font = ImageFont.truetype('profont.ttf', font_size)
(cw, ch) = font.getsize("A");

# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

  
def draw_text(txt):
  draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
  x, y = 0, 0
  cc = 84 / cw
  # lc = 8 # 48 / ch
  for c in txt:
    # print(c)
    if c == '\n':
      y = y + 1
      x = 0
    else:
      #if c == 'i' or c == 'I' or c == 'l':
      #  offset = 2
      print('x = ' + str(x * cw) + ', y = ' + str(y * 8))
      draw.text((x * cw, y * ch), c, font=font)
      x = x + 1
      if x == cc:
        x = 0
        y = y + 1
  draw.text((x * cw, y * ch), '_', font=font)
  disp.image(image)
  disp.display()

# draw_text("hi!\nI'm teddy.")

## test chars
# draw_text("abcdefghijklmnop\nopqrstuvwxyz\n!@#$%^&*()_\n+|{}[]:;'")
## test wrapping
# draw_text("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopopqrstuvwxyz")
## hello, world
# draw_text("hello, world...")
# draw_text("ken@pi$ ")

# while True:
#   draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
#   # prompt = prompt + ch
#   draw.text((0,0),  'ABCDEFGHIJKLMN', font=font)
#   draw.text((0,8),  'OPQRSTUVWXYZab', font=font)
#   draw.text((0,16), 'cdefghijklmnop', font=font)
#   draw.text((0,24), 'qrstuvwxyz', font=font)
#   draw.text((0,32), 'qrstuvwxyz', font=font)
#   draw.text((0,40), 'gjA', font=font)
# 
# 
#   disp.image(image)
#   disp.display()
# 
#   time.sleep(1.0)

def get_input():
  import termios, fcntl, sys, os
  fd = sys.stdin.fileno()
  
  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)
  
  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
  
  msg = ''

  try:
    while 1:
      try:
        c = sys.stdin.read(1)
        # print "Got character", repr(c)
        msg = msg + c
        draw_text(msg)
        # if c == '\n':
        #   msg = msg + os.system(msg)
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

if __name__ == '__main__':
  print 'Press Ctrl-C to quit.'
  draw_text('')
  get_input()
