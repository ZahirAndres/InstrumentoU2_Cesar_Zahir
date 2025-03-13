import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/mq/6"

# 📌 Configurar sensor MQ-6
sensor_analogico = machine.ADC(machine.Pin(34))  # Entrada analógica
sensor_analogico.atten(machine.ADC.ATTN_11DB)   # Rango de 0-3.3V
sensor_digital = machine.Pin(18, machine.Pin.IN)  # Salida digital

# 📡 Conectar a WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

while not wifi.isconnected():
    time.sleep(1)

print("✅ Conectado a WiFi")

# 📡 Conectar a MQTT
def conectar_mqtt():
    global mqtt_client
    try:
        mqtt_client = MQTTClient("ESP32", MQTT_BROKER)
        mqtt_client.connect()
        print("✅ Conectado al broker MQTT")
    except Exception as e:
        print("❌ Error al conectar MQTT:", e)
        time.sleep(5)
        conectar_mqtt()

conectar_mqtt()

# 🔄 Loop principal para monitorear el gas
while True:
    try:
        valor_analogico = sensor_analogico.read()  # Leer nivel de gas
        gas_detectado = valor_analogico     # 1 = No gas, 0 = Gas detectado

        if gas_detectado >= 1000:  # Se detecta gas
            print(f"⚠ Gas detectado - Nivel: {valor_analogico}")
            mqtt_client.publish(MQTT_TOPIC, f"Gas detectado - Nivel: {valor_analogico}")
        else:
            print(f"✅ No hay gas - Nivel: {valor_analogico}")
            mqtt_client.publish(MQTT_TOPIC, f"No hay gas - Nivel: {valor_analogico}")

        time.sleep(1)  # Pausa para evitar spam

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla