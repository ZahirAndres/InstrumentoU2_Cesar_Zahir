import time
import network
import machine
import onewire
import ds18x20
from umqtt.simple import MQTTClient

# ==============================
# Configuración de WiFi
# ==============================
SSID = "Cesar"
PASSWORD = "123456789"

# ==============================
# Configuración de MQTT
# ==============================
MQTT_BROKER = "192.168.71.135"
MQTT_CLIENT_ID = "esp32_ds18b20"
MQTT_TOPIC = "zarm/sesion5"
MQTT_PORT = 1883

# ==============================
# Configuración del sensor DS18B20
# ==============================
pin_sensor = machine.Pin(15)  # Prueba con GPIO4 si hay problemas
sensor = ds18x20.DS18X20(onewire.OneWire(pin_sensor))

# Buscar sensores en el bus 1-Wire
roms = sensor.scan()
if not roms:
    print("⚠ No se encontraron sensores DS18B20. Verifica la conexión.")
else:
    print("✅ Sensor detectado:", roms)

# ==============================
# Función para conectar WiFi
# ==============================
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\n✅ WiFi conectada:", wifi.ifconfig())

# ==============================
# Función para conectar MQTT
# ==============================
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("✅ Conectado al broker MQTT:", MQTT_BROKER)
    return client

# ==============================
# Inicio del programa
# ==============================
conectar_wifi()
client = conectar_mqtt()

# ==============================
# Loop principal: Leer temperatura y enviar por MQTT
# ==============================
try:
    while True:
        sensor.convert_temp()  # Iniciar medición
        time.sleep(1)  # Esperar la conversión

        for rom in roms:
            temp_c = sensor.read_temp(rom)  # Leer temperatura
            temp_str = "{:.2f}".format(temp_c)  # Formato correcto

            print("🌡 Temperatura:", temp_str, "°C")  # Mostrar en consola
            client.publish(MQTT_TOPIC, temp_str)  # Enviar a MQTT

        time.sleep(2)  # Enviar temperatura cada 5 segundos

except Exception as e:
    print("❌ Error:", e)
