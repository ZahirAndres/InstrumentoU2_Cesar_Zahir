import network
import time
from machine import Pin, PWM, time_pulse_us
from umqtt.simple import MQTTClient

# Configuración Wi-Fi
wifi_ssid = "Ubee59E8-2.4G"  # nombre de la red
wifi_password = "5F99F359E8"  # contraseña

# Configura tu broker MQTT
mqtt_broker = "192.168.0.13"  # IP de Raspberry Pi
mqtt_port = 1883 #Puerto de la Rasberry 
mqtt_topic = "zarm/sensor"  # Topico 
mqtt_client_id = "sensor_{}".format(int(time.time())) #nombre del cliente que se conecta

# Pines del sensor ultrasónico HC-SR04
TRIGGER_PIN = 5
ECHO_PIN = 18

trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Pines del LED RGB
LED_RED_PIN = 19
LED_GREEN_PIN = 21
LED_BLUE_PIN = 22

# Configuración de los LEDs (PWM para controlar el brillo)
led_red = PWM(Pin(LED_RED_PIN), freq=1000, duty=0)
led_green = PWM(Pin(LED_GREEN_PIN), freq=1000, duty=0)
led_blue = PWM(Pin(LED_BLUE_PIN), freq=1000, duty=0)

# Función para cambiar el color del LED RGB según la distancia
def change_led_color(distance):
    # Normalizamos la distancia a un rango de 0 a 1023 para PWM (0-100% de brillo)
    if distance is not None:
        if distance < 10:
            # Rojo
            led_red.duty(1023)
            led_green.duty(0)
            led_blue.duty(0)
        elif 10 <= distance < 30:
            # Amarillo (rojo + verde)
            led_red.duty(1023)
            led_green.duty(512)
            led_blue.duty(0)
        elif 30 <= distance < 50:
            # Verde
            led_red.duty(0)
            led_green.duty(1023)
            led_blue.duty(0)
        elif 50 <= distance < 80:
            # Cyan (verde + azul)
            led_red.duty(0)
            led_green.duty(1023)
            led_blue.duty(512)
        elif 80 <= distance < 100:
            # Azul
            led_red.duty(0)
            led_green.duty(0)
            led_blue.duty(1023)
        else:
            # Blanco (rojo + verde + azul)
            led_red.duty(1023)
            led_green.duty(1023)
            led_blue.duty(1023)

# Conexión Wi-Fi con manejo de errores
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        
        timeout = 10  # Esperar hasta 10 segundos para la conexión
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print('Conexión Wi-Fi exitosa:', wlan.ifconfig())
    else:
        print("Error: No se pudo conectar a Wi-Fi")
        return False
    return True

# Conexión MQTT con manejo de errores
def connect_mqtt():
    try:
        client = MQTTClient(mqtt_client_id, mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar al broker MQTT:", e)
        return None

# Función para medir la distancia con el sensor HC-SR04
def measure_distance():
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()

    pulse_time = time_pulse_us(echo, 1, 30000)  # Tiempo en microsegundos
    if pulse_time < 0:
        return None  # Fallo en la medición

    distance = (pulse_time / 2) * 0.0343  # Conversión a cm
    return round(distance, 2)

# Enviar datos del sensor por MQTT solo si la diferencia es >= 1.5 cm
def publish_data(client, last_distance):
    if client is None:
        print("MQTT no está conectado")
        return last_distance

    try:
        distance = measure_distance()
        if distance is not None:
            if last_distance is None or abs(distance - last_distance) >= 1.5:
                payload = "{}".format(distance)
                client.publish(mqtt_topic, payload)
                print("Distancia enviada:", payload, "cm") #mensaje de control sobre lo que recibe el sensor
                change_led_color(distance)  # Cambiar el color del LED según la distancia
                return distance  # Actualizar el último valor enviado
            else:
                print("Distancia sin cambios significativos, no se envía") #evitar enviar demasiada información
                return last_distance
        else:
            print("Error en la medición de distancia") # Atrapamos posibles errores y excepciones
            return last_distance
    except Exception as e:
        print("Error al medir la distancia:", e)
        return last_distance

# Main
if connect_wifi():  # Conectar a Wi-Fi
    client = connect_mqtt()  # Conectar a MQTT
    last_distance = None  # Última distancia medida

    while True:
        last_distance = publish_data(client, last_distance)  # Enviar datos solo si cambia >= 1.5 cm
        time.sleep(2)  # Medir cada 2 segundos
else:
    print("No se pudo establecer conexión Wi-Fi. Reinicia el dispositivo.")
