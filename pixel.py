
import time
import math
import board
import neopixel
import digitalio

pixel_pin = board.EXTERNAL_NEOPIXELS
num_pixels = 25

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

standby_color = (255, 90, 0)
standby_brightness = 0.3

blast_color = (255, 255, 255)
blast_brightness = 1

circle_pixel_range = 15
circle_color = (0, 100, 255)
circle_brightness = 0.4

circle_index = 0


def PowerOn():
    for c in range(9):
        for p in range(num_pixels):
            if (abs(p - 7) < c):
                pixels[p] = standby_color
            if (abs(p - 19.5) < c):
                pixels[p] = standby_color
                
        pixels.brightness = ((standby_brightness / 8) * c)
        pixels.show()
        time.sleep(0.05)
    Standby()
        
def PowerOff():
    for c in range(9):
        for p in range(num_pixels):
            if (abs(p - 7) < c):
                pixels[p] = (0, 0, 0)
            if (abs(p - 19.5) < c):
                pixels[p] = (0, 0, 0)
                
        pixels.brightness = ((standby_brightness / 8) * (8 - c))
        pixels.show()
        time.sleep(0.1)
        
def Standby():
    for p in range(num_pixels):
        pixels[p] = standby_color
    pixels.brightness = standby_brightness
    pixels.show()
                
        
def Blast():
    pixels.brightness = blast_brightness
    for p in range(4, 10):
        pixels[p] = blast_color
    pixels.show()
    time.sleep(0.1)
    Standby()
    
def Debug():
    for p in range(num_pixels):
        pixels[p] = (255, 0, 255)
    pixels.brightness = 1
    pixels.show()
    
def Circle():
    global circle_index
    for p in range(circle_pixel_range):
        if (abs(p - circle_index) < 3):
            pixels[p] = circle_color
        else:
            pixels[p] = (0, 0, 0)
            
    pixels.brightness = circle_brightness
    pixels.show()
     
    circle_index = (circle_index + 1) % (circle_pixel_range * 2)
            
