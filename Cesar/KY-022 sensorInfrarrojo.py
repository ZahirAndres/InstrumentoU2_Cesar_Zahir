
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
# ==============================
SSID = "Cesar"
PASSWORD = "123456789"
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion6"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)
print("Conectado a WiFi")

# Conectar al broker MQTT
mqtt_client = MQTTClient("ESP32_IR", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# ==============================
# Configuración del sensor receptor de infrarrojos KY-022
# ==============================
# Conectar el pin OUT del sensor al GPIO14 del ESP32
# Se utiliza una resistencia pull-up para asegurar un estado HIGH en reposo
ir_sensor = Pin(14, Pin.IN, Pin.PULL_UP)

# Variable para almacenar el estado anterior
estado_anterior = ir_sensor.value()

while True:
    estado_actual = ir_sensor.value()
    # Si hay un cambio en el estado, se publica el mensaje correspondiente
    if estado_actual != estado_anterior:
        if estado_actual == 0:
            mensaje = "IR signal detected"
        else:
            mensaje = "IR signal ended"
        mqtt_client.publish(MQTT_TOPIC, mensaje)
        print(mensaje)
        estado_anterior = estado_actual
    time.sleep(0.1)  # Pequeño retardo para evitar lecturas excesivas