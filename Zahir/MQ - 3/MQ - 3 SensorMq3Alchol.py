import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# ==============================
# Configuración de conexiones
# ==============================

# 📌 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar MQTT
MQTT_BROKER = "192.168.71.135"
MQTT_TOPIC = "zarm/sesion4"

# 📌 Configurar el sensor MQ-3 en el ADC (ej. pin 34)
mq3_sensor = ADC(Pin(34))
mq3_sensor.atten(ADC.ATTN_11DB)      # Permite leer voltajes de 0 a ~3.3V
mq3_sensor.width(ADC.WIDTH_12BIT)    # Resolución de 12 bits (0-4095)

# ==============================
# Conexión a WiFi y MQTT
# ==============================

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)
print("Conectado a WiFi en ESP32")

# Conectar al broker MQTT
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# ==============================
# Loop principal: Lectura y detección de cambios
# ==============================

# Umbral para considerar un cambio significativo (ajusta según tus necesidades)
UMBRAL_CAMBIO = 50

# Variable para almacenar la última lectura enviada
ultima_lectura = None

while True:
    lectura = mq3_sensor.read()  # Leer sensor
    print("Lectura actual:", lectura)  # Mostrar siempre el valor
    time.sleep(2)


    # En la primera iteración, asignamos la lectura inicial
    if ultima_lectura is None:
        ultima_lectura = lectura
        mqtt_client.publish(MQTT_TOPIC, str(lectura))
        print("Lectura inicial enviada:", lectura)
    else:
        # Si la diferencia supera el umbral, se detecta un cambio
        if abs(lectura - ultima_lectura) >= UMBRAL_CAMBIO:
            mensaje = "Cambio detectado: {} (anterior: {})".format(lectura, ultima_lectura)
            mqtt_client.publish(MQTT_TOPIC, str(lectura))
            print(mensaje)
            ultima_lectura = lectura

    time.sleep(2)  # Delay entre lecturas