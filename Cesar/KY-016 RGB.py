import network
import time
import machine
from umqtt.simple import MQTTClient

# 📌 Configuración WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configuración del broker MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion2"  # Cambié el tópico para reflejar el LED

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    print("Conectando a WiFi...")
    time.sleep(1)
print("✅ Conectado a WiFi!")

# 📡 Conectar a MQTT
client = MQTTClient("ESP32", MQTT_BROKER)
client.connect()
print("✅ Conectado a MQTT!")

# 📌 Configurar el módulo KY-009 (LED RGB)
# Se usan PWM en 3 pines: ajusta estos pines según tu conexión.
led_r = machine.PWM(machine.Pin(13), freq=500, duty=0)
led_g = machine.PWM(machine.Pin(12), freq=500, duty=0)
led_b = machine.PWM(machine.Pin(14), freq=500, duty=0)

# Definir algunos colores (valores de 0 a 1023 para PWM)
# Se asume LED de cátodo común
colores = [
    {"nombre": "Rojo",    "r": 1023, "g": 0,    "b": 0},
    {"nombre": "Verde",   "r": 0,    "g": 1023, "b": 0},
    {"nombre": "Azul",    "r": 0,    "g": 0,    "b": 1023},
    {"nombre": "Amarillo","r": 1023, "g": 1023, "b": 0},
    {"nombre": "Cian",    "r": 0,    "g": 1023, "b": 1023},
    {"nombre": "Magenta", "r": 1023, "g": 0,    "b": 1023},
    {"nombre": "Blanco",  "r": 1023, "g": 1023, "b": 1023},
    {"nombre": "Apagado", "r": 0,    "g": 0,    "b": 0}
]

while True:
    for color in colores:
        # Actualizar el PWM para cambiar el color del LED
        led_r.duty(color["r"])
        led_g.duty(color["g"])
        led_b.duty(color["b"])
        
        mensaje = "LED Color: {} (R:{} G:{} B:{})".format(
            color["nombre"], color["r"], color["g"], color["b"]
        )
        print("📡 Enviando: " + mensaje)
        client.publish(MQTT_TOPIC, mensaje)
        
        time.sleep(1)  # Espera 1 segundo entre cada cambio de color