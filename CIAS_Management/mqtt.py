import paho.mqtt.client as mqtt
from gpiozero import LED, Servo
from mfrc522 import SimpleMFRC522
from time import sleep
import RPi.GPIO as GPIO
#hmm
# Configuración de los pines
green_led = LED(14)  # LED verde
red_led = LED(15)    # LED rojo
servo = Servo(18)    # Servo motor
rfid_reader = SimpleMFRC522()  # Inicialización del lector RFID

# Variables de estado
authorized_uid = [0x43, 0x39, 0x8F, 0xE2]  # UID autorizado en formato hexadecimal

# Configuración inicial
red_led.on()
green_led.off()
servo.min()  # Posición inicial del servomotor (0 grados)

# Configuración del cliente MQTT
client = mqtt.Client()
client.connect("test.mosquitto.org", 1883, 60)

# Inicia el loop MQTT en segundo plano
client.loop_start()

# Función para enviar notificaciones MQTT
def publish_status(client, message):
    client.publish("acceso/estado", message)

# Verifica si un UID es autorizado
def check_uid(uid):
    return uid == authorized_uid

# Cambia el estado de los LEDs y el servomotor
def toggle_leds_and_servo(access_granted):
    if access_granted:
        # Acceso permitido
        red_led.off()
        green_led.on()
        servo.max()  # Servo en 90 grados
        publish_status(client, "Acceso permitido. LED verde encendido. Servo en 90 grados.")
        sleep(3)  # Espera antes de volver a la posición inicial
        servo.min()  # Servo vuelve a 0 grados
        publish_status(client, "Servo volvió a 0 grados. LED verde apagado.")
        green_led.off()
    else:
        # Acceso denegado
        green_led.off()
        red_led.on()
        servo.min()  # Servo permanece en 0 grados
        publish_status(client, "Acceso denegado. LED rojo encendido. Servo en 0 grados.")

# Lee la tarjeta RFID
def read_rfid():
    try:
        id, text = rfid_reader.read()
        publish_status(client, f"Intento de acceso con tarjeta UID: {id}.")
        # Verifica si el UID es autorizado
        if id == int(''.join(format(x, '02x') for x in authorized_uid), 16):
            return True
        else:
            return False
    except Exception as e:
        publish_status(client, f"Error leyendo RFID: {str(e)}")
        return False

# Loop principal
try:
    while True:
        # Revisión del RFID
        if read_rfid():
            toggle_leds_and_servo(True)  # Acceso permitido
        else:
            toggle_leds_and_servo(False)  # Acceso denegado
        sleep(1)  # Previene lecturas múltiples rápidas
except KeyboardInterrupt:
    # Limpia los recursos en caso de interrupción
    GPIO.cleanup()
    publish_status(client, "Sistema detenido.")
