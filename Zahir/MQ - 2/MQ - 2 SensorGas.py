import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi y MQTT
# ==============================

SSID = "Cesar"               # Nombre de la red WiFi
PASSWORD = "123456789"       # Contraseña de la red WiFi
MQTT_BROKER = "192.168.71.135"  # Dirección del broker MQTT (ajusta según tu red)
MQTT_TOPIC = "zarm/sesion5"  # Tópico donde se publicarán los datos

# ==============================
# Configuración del sensor MQ-2
# ==============================
# Conectar:
# - VCC a 5V (o 3.3V, según tu módulo)
# - GND a tierra
# - AOUT a GPIO34 (para lectura analógica)

mq2_sensor = ADC(Pin(34))
mq2_sensor.atten(ADC.ATTN_11DB)      # Rango de 0 a ~3.3V
mq2_sensor.width(ADC.WIDTH_12BIT)    # Resolución de 12 bits (0 a 4095)

# ==============================
# Conexión a WiFi
# ==============================
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Conectando a WiFi...", end="")
while not wifi.isconnected():
    time.sleep(1)
    print(".", end="")
print("\n✅ Conectado a WiFi:", wifi.ifconfig())

# ==============================
# Conexión al broker MQTT
# ==============================
mqtt_client = MQTTClient("ESP32", MQTT_BROKER)

try:
    mqtt_client.connect()
    print("✅ Conectado al broker MQTT")
except Exception as e:
    print("❌ Error al conectar con MQTT:", e)
    raise SystemExit()  # Detener ejecución si no se conecta

# ==============================
# Loop principal: Lectura y detección de cambios
# ==============================

UMBRAL_CAMBIO = 10   # Umbral de cambio para enviar datos
ultima_lectura = None

print("📡 Iniciando lectura del sensor...")

while True:
    lectura = mq2_sensor.read()  # Leer el valor analógico del sensor

    # En la primera lectura, inicializa la variable y envía el valor
    if ultima_lectura is None:
        ultima_lectura = lectura
        mqtt_client.publish(MQTT_TOPIC, str(lectura))
        print("📤 Lectura inicial enviada:", lectura)
    else:
        # Enviar datos solo si hay un cambio significativo
        if abs(lectura - ultima_lectura) >= UMBRAL_CAMBIO:
            mensaje = "📢 Cambio detectado: {} (antes: {})".format(lectura, ultima_lectura)
            mqtt_client.publish(MQTT_TOPIC, str(lectura))
            print(mensaje)
            ultima_lectura = lectura

    time.sleep(2)  # Espera de 2 segundos entre lecturas
