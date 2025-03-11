import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion6/joystick"

# 🎮 Configurar pines del joystick
pin_x = machine.ADC(machine.Pin(34))
pin_y = machine.ADC(machine.Pin(35))

# Configurar resolución del ADC (ESP32)
pin_x.width(machine.ADC.WIDTH_10BIT)  # Rango de 0 - 1023
pin_y.width(machine.ADC.WIDTH_10BIT)

pin_x.atten(machine.ADC.ATTN_11DB)  # Extiende el rango hasta ~3.3V
pin_y.atten(machine.ADC.ATTN_11DB)

# Valores de referencia para el centro del joystick
CENTRO_MIN = 300  # Mínimo para considerar "en el centro"
CENTRO_MAX = 300  # Máximo para considerar "en el centro"

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("✅ Conectado a WiFi")

# 📡 Conectar a MQTT
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("✅ Conectado al broker MQTT")

# Última dirección enviada para evitar repetición innecesaria
ultima_direccion = ""

# 🎮 Loop principal
while True:
    x_value = pin_x.read()
    y_value = pin_y.read()
    direccion = ""

    # Determinar dirección del joystick
    if x_value < CENTRO_MIN:
        direccion = "Izquierda"
    elif x_value > CENTRO_MAX:
        direccion = "Derecha"

    if y_value < CENTRO_MIN:
        direccion = "Abajo"
    elif y_value > CENTRO_MAX:
        direccion = "Arriba"

    # Solo enviar si la dirección ha cambiado
    if direccion and direccion != ultima_direccion:
        mqtt_client.publish(MQTT_TOPIC, direccion)
        print(f"📡 Dirección enviada: {direccion}")
        ultima_direccion = direccion

    time.sleep(0.2)  # Pequeña pausa para evitar lecturas excesivas