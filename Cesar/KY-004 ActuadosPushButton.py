import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# 📌 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion3"

# 📌 Configurar botón en GPIO 18 (ESP32)
boton = Pin(18, Pin.IN, Pin.PULL_UP)

# 📡 Conectar a WiFi en ESP32
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("Conectado a WiFi en ESP32")

# 📡 Configurar MQTT en ESP32
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()

print("Conectado al broker MQTT")

# 📌 Loop principal en ESP32
while True:
    if boton.value() == 0:  # Si se presiona el botón
        mqtt_client.publish(MQTT_TOPIC, "Botón presionado en ESP32")
        print("Mensaje enviado: Botón presionado en ESP32")
        time.sleep(1)  # Pequeño delay para evitar múltiples envíos
