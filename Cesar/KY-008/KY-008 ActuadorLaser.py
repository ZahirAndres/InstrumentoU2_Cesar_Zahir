import network
import time
import machine
from umqtt.simple import MQTTClient

# Configuración de la red WiFi
SSID = "Cesar"
PASSWORD = "123456789"

# Configuración de MQTT
MQTT_BROKER = "192.168.170.135"
MQTT_TOPIC = "zarm/sesion3"
CLIENT_ID = "ESP32_LASER"

# Configuración del módulo láser KY-008
laser = machine.Pin(16, machine.Pin.OUT)  # Conectado al GPIO 16

# Conexión a la red WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando a WiFi...", end="")

    while not wlan.isconnected():
        print(".", end="")
        time.sleep(1)

    print("\nConectado a WiFi:", wlan.ifconfig())

# Conectar a MQTT con manejo de errores
def conectar_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER)
    while True:
        try:
            client.connect()
            print("Conectado al broker MQTT:", MQTT_BROKER)
            return client
        except OSError as e:
            print("Error al conectar a MQTT, reintentando en 5 segundos...")
            time.sleep(5)

# Programa principal con reconexión automática
def main():
    conectar_wifi()
    client = conectar_mqtt()

    while True:
        try:
            # Intentar enviar mensajes solo si el cliente está conectado
            try:
                # Enviar mensaje de encendido del láser
                laser.value(1)
                mensaje = "Láser encendido"
                client.publish(MQTT_TOPIC, mensaje)
                print("Mensaje enviado:", mensaje)
                time.sleep(2)

                # Enviar mensaje de apagado del láser
                laser.value(0)
                mensaje = "Láser apagado"
                client.publish(MQTT_TOPIC, mensaje)
                print("Mensaje enviado:", mensaje)
                time.sleep(2)

            except OSError as e:
                print("Error en la conexión MQTT, reconectando...")
                client = conectar_mqtt()

        except OSError as e:
            print("Error en la conexión MQTT, reconectando...")
            client = conectar_mqtt()

# Ejecutar el programa automáticamente
main()
