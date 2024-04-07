
import time
import math
import board
import digitalio
import neopixel

pixel_pin = board.EXTERNAL_NEOPIXELS
num_pixels = 22

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

standby_color = (255, 90, 0)
standby_brightness = 0.3

blast_color = (255, 255, 255)
blast_brightness = 1
blast_size = 2

circle_pixel_range = 11
circle_color = (255, 90, 0)
circle_brightness = 0.8

circle_index = 0

center_front_pixel = 5
center_back_pixel = 16



def PowerOn():
    for c in range(9):
        for p in range(num_pixels):
            if (abs(p - center_front_pixel) < c):
                pixels[p] = standby_color
            if (abs(p - center_back_pixel) < c):
                pixels[p] = standby_color
                
        pixels.brightness = ((standby_brightness / 8) * c)
        pixels.show()
        time.sleep(0.05)
    Standby()
        
def PowerOff():
    for c in range(9):
        for p in range(num_pixels):
            if (abs(p - center_front_pixel) < c):
                pixels[p] = (0, 0, 0)
            if (abs(p - center_back_pixel) < c):
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
    BlastOn()
    time.sleep(0.1)
    Standby()
    
def BlastOn():
    pixels.brightness = blast_brightness
    for p in range(center_front_pixel - blast_size, center_front_pixel + blast_size + 1):
        pixels[p] = blast_color
    pixels.show()
    
    
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
            
