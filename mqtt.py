# Importando Dependencias
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Define GPIO y configura sus modos
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)  # GPIO 12 conectado al LED rojo
GPIO.setup(11, GPIO.OUT)  # GPIO 11 conectado al LED verde
GPIO.setup(9, GPIO.OUT)   # GPIO 9 conectado al servomotor
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO 7 conectado al botón 1

# Configura la conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código de resultado " + str(rc))
    client.subscribe("identificacion")  # Suscripción a un tema

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if "green_on" in msg.payload:
        GPIO.output(11, True)
    elif "green_off" in msg.payload:
        GPIO.output(11, False)

# Configura la publicación de mensajes en MQTT
def publish_status(client, message):
    # Publica el mensaje en el tema 'estado'
    client.publish("estado", message)

# Función principal para controlar la lógica de los botones
def button_press_control(client):
    while True:
        # Detecta si el botón ha sido presionado
        input_state = GPIO.input(7)
        if input_state == False:  # El botón está presionado
            print("Botón presionado, encendiendo LED verde.")
            GPIO.output(11, True)  # Enciende el LED verde
            publish_status(client, "green_on")  # Publica el estado en MQTT
            time.sleep(1)  # Espera 1 segundo
        else:
            GPIO.output(11, False)  # Apaga el LED verde
            publish_status(client, "green_off")  # Publica el estado en MQTT
        time.sleep(0.1)  # Revisa el estado del botón cada 100ms

# Llamadas de la función MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Llamar a la función que controla el botón y publica el estado
client.loop_start()  # Inicia el bucle MQTT en segundo plano
button_press_control(client)  # Ejecuta el control del botón