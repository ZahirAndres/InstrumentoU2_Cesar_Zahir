import network
import time
import machine
import math
from umqtt.simple import MQTTClient

# 📌 Configurar conexión WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📌 Configurar broker MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/temperatura"

# 📌 Configurar termistor en entrada analógica (GPIO 34)
sensor_temp = machine.ADC(machine.Pin(34))  # GPIO 34 (ADC1)
sensor_temp.atten(machine.ADC.ATTN_11DB)  # Rango 0 - 3.3V

# 📌 Parámetros del termistor
R_SERIE = 10000  # Resistencia en serie (10kΩ)
BETA = 3950  # Coeficiente Beta del termistor
T0 = 298.15  # Temperatura de referencia en Kelvin (25°C)
R0 = 10000  # Resistencia del termistor a 25°C (10kΩ)

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

def leer_temperatura():
    lectura = sensor_temp.read()  # Leer valor ADC (0 - 4095)
    voltaje = lectura * (3.3 / 4095)  # Convertir a voltaje

    if voltaje <= 0 or voltaje >= 3.3:  # Validación de rango
        return None

    # Calcular resistencia del termistor
    resistencia = R_SERIE * (voltaje / (3.3 - voltaje))

    # Aplicar ecuación de Steinhart-Hart
    temperatura_kelvin = 1 / ((1 / T0) + (math.log(resistencia / R0) / BETA))
    temperatura_celsius = temperatura_kelvin - 273.15  # Convertir a °C

    return temperatura_celsius

# 📌 Variable para guardar la última temperatura registrada
ultima_temperatura = None
diferencia_umbral = 0.1  # 🔥 Enviar solo si la diferencia es ≥ 0.5°C

while True:
    temperatura = leer_temperatura()

    if temperatura is not None:
        if ultima_temperatura is None or abs(temperatura - ultima_temperatura) >= diferencia_umbral:
            mensaje = f"🔥 Cambio detectado: {temperatura:.2f}°C"
            print(f"📡 Enviando: {mensaje}")
            client.publish(MQTT_TOPIC, mensaje)  # Enviar temperatura a MQTT
            ultima_temperatura = temperatura  # Actualizar última temperatura

    time.sleep(1)  # Esperar 1 segundo
