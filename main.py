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

class Tinyvim: 
# Raspberry Pi hardware SPI config:
  def __init__(self):
    self.DC = 23
    self.RST = 24
    self.SPI_PORT = 0
    self.SPI_DEVICE = 0

    # Hardware SPI usage:
    self.disp = LCD.PCD8544(
        self.DC, self.RST, 
        spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, 
        max_speed_hz=4000000))

    # Software SPI usage (defaults to bit-bang SPI interface):
    #disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

    # Initialize library.
    self.disp.begin(contrast=60)

    # Clear display.
    self.disp.clear()
    self.disp.display()

    # Raspberry Pi software SPI config:
    # SCLK = 4
    # DIN = 17
    # DC = 23
    # RST = 24
    # CS = 8


    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    self.image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

    # Get drawing object to draw on image.
    self.draw = ImageDraw.Draw(self.image)

    # Draw a white filled box to clear the image.
    self.draw.rectangle(
        (0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    # font = ImageFont.load_default()

  def set_5x7(self):
    self.font_size = 16
    self.font = ImageFont.truetype('fonts/Tinymoon5x7.ttf', 
        self.font_size)
    self.c_w = 6
    self.c_h = 8 # font.getsize("A");
    self.yoff = -5
    self.xoff = 0
  
  def set_5x9(self):
    self.font_size = 16
    self.font = ImageFont.truetype('fonts/Tinymoon5x9.ttf', 
        self.font_size)
    self.c_w = 6
    self.c_h = 9 # font.getsize("A");
    self.yoff = -4
    self.xoff = -1
  
  def draw_text(self, txt):
    self.draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
    col, row = 0, 0
    ncol = 84 / self.c_w
    # lc = 8 # 48 / c_h
    for c in txt:
      # print(c)
      if c == '\n':
        row = row + 1
        col = 0
      else:
        #if c == 'i' or c == 'I' or c == 'l':
        #  offset = 2
        print('x = ' + str(col * self.c_w) + ', y = ' + 
            str(row * self.c_h))
        self.draw.text((col * self.c_w + self.xoff, 
            row * self.c_h + self.yoff), c, font=self.font)
        col = col + 1
        if col == ncol:
          col = 0
          row = row + 1
    self.draw.text((col * self.c_w, 
        row * self.c_h + self.yoff), '_', font=self.font)
    self.disp.image(self.image)
    self.disp.display()
  
  def get_input(self):
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
      while True:
        try:
          c = sys.stdin.read(1)
          # print "Got character", repr(c)
          msg = msg + c
          self.draw_text(msg)
          # if c == '\n':
          #   msg = msg + os.system(msg)
        except IOError: pass
    finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
      fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  
if __name__ == '__main__':
  print 'Press Ctrl-C to quit.'
  vim = Tinyvim()
  # vim.set_5x9()
  vim.set_5x7()
  vim.draw_text('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?@#$%^&*()[]{}-+=:;<>')
  #get_input()
