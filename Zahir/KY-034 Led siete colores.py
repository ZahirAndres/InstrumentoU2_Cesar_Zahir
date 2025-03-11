import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/LedSieteColores"

# 📌 Configurar LED KY-034
led = machine.Pin(27, machine.Pin.OUT)  # SIG conectado a GPIO 27

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

# 🔄 Loop para encender y apagar el LED cada 2 segundos
while True:
    try:
        led.value(1)  # Encender LED
        print("💡 LED ENCENDIDO")
        mqtt_client.publish(MQTT_TOPIC, "LED ENCENDIDO")
        time.sleep(2)

        led.value(0)  # Apagar LED
        print("🌑 LED APAGADO")
        mqtt_client.publish(MQTT_TOPIC, "LED APAGADO")
        time.sleep(2)

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla