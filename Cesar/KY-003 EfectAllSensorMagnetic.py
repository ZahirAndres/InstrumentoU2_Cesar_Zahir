
import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
# ==============================

SSID = "Cesar"
PASSWORD = "123456789"

MQTT_BROKER = "192.168.71.135"
MQTT_TOPIC = "zarm/sesion4"

# ==============================
# Configuración del sensor Hall KY-003
# ==============================
# Conectar:
# - VCC a 5V (o 3.3V, según el módulo)
# - GND a tierra
# - DO (salida digital) a GPIO15 del ESP32
sensor_hall = Pin(15, Pin.IN)

# ==============================
# Conexión a WiFi
# ==============================
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)
print("Conectado a WiFi en ESP32")

# ==============================
# Conexión al broker MQTT
# ==============================
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# ==============================
# Loop principal: Detección del campo magnético
# ==============================

estado_anterior = None

while True:
    estado = sensor_hall.value()  # Lee el estado del sensor (0 o 1)
    
    # Inicializar el estado y enviar el primer mensaje
    if estado_anterior is None:
        estado_anterior = estado
        if estado == 0:
            mensaje = "Campo magnético detectado (inicial)"
        else:
            mensaje = "No se detecta campo magnético (inicial)"
        mqtt_client.publish(MQTT_TOPIC, mensaje)
        print("Mensaje enviado:", mensaje)
    else:
        # Si el estado ha cambiado, enviar mensaje vía MQTT
        if estado != estado_anterior:
            if estado == 0:
                mensaje = "Campo magnético detectado"
            else:
                mensaje = "No se detecta campo magnético"
            mqtt_client.publish(MQTT_TOPIC, mensaje)
            print("Mensaje enviado:", mensaje)
            estado_anterior = estado
    
    time.sleep(0.1)  # Retardo para evitar rebotes