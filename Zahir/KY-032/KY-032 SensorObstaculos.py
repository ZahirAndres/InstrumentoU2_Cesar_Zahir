import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# ==============================
# Configuración WiFi y MQTT
# ==============================

SSID = "Cesar"
PASSWORD = "123456789"

MQTT_BROKER = "192.168.71.135"
MQTT_TOPIC = "zarm/sesion4"

# ==============================
# Configuración del sensor KY-032
# ==============================
sensor_ir = Pin(14, Pin.IN)  # OUT del KY-032 al GPIO 14

# ==============================
# Función para conectar WiFi
# ==============================
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        time.sleep(1)
    print("Conectado a WiFi en ESP32")

# ==============================
# Función para conectar al broker MQTT con reconexión
# ==============================
def conectar_mqtt():
    global mqtt_client
    try:
        mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
        mqtt_client.connect()
        print("Conectado al broker MQTT")
    except OSError as e:
        print("Error conectando al broker MQTT, reintentando en 5s...")
        time.sleep(5)
        conectar_mqtt()

# ==============================
# Iniciar conexión
# ==============================
conectar_wifi()
conectar_mqtt()

# ==============================
# Loop principal: detección de obstáculos con reconexión
# ==============================
estado_anterior = None

while True:
    estado = sensor_ir.value()  # 0 = obstáculo detectado, 1 = sin obstáculo

    if estado_anterior is None:
        estado_anterior = estado

    if estado != estado_anterior:
        if estado == 0:
            mensaje = "Obstáculo detectado"
        else:
            mensaje = "Obstáculo no detectado"

        try:
            mqtt_client.publish(MQTT_TOPIC, mensaje)
            print("Mensaje enviado:", mensaje)
        except OSError:
            print("Error al enviar mensaje, intentando reconectar...")
            conectar_mqtt()

        estado_anterior = estado

    time.sleep(0.1)
