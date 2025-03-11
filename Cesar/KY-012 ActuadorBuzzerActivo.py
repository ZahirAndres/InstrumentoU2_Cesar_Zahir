import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
# ==============================
SSID = "Cesar"
PASSWORD = "123456789"

MQTT_BROKER = "192.168.71.135"
MQTT_TOPIC = "zarm/sesion4"

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
# Configuración del Buzzer Pasivo
# ==============================
# Conecta:
# - Terminal positivo del buzzer al GPIO 12 (PWM)
# - Terminal negativo a GND
buzzer = PWM(Pin(12))
buzzer.freq(2000)  # Frecuencia en Hz (puedes ajustarla)
buzzer.duty(0)     # Inicia con el buzzer apagado

def beep(duration=0.5, freq=2000, duty=800):
    """
    Activa el buzzer generando un tono con la frecuencia y duty especificados
    durante 'duration' segundos.
    """
    buzzer.freq(freq)
    buzzer.duty(duty)  # Aumenta el duty para mayor volumen
    time.sleep(duration)
    buzzer.duty(0)  # Apaga el buzzer

# ==============================
# Loop principal: Emisión periódica del beep
# ==============================
while True:
    beep(0.5)  # Emite un beep de 0.5 segundos
    mqtt_client.publish(MQTT_TOPIC, "Buzzer activado con mayor volumen")
    print("Buzzer activado")
    time.sleep(5)  # Espera 5 segundos antes de volver a emitir el beep