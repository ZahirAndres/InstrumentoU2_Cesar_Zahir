import network
import time
import machine
from umqtt.simple import MQTTClient

# 📌 Configurar conexión WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar broker MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion2"

# 📌 Configurar sensor de vibración en entrada analógica (GPIO 34)
sensor_vibracion = machine.ADC(machine.Pin(32))  # GPIO 34 (ADC1)
sensor_vibracion.atten(machine.ADC.ATTN_11DB)  # Rango 0 - 3.3V

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)

print("✅ Conectado a WiFi!")

# 📡 Conectar a MQTT
client = MQTTClient("ESP32_Vibracion", MQTT_BROKER)
client.connect()
print("✅ Conectado a MQTT!")

def leer_vibracion():
    lectura = sensor_vibracion.read()  # Leer valor ADC (0 - 4095)
    voltaje = lectura * (3.3 / 4095)  # Convertir a voltaje
    return voltaje

while True:
    vibracion = leer_vibracion()
    
    if vibracion > 0.5:  # Umbral de detección de vibración (ajustable)
        mensaje = f"⚠ Vibración detectada: {vibracion:.2f}V"
        print(f"📡 Enviando: {mensaje}")
        client.publish(MQTT_TOPIC, mensaje)  # Enviar datos de vibración a MQTT

    time.sleep(0.5)  # Esperar 500ms para lecturas rápidas
