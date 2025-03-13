import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion1/inclinacion"

# 📌 Configurar sensor SW-520D en GPIO25
sensor = machine.Pin(25, machine.Pin.IN)

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

# Último estado enviado
ultimo_estado = None

# 🔄 Loop principal
while True:
    estado = sensor.value()  # 1 = Vertical, 0 = Inclinado

    if estado == 0 and ultimo_estado != "Inclinado":
        mqtt_client.publish(MQTT_TOPIC, "Inclinado")
        print("📡 Enviado: Inclinado")
        ultimo_estado = "Inclinado"

    elif estado == 1 and ultimo_estado != "Vertical":
        mqtt_client.publish(MQTT_TOPIC, "Vertical")
        print("📡 Enviado: Vertical")
        ultimo_estado = "Vertical"

    time.sleep(0.2)  # Pequeño delay para evitar envíos excesivos