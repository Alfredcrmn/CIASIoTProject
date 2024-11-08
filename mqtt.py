import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Servo
from time import sleep

# Crea objetos para los LEDs, el botón y el servomotor
led_verde = LED(14)  # LED verde conectado a GPIO 14
led_rojo = LED(15)   # LED rojo conectado a GPIO 15
boton = Button(3)    # Botón conectado a GPIO 3
servo = Servo(18)    # Servomotor conectado a GPIO 18

# Función de conexión MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código de resultado " + str(rc))
    client.subscribe("identificacion")  # Suscripción a un tema

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload_str = msg.payload.decode('utf-8')
    
    if "green_on" in payload_str:
        led_verde.on()  # Enciende el LED verde
    elif "green_off" in payload_str:
        led_verde.off()  # Apaga el LED verde
    elif "red_on" in payload_str:
        led_rojo.on()  # Enciende el LED rojo
    elif "red_off" in payload_str:
        led_rojo.off()  # Apaga el LED rojo
    elif "servo_move" in payload_str:  # Mueve el servomotor
        servo.min()  # Mueve el servo a la posición mínima (aproximadamente 0 grados)
        sleep(1)
        servo.max()  # Mueve el servo a la posición máxima (aproximadamente 180 grados)

# Función para controlar el botón y publicar estado
def button_press_control(client):
    while True:
        if boton.is_pressed:  # Si el botón está presionado
            print("Botón presionado, encendiendo LED verde.")
            led_verde.on()  # Enciende el LED verde
            publish_status(client, "green_on")  # Publica el estado en MQTT
            sleep(1)
        else:
            led_verde.off()  # Apaga el LED verde
            publish_status(client, "green_off")  # Publica el estado en MQTT
        sleep(0.1)

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
