# air quality monitor using the Raspberry Pi Pico W

Checkout the whole story on [Medium](https://medium.com/@lukas.krimphove).

## What are we going to do?
Together with you, I want to build an air quality monitor to gather different parameters. To know whether I have to air my room or not I need to know the current humidity level and the carbon dioxide concentration. So my device has to be able to measure those. I want to collect, store and visualize the gathered data centralized. In the future, I want to do this by sending all the data to my homeserver, where I can use software like InfluxDB and Grafana. Last but not least I want to get notified, whenever the humidity or the CO2 exceeds a certain threshold. This could be done by mail (using Grafana Alerts) or even better by push notification (using Home Assistant). There are a few other improvements I might implement later like a small display, a battery pack, and a 3D-printed case to bring it all together.

## About the Raspberry Pi Pico
The Raspberry Pi Pico is a low-cost, high-performance microcontroller board. There are two different versions: the normal Pico and the Pico W, which comes with built in wlan. It comes with a rich peripheral set, including SPI, I2C, and eight Programmable I/O (PIO) state machines for custom peripheral support. You can use C or (MicroPython)[https://micropython.org/] (an implementation of Python 3) to program it. All this makes it the perfect match for all kinds of small hobby projects like this.

## About the sensors
I am using two sensors to gather all the data I need. The [DHT22](https://learn.adafruit.com/dht) measures temperature and humidity. The [CCS811](https://learn.adafruit.com/adafruit-ccs811-air-quality-sensor) detects Volatile Organic Compounds (VOCs). We can use this to get a Total Volatile Organic Compound (TVOC) reading and an equivalent carbon dioxide reading (eCO2). 

## Wiring it all up
The wiring is quite simple. Check out the Picos [pinout diagram](https://datasheets.raspberrypi.com/picow/PicoW-A4-Pinout.pdf) and then connect the sensors according to their documentation.

- CCS811
	- 3V3 to 3V3 (red)
	- GND to GND (black)
	- I2C (blue)
		- SDA to GP0 (SDA)
		- SCL to GP1 (SCL)
	- WAKE to GND (black)
- DHT22
	- VCC to 3V3 (red)
	- Data to GP2 (blue)
	- GND to GND (black)

## The dependencies
First, you will have to download [CircuitPython](https://circuitpython.org/board/raspberry_pi_pico). CircuitPython is a programming language based on MicroPython. You also should set up your development environment and get a code editor for python (if you don’t have one). A quick and easy way is using [Mu](https://codewith.mu), a simple editor that works out-of-the-box with CircuitPython. It comes for Windows, Linux, and Mac and can easily be connected with most microcontrollers. You can find some detailed instructions [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor). There are also solutions for IDEs like [PyCharm](https://learn.adafruit.com/welcome-to-circuitpython/pycharm-and-circuitpython).

Now you can install CircuitPython onto your board. Therefore you have to unplug the Pico. Then hold down the BOOTSEL button on your Pico. Plug the Pico into your computer's USB port while still holding down the BOOTSEL button. Now let go of the BOOTSEL button. Now you should be able to see the RPI-RP2 drive. Open it and copy the ‘adafruit_circuitpython_etc.uf2’ into it. RPI-RP2 disappears and the CIRCUITPY drive appears. You have successfully installed CircuitPython.

Next, you will have to copy all the dependencies. Simply download the [Adafruit CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) Bundle. In it you will find everything you need. Copy the following modules from the bundle's lib folder into the lib folder on your CIRCUITPY drive:
- `adafruit_ccs811.mpy`
- `adafruit_register/*`
- `adafruit_bus_device/*`
- `adafruit_dht.mpy`

## The code
Create a new file called ‘code.py’ (it is important that you name it like this, otherwise CircuitPython won’t find it) and copy the code into it. As soon as you save the file the code will be executed.
To check the outputs use Mu to open a serial connection. If you are on Linux you can also use minicom (‘sudo minicom -o -D /dev/ttyACM0’).
You can check if your sensors are working by simply blowing on them. This should raise the CO2 and TVOC readings.
