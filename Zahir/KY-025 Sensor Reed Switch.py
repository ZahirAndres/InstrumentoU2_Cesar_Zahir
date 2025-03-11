import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.90.135"
MQTT_TOPIC = "zarm/sesion7/ReedSwitch"

# 📌 Configurar sensor KY-025 en GPIO 25 (Salida Digital D0)
sensor = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)  # Asegura lectura estable
estado_anterior = sensor.value()

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

# 🔄 Loop para detectar campo magnético
def asegurar_conexion_mqtt():
    try:
        mqtt_client.ping()  # Verificar si el broker está disponible
    except Exception as e:
        print("❌ Se perdió la conexión al MQTT, reconectando...", e)
        conectar_mqtt()

while True:
    try:
        estado_actual = sensor.value()

        # Si el estado cambia, enviamos un mensaje
        if estado_actual != estado_anterior:
            asegurar_conexion_mqtt()  # Verificar si el cliente MQTT está conectado

            if estado_actual == 0:  # Activo bajo (según el sensor)
                print("🧲 ¡Campo magnético detectado!")
                mqtt_client.publish(MQTT_TOPIC, "¡Campo magnético detectado!")
            else:
                print("❌ Campo magnético perdido")

            estado_anterior = estado_actual  # Guardar estado

        time.sleep(1)  # Pequeño delay para evitar saturación

    except Exception as e:
        print("❌ Error en la detección:", e)
        asegurar_conexion_mqtt()  # Intentar reconectar en caso de error
