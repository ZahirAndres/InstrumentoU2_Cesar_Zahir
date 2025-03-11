import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.90.135"
MQTT_TOPIC = "zarm/sesion7/impacto"

# 📌 Configurar el sensor KY-031 con interrupción
sensor_impacto = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("✅ Conectado a WiFi")

# 📡 Conectar a MQTT
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("✅ Conectado al broker MQTT")

# 📌 Función de interrupción cuando se detecta un impacto
def impacto_detectado(pin):
    print("💥 ¡Impacto detectado!")
    mqtt_client.publish(MQTT_TOPIC, "Impacto detectado en ESP32")

# Configurar la interrupción en el sensor (cambio de estado)
sensor_impacto.irq(trigger=machine.Pin.IRQ_FALLING, handler=impacto_detectado)

# 🔄 Loop principal (mantiene el código en ejecución)
while True:
    time.sleep(1)