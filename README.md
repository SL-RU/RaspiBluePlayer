# RaspiBluePlayer
 Bluetooth music and audiobooks player app for Raspberry PI.

Player based on Raspberry Pi A+. With internal 2200mA*h li-pol battery, bluetooth module, DC-DC convertor(from li-pol to 5V), keyboard with nine buttons, two leds, and 3 usb ports for connecting external devices. As lcd cheap i2c 0.96" 128x64 OLED display from ebay.

Current hardware stage: compiling all components together. Soon will be photos.

In develop:
* special mode for audiobooks 
* LCD display control UI

Done:
* playing all major audio formats
* music player
* smart playlist for music
* bluetooth connection
* connecting to bluetooth headphones
* Lcd OLED display 
* controlling with bluetooth headphone's buttons
* controlling with hardware buttons on gpio

Obsolete:
* basic web interface (not developing anymore)

##Resources
- For playing audio I'm using VLC python bindings https://wiki.videolan.org/Python_bindings
- For web interface: CherryP http://www.cherrypy.org/
- LCD library: https://github.com/BLavery/lib_oled96


##License
Released under the MIT license.
