import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Configuración Wi-Fi
wifi_ssid = "Ubee59E8-2.4G"  #nombre de la red-b
wifi_password = "5F99F359E8"  #contraseña

# Configura tu broker MQTT (IP de Node-RED)
mqtt_broker = "192.168.0.13"  # IP de tu servidor Node-RED de la Rassberry
mqtt_port = 1883 #Puerto del broker dentro del archivo .conf
mqtt_topic = "zarm/sensor" #topico asigado de mosquitto
mqtt_client_id = "sensor_{}".format(int(time.time()))

# Pines del LED RGB
LED_RED_PIN = 19
LED_GREEN_PIN = 21
LED_BLUE_PIN = 22

# Configuración de los LEDs (PWM con duty cycle en 16 bits)
led_red = PWM(Pin(LED_RED_PIN), freq=1000)
led_green = PWM(Pin(LED_GREEN_PIN), freq=1000)
led_blue = PWM(Pin(LED_BLUE_PIN), freq=1000)

# Función para cambiar el estado del LED RGB
def change_led_state(state):
    if state == "true":
        # Encender el LED RGB (blanco)
        led_red.duty_u16(65535)
        led_green.duty_u16(65535)
        led_blue.duty_u16(65535)
    elif state == "false":
        # Apagar el LED RGB
        led_red.duty_u16(0)
        led_green.duty_u16(0)
        led_blue.duty_u16(0)

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print('Conexión Wi-Fi exitosa:', wlan.ifconfig())
        return True
    else:
        print("Error: No se pudo conectar a Wi-Fi")
        return False

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient(mqtt_client_id, mqtt_broker, mqtt_port)
        client.set_callback(message_callback)
        client.connect()
        client.subscribe(mqtt_topic)
        print("Conectado al broker MQTT y suscrito a", mqtt_topic)
        return client
    except Exception as e:
        print("Error al conectar al broker MQTT:", e)
        return None

# Callback para manejar mensajes MQTT
def message_callback(topic, msg):
    state = msg.decode().strip()  # Decodifica y elimina espacios en blanco
    print("Mensaje recibido en '{}': {}".format(topic.decode(), state))
    
    change_led_state(state)  # Llamar a la función para cambiar el LED

# Main
if connect_wifi():
    client = connect_mqtt()
    if client:
        while True:
            client.check_msg()  # Verifica si hay nuevos mensajes
            time.sleep(1)  # Espera un segundo entre verificaciones
else:
    print("No se pudo establecer conexión Wi-Fi. Reinicia el dispositivo.")
