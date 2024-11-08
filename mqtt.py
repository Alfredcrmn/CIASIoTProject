import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Servo
from time import sleep

# Configuración de LEDs, botón y servomotor
red_led = LED(15)
green_led = LED(14)
button = Button(10)
servo = Servo(18)

# Variables de estado
is_green_on = False

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

# Función para manejar el cambio de estado al presionar el botón
def toggle_leds_and_servo():
    global is_green_on
    
    if is_green_on:
        # Cambiar a rojo encendido y verde apagado
        green_led.off()
        red_led.on()
        servo.min()  # Servo en 0 grados
        publish_status(client, "Acceso negado. El LED verde se apagó. Ahora se encendió el rojo.")
    else:
        # Cambiar a verde encendido y rojo apagado
        red_led.off()
        green_led.on()
        servo.max()  # Servo en 90 grados
        publish_status(client, "Acceso permitido. El LED rojo se apagó. Ahora se encendió el verde.")
    
    is_green_on = not is_green_on

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
        sleep(0.1)  # Pausa pequeña para evitar sobrecarga en el bucle principal
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
    red_led.off()
    green_led.off()
    servo.detach()