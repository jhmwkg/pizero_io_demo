"""
This example is cobbled together from the following hardware/code:
https://learn.adafruit.com/adafruit-1-3-color-tft-bonnet-for-raspberry-pi/python-setup
https://learn.adafruit.com/lsm6ds33-6-dof-imu=accelerometer-gyro/python-circuitpython

And of course a Raspberry Pi Zero

Resulting graphic on the display will be two circular graphics.
The left one is for the accelerometer, a circle outline getting squished inside another circle outline.
The right one is for the gyroscope, a filled circle moving across a centerpoint to show direction of force.
"""

# library imports

## general
import time
import random
import board
import busio
from digitalio import DigitalInOut, Direction

## oled
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

## 6dof
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33

# setups
## general
i2c = busio.I2C(board.SCL, board.SDA)

## oled bonnet
# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000
 
spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
 
# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
 
button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
 
button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
 
button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
 
button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
 
button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
 
button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
 
# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True
 
# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

 
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)

## 6dof
lsm6 = LSM6DS33(i2c)

# main loop
while True:    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
 
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #accel is position, up to 10
    #gyro is direction, up to 5
    ax,ay,az = lsm6.acceleration
    gx,gy,gz = lsm6.gyro
    
    # setting centerpoints for each graphic
    m_ax = 80
    m_ay = 120
    m_gx = 160
    m_gy = 120
    
    # colors adjust to z axis changes
    coloraz = int(128+az*10)+128
    colorgzr = int(128+gz*20)
    colorgzb = int(128-gz*20)
    
    fix = 1.2 # multiplier against sensor returns
    fix2 = 15 # buffer to maintain graphic visibility
    fix3 = fix2*2
    
    # math for drawing
    cax1 = m_ax-(ax*fix)-fix2
    cay1 = m_ay-(ay*fix)-fix2
    cax2 = m_ax+(ax*fix)+fix2
    cay2 = m_ay+(ay*fix)+fix2
    
    cgx1 = m_gx-gx*fix-fix2
    cgy1 = m_gy-gy*fix-fix2
    
    # draw.ellipse((x1,y1,x2,y2),outline="#",fill="#")
    # draw funcs actually draw between two corners, upper-left and lower-right
    draw.ellipse((m_ax-30,m_ay-30,m_ax+30,m_ay+30),outline="#999999",fill=0)
    draw.ellipse((cgx1,cgy1,cgx1+fix3,cgy1+fix3),outline=0,fill=((colorgzr),0,(colorgzb)))
    draw.ellipse((cax1,cay1,cax2,cay2),outline=(coloraz,coloraz,coloraz),fill=(0,0,0,0))
    draw.ellipse((m_gx-3,m_gy-3,m_gx+3,m_gy+3),outline="#aaaaaa",fill=0)
    
    disp.image(image)
    time.sleep(0.01)
