import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/SensorObstaculos"

# 📌 Configurar sensor KY-032
sensor = machine.Pin(18, machine.Pin.IN)

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

# 🔄 Loop principal para detectar obstáculos
while True:
    try:
        if sensor.value() == 0:  # Se detecta un obstáculo
            print("🚧 Obstáculo detectado")
            mqtt_client.publish(MQTT_TOPIC, "Obstáculo detectado")
        else:
            print("✅ No hay obstáculos")
            mqtt_client.publish(MQTT_TOPIC, "No hay obstáculos")

        time.sleep(0.5)  # Pequeña pausa para evitar spam

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla