import network
import time
from machine import ADC, Pin
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
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
# Configuración de la Fotoresistencia
# ==============================
# Se asume que la fotoresistencia (en configuración de divisor de voltaje) se conecta al ADC del pin GPIO34
fotoresistor = ADC(Pin(34))
fotoresistor.atten(ADC.ATTN_11DB)      # Permite medir un rango de voltaje de 0 a ~3.3V
fotoresistor.width(ADC.WIDTH_12BIT)    # Resolución de 12 bits (0 a 4095)

# ==============================
# Loop principal: Lectura y detección de cambios
# ==============================
UMBRAL_CAMBIO = 50  # Define el umbral para considerar un cambio significativo
ultima_lectura = None

while True:
    lectura = fotoresistor.read()  # Se lee el valor analógico

    # En la primera lectura se envía el valor inicial
    if ultima_lectura is None:
        ultima_lectura = lectura
        mqtt_client.publish(MQTT_TOPIC, str(lectura))
        print("Lectura inicial enviada:", lectura)
    else:
        # Solo se envía un mensaje vía MQTT si la diferencia supera el umbral definido
        if abs(lectura - ultima_lectura) >= UMBRAL_CAMBIO:
            mensaje = "Cambio detectado: {} (anterior: {})".format(lectura, ultima_lectura)
            mqtt_client.publish(MQTT_TOPIC, str(lectura))
            print(mensaje)
            ultima_lectura = lectura

    time.sleep(2)  # Delay entre lecturas