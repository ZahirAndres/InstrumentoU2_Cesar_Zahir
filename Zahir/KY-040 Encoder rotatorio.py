import machine
import time
import network
from umqtt.simple import MQTTClient

# 📡 Configurar WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# 📡 Configurar MQTT
MQTT_BROKER = "192.168.111.135"
MQTT_TOPIC = "zarm/sesion8/rotatorio"

# 📌 Configurar Pines del KY-040
clk = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
dt = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
sw = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)

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

# 🔄 Variables del encoder
ultimo_estado_clk = clk.value()

# 🔄 Loop principal para detectar giro y botón
while True:
    try:
        estado_clk = clk.value()

        if estado_clk != ultimo_estado_clk:  # Detectar cambio en CLK
            if dt.value() != estado_clk:
                print("⏩ Girando en sentido horario (CW)")
                mqtt_client.publish(MQTT_TOPIC, "Giro horario")
            else:
                print("⏪ Girando en sentido antihorario (CCW)")
                mqtt_client.publish(MQTT_TOPIC, "Giro antihorario")

        ultimo_estado_clk = estado_clk

        if sw.value() == 0:  # Si se presiona el botón
            print("🔘 Botón presionado")
            mqtt_client.publish(MQTT_TOPIC, "Botón presionado")
            time.sleep(0.3)  # Pequeña pausa para evitar múltiples envíos

        time.sleep(0.01)  # Pequeña pausa para evitar sobrecarga

    except Exception as e:
        print("❌ Error en la ejecución:", e)
        conectar_mqtt()  # Intentar reconectar si falla