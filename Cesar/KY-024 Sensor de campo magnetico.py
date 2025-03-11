import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuración de WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# Configuración del broker MQTT
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion6/SensorCampoMagnetico"

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)
while not wifi.isconnected():
    time.sleep(1)
print("Conectado a WiFi")

# Conectar al broker MQTT
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# Configurar el sensor magnético KY-024 (usamos la salida digital)
# Se asume: sensor.value() == 0  => campo magnético detectado
#            sensor.value() == 1  => sin campo magnético
sensor = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)

# Variable para almacenar el estado anterior
ultimo_estado = None

while True:
    try:
        estado_actual = sensor.value()

        if estado_actual != ultimo_estado:
            if estado_actual == 1:
                mensaje = "Campo magnético detectado"
            else:
                mensaje = "Campo magnético no detectado"
            print(mensaje)
            mqtt_client.publish(MQTT_TOPIC, mensaje)
            ultimo_estado = estado_actual

        time.sleep(0.2)

    except OSError as e:
        print("Error en la conexión MQTT, reconectando...")
        mqtt_client.connect()
        print("Reconectado al broker MQTT")
        time.sleep(2)  # Espera un poco antes de intentar de nuevo
