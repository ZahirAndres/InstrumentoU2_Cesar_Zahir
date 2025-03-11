import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/SensorTactilMetal"

# 📌 Configurar Sensor KY-036 en GPIO 27 (DO)
sensor = machine.Pin(27, machine.Pin.IN)

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

# 🔄 Loop para detectar contacto y enviar datos a MQTT
while True:
    try:
        if sensor.value() == 1:
            print("🖐 ¡Contacto detectado!")
            mqtt_client.publish(MQTT_TOPIC, "Contacto detectado")
        else:
            print("❌ Sin contacto")
            mqtt_client.publish(MQTT_TOPIC, "Sin contacto")

        time.sleep(0.5)  # Leer cada 500ms

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla