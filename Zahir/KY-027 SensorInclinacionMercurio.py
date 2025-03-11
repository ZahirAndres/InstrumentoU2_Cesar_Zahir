
import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.139.135"
MQTT_TOPIC = "zarm/sesion1/inclinacionMercurioLuminoso"

# 📌 Configurar sensor KY-027 en GPIO25 (salida digital)
sensor = machine.Pin(25, machine.Pin.IN)
led = machine.Pin(26, machine.Pin.OUT)  # LED interno del KY-027

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

# Último estado enviado
ultimo_estado = None

# 🔄 Loop principal
while True:
    estado = sensor.value()  # 1 = Vertical, 0 = Inclinado

    if estado == 0 and ultimo_estado != "Inclinado":
        mqtt_client.publish(MQTT_TOPIC, "Inclinado")
        print("📡 Enviado: Inclinado")
        led.value(1)  # Encender LED
        ultimo_estado = "Inclinado"

    elif estado == 1 and ultimo_estado != "Vertical":
        mqtt_client.publish(MQTT_TOPIC, "Vertical")
        print("📡 Enviado: Vertical")
        led.value(0)  # Apagar LED
        ultimo_estado = "Vertical"

    time.sleep(0.2)  # Pequeño delay para evitar envíos excesivos