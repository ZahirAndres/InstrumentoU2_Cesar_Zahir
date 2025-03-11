import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# 📌 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion3"

# 📌 Configurar LM35 en un pin ADC (ej. GPIO 32)
lm35 = ADC(Pin(32))
lm35.atten(ADC.ATTN_11DB)  # Rango completo (0-3.6V aprox.)
lm35.width(ADC.WIDTH_12BIT)  # Resolución 12 bits (0-4095)

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
while True:
    try:
        # Leer el valor ADC del LM35 (0-4095)
        adc_value = lm35.read()
        # Convertir a voltaje (asumiendo Vref = 3.3V)
        voltage = (adc_value / 4095) * 3.3
        # LM35: 10 mV por °C => Temperatura (°C) = (voltaje en V * 100)
        temperatura = voltage * 100

        mensaje = "Temperatura: {:.2f}°C".format(temperatura)
        mqtt_client.publish(MQTT_TOPIC, mensaje)
        print(f"Mensaje enviado: {mensaje}")

    except OSError as e:
        print(f"Error leyendo LM35: {e}, reconectando MQTT...")
        conectar_mqtt()

    time.sleep(2)  # Esperar 2 segundos entre lecturas
