
"""Simple example to print acceleration data to console"""
import time
import digitalio
import board
import busio
import adafruit_lis3dh

import audiocore
import audiobusio



import pixel as lights

# Set up accelerometer on I2C bus, 4G range:
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)
accel = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
accel.range = adafruit_lis3dh.RANGE_4_G
accel.set_tap(1, 100)

enable = digitalio.DigitalInOut(board.EXTERNAL_POWER)
enable.direction = digitalio.Direction.OUTPUT
enable.value = True

powerpin = digitalio.DigitalInOut(board.D13)
powerpin.direction = digitalio.Direction.OUTPUT
powerpin.value = False

handleSensor = digitalio.DigitalInOut(board.D24)
handleSensor.direction = digitalio.Direction.INPUT
handleSensor.pull = digitalio.Pull.DOWN

reedSwitch = digitalio.DigitalInOut(board.D5)
reedSwitch.direction = digitalio.Direction.INPUT
reedSwitch.pull = digitalio.Pull.DOWN

# Global Varible init
is_shooting = False
powered_on = False
shutdown_time = 4

# Audio setup
audio = audiobusio.I2SOut(board.I2S_BIT_CLOCK, board.I2S_WORD_SELECT, board.I2S_DATA)

def PlayTest():
    with open("StreetChicken.wav", "rb") as wave_file:
        wav = audiocore.WaveFile(wave_file)

        print("Playing wav file!")
        audio.play(wav)
        while audio.playing:
            pass

    print("Done!")
    
lastAudioFile = open("StreetChicken.wav","rb")
lastAudioFile.close()
lastAudioFile = None

################   CORE FUNCTIONS   ################
def FireBlast():
    lights.Blast()
    
    global lastAudioFile
    
    if (audio.playing):
        audio.stop()
        lastAudioFile.close()
        
    lastAudioFile = open("blast.wav", "rb")
    wav = audiocore.WaveFile(lastAudioFile)

    audio.play(wav)
    
previousAccelX = 0
previousAccelY = 0
previousAccelZ = 0
def GetCalibratedAccel():
    global previousAccelX
    global previousAccelY
    global previousAccelZ
    
    x, y, z =  accel.acceleration
    
    new = (x - previousAccelX, y - previousAccelY, z - previousAccelZ)
    
    previousAccelX = x
    previousAccelY = y
    previousAccelZ = z
    return new
    


################   SETUP   ################

################   LOOP   ################
def Update():
    global is_shooting
    global powered_on
    global shutdown_time
    global lastAudioFile
    
    if (not handleSensor.value) and (powered_on):
        print("poweroff begin")
        startTime = time.time()
        
        prevCount = -1
        
        while ((time.time() < (startTime + shutdown_time)) and (not handleSensor.value)):
            time.sleep(0.1)
            
            if ((startTime + shutdown_time) - time.time() != prevCount):
                print((startTime + shutdown_time) - time.time())
                prevCount = ((startTime + shutdown_time) - time.time())
            
            
        if (time.time() >= (startTime + shutdown_time)):
            powered_on = False
            lights.PowerOff()
            enable.value = False
            powerpin.value = False
            
            print("powered off. Low power mode enabled")
        else:
            print("poweroff canceled")
            
    if (handleSensor.value and (not powered_on)):
        powered_on = True
        enable.value = True
        powerpin.value = True
        lights.PowerOn()
    
            
    if (powered_on):
        x, y, z = GetCalibratedAccel()
        
        if ((x > 10) and (not is_shooting)):
            print("pew!!!")
            
            FireBlast()
            
            is_shooting = True
        if ((x < 3) and (is_shooting)):
            is_shooting = False
            
        if (reedSwitch.value):
            while (reedSwitch.value):
                lights.Circle()
                time.sleep(0.05)
            lights.Standby()
        
    if ((not audio.playing) and (lastAudioFile != None)):
        lastAudioFile.close()
        lastAudioFile = None
    
    time.sleep(0.05)


while True:
    Update()  
    
lights.PowerOff()