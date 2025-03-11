import network
import time
from machine import Pin, PWM
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
# Configuración del Buzzer Pasivo
# ==============================
# Conecta el terminal positivo del buzzer al GPIO12 (PWM) y el negativo a GND
buzzer = PWM(Pin(12))
buzzer.duty(0)  # Inicialmente apagado

# Función para reproducir una nota
def play_tone(frequency, duration):
    if frequency == 0:
        # Si la frecuencia es 0, se genera un silencio
        time.sleep(duration)
    else:
        buzzer.freq(frequency)
        buzzer.duty(512)  # Ajusta el duty (volumen); valor máximo es 1023
        time.sleep(duration)
        buzzer.duty(0)  # Apaga el buzzer tras la nota
    time.sleep(0.05)  # Breve pausa entre notas

# ==============================
# Definición de notas y melodía
# ==============================
notes = {
    'C4': 261,
    'D4': 293,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 493,
    'C5': 523,
}

# Ejemplo: "Mary Had a Little Lamb"
melody = [
    (notes['E4'], 0.4),
    (notes['D4'], 0.4),
    (notes['C4'], 0.4),
    (notes['D4'], 0.4),
    (notes['E4'], 0.4),
    (notes['E4'], 0.4),
    (notes['E4'], 0.8),
    (notes['D4'], 0.4),
    (notes['D4'], 0.4),
    (notes['D4'], 0.8),
    (notes['E4'], 0.4),
    (notes['G4'], 0.4),
    (notes['G4'], 0.8),
]

# ==============================
# Loop principal: Reproducción de melodía con registro MQTT
# ==============================
while True:
    # Indica que la melodía está por comenzar
    mqtt_client.publish(MQTT_TOPIC, "Melody started")
    print("Melody started")
    
    # Reproduce la melodía nota a nota
    for note, duration in melody:
        play_tone(note, duration)
    
    # Indica que la melodía ha finalizado
    mqtt_client.publish(MQTT_TOPIC, "Melody stopped")
    print("Melody stopped")
    
    time.sleep(1)  # Pausa antes de repetir la melodía