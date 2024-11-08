import paho.mqtt.client as mqtt
from gpiozero import LED, Button, Servo
from time import sleep

# Configuración de pines
red_led = LED(15)      # LED rojo en GPIO 15
green_led = LED(14)    # LED verde en GPIO 14
button = Button(10)    # Botón en GPIO 10
servo = Servo(18)      # Servomotor en GPIO 18

# Estado inicial
red_led.on()            # Enciende el LED rojo al inicio
green_led.off()         # Asegura que el LED verde esté apagado
servo.mid()             # Coloca el servomotor en posición media (0 grados)

# Estado del sistema
is_green_on = False     # Controla el estado del switch

# Función de conexión MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado con el código de resultado " + str(rc))
    client.subscribe("identificacion")  # Suscripción a un tema

# Función de mensaje MQTT
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload.decode()))

# Configuración de MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)
client.loop_start()

# Función para alternar LEDs y controlar el servo
def toggle_leds_and_servo():
    global is_green_on
    if is_green_on:
        red_led.on()               # Enciende el LED rojo
        green_led.off()            # Apaga el LED verde
        servo.mid()                # Devuelve el servo a 0 grados
        client.publish("identificacion", "red_on")
    else:
        red_led.off()              # Apaga el LED rojo
        green_led.on()             # Enciende el LED verde
        servo.max()                # Mueve el servo a 90 grados
        client.publish("identificacion", "green_on")
    is_green_on = not is_green_on  # Cambia el estado del switch

# Configura el botón para activar la función de toggle al hacer clic
button.when_pressed = toggle_leds_and_servo

# Mantén el programa en ejecución
try:
    while True:
        sleep(0.1)  # Pausa breve para evitar uso excesivo de CPU
except KeyboardInterrupt:
    client.loop_stop()  # Detiene el loop de MQTT al salir
    print("Programa terminado")
