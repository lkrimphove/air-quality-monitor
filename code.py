import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT

import board
import busio

import adafruit_ccs811
import adafruit_dht


# WiFi setup
wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))

# Feed setup
co2_feed = os.getenv("AIO_USERNAME") + "/feeds/air-quality.co2"
tvoc_feed = os.getenv("AIO_USERNAME") + "/feeds/air-quality.tvoc"
temperature_feed = os.getenv("AIO_USERNAME") + "/feeds/air-quality.temperature"
humidity_feed = os.getenv("AIO_USERNAME") + "/feeds/air-quality.humidity"

pool = socketpool.SocketPool(wifi.radio)

# MQTT setup
def connected(client, userdata, flags, rc):
    # gets called when client is connected successfully to the broker
    print("Connected to Adafruit IO")


def disconnected(client, userdata, rc):
    # gets called when client is disconnected
    print("Disconnected from Adafruit IO")

mqtt_client = MQTT.MQTT(
    broker=os.getenv("BROKER"),
    port=os.getenv("PORT"),
    username=os.getenv("AIO_USERNAME"),
    password=os.getenv("AIO_KEY"),
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected

print("Connecting to Adafruit IO...")
mqtt_client.connect()

# DHT setup
dht = adafruit_dht.DHT22(board.GP2)

# I2C setup
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the sensor to be ready
while not ccs811.data_ready:
    pass


def average(measurements, key):
    sum = 0
    for i in measurements:
        sum = sum + i[key]
    return sum / len(measurements)


measurements = []
while True:
    try:
        print()
        print(len(measurements))
        print("CO2: {} PPM\tTVOC: {} PPM".format(ccs811.eco2, ccs811.tvoc))
        print("Temp: {:.1f} *C\tHumidity: {}%".format(dht.temperature, dht.humidity))
        
        if len(measurements) >= 60:
            print("Sending data to Adafruit IO")

            mqtt_client.publish(co2_feed, average(measurements, "co2"))
            mqtt_client.publish(tvoc_feed, average(measurements, "tvoc"))
            mqtt_client.publish(temperature_feed, average(measurements, "temperature"))
            mqtt_client.publish(humidity_feed, average(measurements, "humidity"))

            measurements = []
        else:
            measurements.append(
                {
                    "co2": ccs811.eco2,
                    "tvoc": ccs811.tvoc,
                    "temperature": dht.temperature,
                    "humidity": dht.humidity,
                }
            )
        
    except RuntimeError as e:
        print("Reading error: ", e.args)

    time.sleep(1)

