import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

# Define GPIO y configura sus modos
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Configura pines de salida para LEDs
GPIO.setup(15, GPIO.OUT)  # GPIO 15 conectado al LED rojo
GPIO.setup(14, GPIO.OUT)  # GPIO 14 conectado al LED verde

# Configura el pin 3 (botón) como entrada con resistencia pull-up interna
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up para que el botón lea HIGH cuando no se presiona

# Configura el PWM en GPIO 18 para controlar el servomotor
GPIO.setup(18, GPIO.OUT)  # GPIO 18 para el servomotor

# Configura el PWM para el servomotor
pwm = GPIO.PWM(18, 50)  # Frecuencia de 50Hz, que es la típica para servos
pwm.start(0)  # Inicializa el PWM con 0% de ciclo de trabajo

# Función de conexión MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código de resultado " + str(rc))
    client.subscribe("identificacion")  # Suscripción a un tema

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload_str = msg.payload.decode('utf-8')
    
    if "green_on" in payload_str:
        GPIO.output(14, True)  # Enciende el LED verde
    elif "green_off" in payload_str:
        GPIO.output(14, False)  # Apaga el LED verde
    elif "red_on" in payload_str:
        GPIO.output(15, True)  # Enciende el LED rojo
    elif "red_off" in payload_str:
        GPIO.output(15, False)  # Apaga el LED rojo
    elif "servo_move" in payload_str:  # Mueve el servomotor
        pwm.ChangeDutyCycle(7)  # Ajusta el ciclo de trabajo para mover el servo (90 grados aproximadamente)
        time.sleep(1)
        pwm.ChangeDutyCycle(0)  # Detiene el servo

# Función para controlar el botón y publicar estado
def button_press_control(client):
    while True:
        input_state = GPIO.input(3)  # Detecta si el botón está presionado (en GPIO 3)
        if input_state == False:  # El botón está presionado
            print("Botón presionado, encendiendo LED verde.")
            GPIO.output(14, True)  # Enciende el LED verde
            publish_status(client, "green_on")  # Publica el estado en MQTT
            time.sleep(1)
        else:
            GPIO.output(14, False)  # Apaga el LED verde
            publish_status(client, "green_off")  # Publica el estado en MQTT
        time.sleep(0.1)

# Función de publicación MQTT
def publish_status(client, message):
    client.publish("identificacion", message)

# Llamadas de la función MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Inicia el bucle MQTT en segundo plano
client.loop_start()
button_press_control(client)  # Control de botón y publicación
