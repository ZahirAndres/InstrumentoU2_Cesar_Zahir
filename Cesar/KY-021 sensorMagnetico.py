import machine
import time
from umqtt.simple import MQTTClient

# Configurar WiFi
import network
SSID = "Cesar"
PASSWORD = "123456789"

# Configurar MQTT
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion6"

# Configurar sensor Reed Switch en GPIO15 con resistencia pull-up
reed_switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("Conectado a WiFi en ESP32")

# Conectar a MQTT
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
mqtt_client.connect()
print("Conectado al broker MQTT")

# Variables de control para evitar detección múltiple por rebote
last_state = reed_switch.value()
last_time = time.ticks_ms()

def check_reed_switch():
    global last_state, last_time
    
    current_state = reed_switch.value()
    current_time = time.ticks_ms()
    
    # Solo envía mensaje si hay un cambio de estado y ha pasado suficiente tiempo (evitar rebotes)
    if current_state != last_state and time.ticks_diff(current_time, last_time) > 200:
        last_time = current_time
        last_state = current_state
        
        if current_state == 0:
            print("¡Imán detectado! (Cerrado)")
            mqtt_client.publish(MQTT_TOPIC, "CERRADO")
        else:
            print("¡Imán alejado! (Abierto)")
            mqtt_client.publish(MQTT_TOPIC, "ABIERTO")

# Loop principal
while True:
    check_reed_switch()
    time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga del procesador