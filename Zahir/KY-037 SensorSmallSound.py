import network
import time
import machine
from umqtt.simple import MQTTClient

# 📌 Configurar conexión WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar broker MQTT
MQTT_BROKER = "192.168.127.135"
MQTT_TOPIC = "zarm/sonido"

# 📌 Configurar sensor de sonido en entrada analógica (GPIO 34)
sensor_sonido = machine.ADC(machine.Pin(34))  # GPIO 34 (ADC1)
sensor_sonido.atten(machine.ADC.ATTN_11DB)  # Rango 0 - 3.3V

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
    lectura = sensor_sonido.read()  # Leer nivel de sonido (0 - 4095)
    voltaje = lectura * (3.3 / 4095)  # Convertir a voltaje
    mensaje = f"Ruido: {lectura}, Voltaje: {voltaje:.2f}V"

    print(f"📡 Enviando: {mensaje}")
    client.publish(MQTT_TOPIC, mensaje)  # Enviar datos a MQTT

    time.sleep(1)  # Esperar 1 segundo
