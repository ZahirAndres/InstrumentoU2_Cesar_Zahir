import network
import time
import machine
from umqtt.simple import MQTTClient

# 📌 Configurar conexión WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar broker MQTT
MQTT_BROKER = "192.168.127.135"
MQTT_TOPIC = "zarm/nivel_agua"

# 📌 Configurar sensor de nivel de agua (modo digital DO)
sensor_agua = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi!")

# 📡 Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("✅ Conectado a MQTT!")

ultimo_estado = sensor_agua.value()

while True:
    estado_actual = sensor_agua.value()

    if estado_actual != ultimo_estado:
        time.sleep(0.1)  # Pequeño delay para evitar ruido
        if sensor_agua.value() == estado_actual:
            ultimo_estado = estado_actual
            mensaje = "Agua detectada" if estado_actual == 1 else "Sin agua"
            print(f"📡 Enviando estado: {mensaje}")
            client.publish(MQTT_TOPIC, mensaje)

    time.sleep(0.5)  # Evitar lecturas muy rápidas
