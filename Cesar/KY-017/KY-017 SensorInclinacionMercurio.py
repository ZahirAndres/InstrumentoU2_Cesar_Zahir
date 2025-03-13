import network
import time
import machine
from umqtt.simple import MQTTClient

# 📌 Configurar conexión WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar broker MQTT
MQTT_BROKER = "192.168.127.135"  # Puedes usar otro broker
MQTT_TOPIC = "zarm/inclinacion"  # Tópico donde se enviará la inclinación

# 📌 Configurar sensor de inclinación KY-027
sensor_inclinacion = machine.Pin(15, machine.Pin.IN)  # Entrada digital

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

while True:
    inclinacion = sensor_inclinacion.value()  # Leer estado del sensor (0 o 1)
    mensaje = "Inclinado" if inclinacion == 1 else "Estable"
    
    print(f"📡 Enviando estado: {mensaje}")
    client.publish(MQTT_TOPIC, mensaje)  # Enviar estado al broker
    
    time.sleep(4)  # Esperar 1 segundo
