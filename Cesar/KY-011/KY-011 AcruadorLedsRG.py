import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# 📌 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion3"

# 📌 Configurar pines del LED KY-011
led_rojo = Pin(18, Pin.OUT)   # LED rojo en GPIO 18
led_verde = Pin(19, Pin.OUT)  # LED verde en GPIO 19

# 📡 Conectar a WiFi en ESP32
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("Conectado a WiFi en ESP32")

# 📡 Configurar MQTT en ESP32
def conectar_mqtt():
    global mqtt_client
    while True:
        try:
            print(f"Intentando conectar al broker MQTT en {MQTT_BROKER}...")
            mqtt_client = MQTTClient("ESP32", MQTT_BROKER, keepalive=60)
            mqtt_client.connect()
            print("✅ Conectado al broker MQTT")
            return
        except OSError as e:
            print(f"⚠️ Error conectando al broker MQTT: {e}")
            time.sleep(5)

# Conectar al iniciar
conectar_mqtt()

# 📌 Loop principal en ESP32
estado = 0  # Variable para alternar entre los colores

while True:
    try:
        if estado == 0:
            led_rojo.value(1)
            led_verde.value(0)
            mensaje = "LED en ROJO"
        else:
            led_rojo.value(0)
            led_verde.value(1)
            mensaje = "LED en VERDE"

        mqtt_client.publish(MQTT_TOPIC, mensaje)
        print(f"Mensaje enviado: {mensaje}")

        estado = 1 - estado  # Alternar estado (0 ↔ 1)

    except OSError as e:
        print(f"Error MQTT: {e}, reconectando...")
        conectar_mqtt()

    time.sleep(2)  # Esperar 2 segundos antes de cambiar el color
