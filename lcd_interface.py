from lib_oled96 import ssd1306
from PIL import Image
from smbus import SMBus
from time import sleep

class LcdInterface(object):
    def __init__(self):
        self.i2cbus = SMBus(1)        # 1 = Raspberry Pi but NOT early REV1 board

        self.oled = ssd1306(self.i2cbus)   # create oled object, nominating the correct I2C bus, default address
        self.canvas = self.oled.canvas
        try:
            self.logo_image = Image.open(self.logo_image_path)
        except:
            pass

        self.show_logo()
        sleep(2)
        self.cls()


    i2cbus = None
    oled = None
    canvas = None
    logo_image_path = "/home/pi/b/RaspiBluePlayer/raspiblueplayer128logo.png"
    logo_image = None
    
    def show_logo(self):
        self.oled.canvas.bitmap((0,0), self.logo_image, fill=1)
        self._display()

    def _display(self):
        self.oled.display()

    def text(self, px, py, t):
        self.canvas.text((px, py), t, fill=1)
        self.oled.display()

    def cls(self):
        self.oled.cls()