import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
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
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# ==============================
# Configuración del relé
# ==============================
RELE_PIN = 26  # Pin GPIO para controlar el relé
rele = Pin(RELE_PIN, Pin.OUT)
rele.value(0)  # Asegurar que el relé inicie apagado

# ==============================
# Loop principal: Activación del relé cada 5 segundos
# ==============================
while True:
    # Encender el relé
    rele.value(1)
    mqtt_client.publish(MQTT_TOPIC, "Rele ON")
    print("Relé ENCENDIDO")
    time.sleep(2)

    # Apagar el relé
    rele.value(0)
    mqtt_client.publish(MQTT_TOPIC, "Rele OFF")
    print("Relé APAGADO")
    time.sleep(2)
