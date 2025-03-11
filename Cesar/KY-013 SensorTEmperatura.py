import network
import time
from machine import ADC, Pin
from umqtt.simple import MQTTClient
import math

# ==============================
# Configuración de WiFi y MQTT
# ==============================
SSID = "Cesar"
PASSWORD = "123456789"
MQTT_BROKER = "192.168.71.135"
MQTT_TOPIC = "zarm/sesion5"

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

# ==============================
# Configuración del sensor KY-013
# ==============================
sensor = ADC(Pin(34))
sensor.atten(ADC.ATTN_11DB)      # Rango de 0 a ~3.3V
sensor.width(ADC.WIDTH_12BIT)    # Resolución de 12 bits (0 a 4095)

# ==============================
# Parámetros del termistor NTC
# ==============================
R1 = 10000  # Resistencia de 10kΩ en el divisor de voltaje
BETA = 3950  # Coeficiente beta del termistor
T0 = 298.15  # Temperatura de referencia en Kelvin (25°C)

def adc_to_temp(adc_value):
    """ Convierte la lectura ADC en temperatura usando Steinhart-Hart. """
    if adc_value == 0 or adc_value == 4095:  # Evitar valores fuera de rango
        return None
    
    voltage = adc_value * (3.3 / 4095)  # Convertir ADC a voltaje
    resistance = (R1 * voltage) / (3.3 - voltage)  # Calcular resistencia
    
    temp_kelvin = 1 / ((1 / T0) + (math.log(resistance / R1) / BETA))  # Steinhart-Hart
    temp_celsius = temp_kelvin - 273.15  # Convertir a Celsius
    
    return round(temp_celsius, 2)

# ==============================
# Loop principal: Lectura y envío
# ==============================
while True:
    lectura_adc = sensor.read()
    print("Valor ADC:", lectura_adc)
    mqtt_client.publish(MQTT_TOPIC, str(lectura_adc))  # Enviar temperatura en °C
    temperatura = adc_to_temp(lectura_adc)  # Convertir a °C
    if temperatura is not None:
        mqtt_client.publish(MQTT_TOPIC, str(temperatura))  # Enviar temperatura en °C
        print("Temperatura enviada:", temperatura, "°C")
    else:
        print("Error en la lectura del sensor")

    time.sleep(2)
