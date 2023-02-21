import time
import board
import busio

import adafruit_ccs811
import adafruit_dht


# DHT setup
dht = adafruit_dht.DHT22(board.GP2)

# I2C setup
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass

while True:
    try:
        print("CO2: {} PPM\tTVOC: {} PPM".format(ccs811.eco2, ccs811.tvoc))
        print("Temp: {:.1f} *C\tHumidity: {}%".format(dht.temperature, dht.humidity))
    except Exception as e:
        print("Error: ", e.args)

    print()
    time.sleep(1)
