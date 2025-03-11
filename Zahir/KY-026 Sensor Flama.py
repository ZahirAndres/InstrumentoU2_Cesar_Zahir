import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.90.135"
MQTT_TOPIC = "zarm/sesion7/SensorFlama"

# 📌 Configurar sensor KY-026
sensor_digital = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)  # D0 - Salida digital
sensor_analogico = machine.ADC(machine.Pin(34))  # A0 - Salida analógica
sensor_analogico.atten(machine.ADC.ATTN_11DB)  # Rango de 0V a 3.3V

estado_anterior = sensor_digital.value()

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

# 🔄 Loop para detectar flama
while True:
    try:
        estado_actual = sensor_digital.value()
        valor_analogico = sensor_analogico.read()  # Lectura analógica (0-4095)

        # Ajuste del umbral de detección basado en el sensor analógico
        if valor_analogico < 1000:  # Ajusta este valor según la sensibilidad deseada
            estado_actual = 0
        else:
            estado_actual = 1

        # Si el estado cambia, enviamos un mensaje
        if estado_actual != estado_anterior:
            if estado_actual == 0:  # Flama detectada
                print(f"🔥 ¡Fuego detectado! (Valor analógico: {valor_analogico})")
                mqtt_client.publish(MQTT_TOPIC, "🔥 ¡Fuego detectado!")
            else:
                print(f"❌ No hay fuego (Valor analógico: {valor_analogico})")
                mqtt_client.publish(MQTT_TOPIC, "❌ No hay fuego")

            estado_anterior = estado_actual  # Guardar estado

        time.sleep(0.5)  # Pequeño delay para evitar saturación

    except Exception as e:
        print("❌ Error en la detección:", e)
        conectar_mqtt()  # Intentar reconectar en caso de error