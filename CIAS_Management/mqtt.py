import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Servo
from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

# Configuración de los pines
green_led = LED(14)  # LED verde
red_led = LED(15)    # LED rojo
button = Button(10)  # Botón para enviar mensaje manual
servo = Servo(18)    # Servo motor
RST_PIN = 22         # Pin de reset para RFID
SS_PIN = 8           # Pin de chip select para RFID

# Variables de estado
is_green_on = False
authorized_uid = [0x43, 0x39, 0x8F, 0xE2]  # UID autorizado
rfid_reader = SimpleMFRC522()  # Usa SimpleMFRC522 en lugar de MFRC522

# Configuración inicial
red_led.on()
green_led.off()
servo.mid()  # Posición inicial del servomotor

# Configuración de MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe("identificacion")

def publish_status(client, message):
    client.publish("identificacion", message)

def check_uid(uid):
    """
    Verifica si el UID leído coincide con el autorizado
    """
    return uid == authorized_uid

def toggle_leds_and_servo():
    global is_green_on

    if is_green_on:
        # Acceso denegado: LED verde apagado, LED rojo encendido y servo en 0 grados
        green_led.off()
        red_led.on()
        servo.min()  # Servo en 0 grados
        publish_status(client, "Acceso denegado. El LED verde se apagó. Ahora se encendió el rojo.")
    else:
        # Acceso permitido: LED rojo apagado, LED verde encendido y servo en 90 grados
        red_led.off()
        green_led.on()
        servo.max()  # Servo en 90 grados
        publish_status(client, "Acceso permitido. El LED rojo se apagó. Ahora se encendió el verde.")
    
    is_green_on = not is_green_on

def read_rfid():
    """
    Lee el RFID y verifica si es autorizado
    """
    (status, tag_type) = rfid_reader.Request()
    if status != rfid_reader.MI_OK:
        return None

    (status, uid) = rfid_reader.Anticoll()
    if status != rfid_reader.MI_OK:
        return None

    # Verifica si el UID es autorizado
    if check_uid(uid):
        return True
    else:
        return False

# Configuración del cliente MQTT
client.on_connect = on_connect
client.connect("test.mosquitto.org", 1883, 60)

# Inicia el loop MQTT en segundo plano
client.loop_start()

# Vincula el botón a la función de cambio de estado
button.when_pressed = toggle_leds_and_servo

# Mantiene el programa en ejecución
try:
    while True:
        # Revisión del RFID
        if read_rfid():
            toggle_leds_and_servo()  # Acceso permitido, cambio de estado de LEDs y servo
            publish_status(client, "Acceso concedido. El servo se movió a 90 grados.")
            sleep(3)  # Tiempo de espera antes de volver a la posición inicial
            servo.min()  # Regresa el servo a 0 grados
            green_led.off()
            red_led.on()
            publish_status(client, "Acceso cerrado. El servo volvió a 0 grados.")
        sleep(0.1)  # Pausa pequeña para evitar sobrecarga en el bucle principal
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    red_led.off()
    green_led.off()
    servo.detach()
    GPIO.cleanup()
