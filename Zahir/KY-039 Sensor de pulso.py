import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/SensorPulso"

# 📌 Configurar Sensor KY-039 en GPIO 34 (ADC)
sensor = machine.ADC(machine.Pin(34))
sensor.atten(machine.ADC.ATTN_11DB)  # Rango 0 - 3.3V

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("✅ Conectado a WiFi")

# 📡 Conectar a MQTT
def conectar_mqtt():
    global mqtt_client
    try:
        mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
        mqtt_client.connect()
        print("✅ Conectado al broker MQTT")
    except Exception as e:
        print("❌ Error al conectar MQTT:", e)
        time.sleep(5)
        conectar_mqtt()

conectar_mqtt()

# 🔄 Loop para leer el sensor y enviar datos a MQTT
while True:
    try:
        pulso = sensor.read()  # Leer valor analógico (0-4095)
        print(f"💓 Pulso: {pulso}")
        mqtt_client.publish(MQTT_TOPIC, str(pulso))
        time.sleep(0.5)  # Leer cada 500ms

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla