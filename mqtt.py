import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Servo
from time import sleep

# Definir los pines y configurar los componentes
led_verde = LED(14)  # LED verde conectado a GPIO 14
led_rojo = LED(15)   # LED rojo conectado a GPIO 15
boton = Button(3)    # Botón conectado a GPIO 3
servo = Servo(18)    # Servomotor conectado a GPIO 18

# Estado inicial: LED rojo encendido
led_rojo.on()
led_verde.off()
servo.min()  # Mueve el servo a la posición 0 grados

# Función de conexión MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código de resultado " + str(rc))
    client.subscribe("identificacion")  # Suscripción a un tema

# Función que maneja los mensajes recibidos de MQTT
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload_str = msg.payload.decode('utf-8')
    
    # Acciones basadas en los comandos recibidos
    if "green_on" in payload_str:
        led_verde.on()  # Enciende el LED verde
        led_rojo.off()  # Apaga el LED rojo
        servo.mid()     # Mueve el servo a 90 grados
    elif "green_off" in payload_str:
        led_verde.off()  # Apaga el LED verde
    elif "red_on" in payload_str:
        led_rojo.on()   # Enciende el LED rojo
        led_verde.off()  # Apaga el LED verde
        servo.min()      # Mueve el servo a 0 grados
    elif "servo_move" in payload_str:
        servo.mid()     # Mueve el servo a 90 grados
        sleep(1)
        servo.min()     # Mueve el servo a 0 grados

# Función para controlar el botón y las acciones correspondientes
def button_press_control(client):
    while True:
        if boton.is_pressed:  # Si el botón está presionado (LOW)
            print("Botón presionado, apagando LED rojo y encendiendo LED verde.")
            led_rojo.off()  # Apaga el LED rojo
            led_verde.on()  # Enciende el LED verde
            servo.mid()     # Mueve el servo a 90 grados
            publish_status(client, "green_on")  # Publica el estado en MQTT
            sleep(0.5)      # Espera un poco para mantener el estado
        else:
            led_verde.off()  # Apaga el LED verde
            led_rojo.on()    # Enciende el LED rojo
            servo.min()      # Mueve el servo a 0 grados
            publish_status(client, "red_on")  # Publica el estado en MQTT
        sleep(0.1)  # Pausa pequeña para evitar lecturas rápidas

# Función de publicación MQTT
def publish_status(client, message):
    client.publish("identificacion", message)

# Llamada de conexión MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Inicia el bucle MQTT en segundo plano
client.loop_start()

# Inicia el control del botón
button_press_control(client)
