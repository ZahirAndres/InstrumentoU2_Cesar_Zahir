import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/SeguidorLineas"

# 📌 Configurar sensor KY-033
sensor_linea = machine.Pin(26, machine.Pin.IN)  # OUT del sensor conectado a GPIO 26

estado_anterior = None  # Para detectar cambios

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

# 🔄 Loop para detectar línea
while True:
    try:
        valor = sensor_linea.value()  # 0 = línea negra, 1 = superficie blanca

        if valor == 0:
            estado_actual = "⬛ Línea negra detectada"
        else:
            estado_actual = "⬜ Superficie blanca detectada"

        # Si el estado cambia, enviar mensaje MQTT
        if estado_actual != estado_anterior:
            print(estado_actual)
            mqtt_client.publish(MQTT_TOPIC, estado_actual)
            estado_anterior = estado_actual  # Guardar estado

        time.sleep(0.5)  # Pequeño delay

    except Exception as e:
        print("❌ Error en la detección:", e)
        conectar_mqtt()  # Intentar reconectar en caso de fallo