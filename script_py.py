import paho.mqtt.client as mqtt
import random
import time

# Lista de tópicos a los que se enviarán los mensajes
topics = ["topic/sensor1", "topic/sensor2", "topic/sensor3"]

# Función para generar valores aleatorios (puedes modificarla según tus necesidades)
def generate_random_value():
    return random.uniform(0, 100)  # Por ejemplo, un valor entre 0 y 100

# Función que se llama cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código de resultado {rc}")

# Función principal
def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    # Configura el broker MQTT (cambia esto según tus necesidades)
    broker_address = "test.mosquitto.org"  # Por ejemplo, el broker público de Mosquitto
    client.connect(broker_address, 1883, 60)

    # Inicia el loop en un hilo aparte
    client.loop_start()

    try:
        while True:
            for topic in topics:
                value = generate_random_value()
                client.publish(topic, value)
                print(f"Publicado {value} en {topic}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Detenido por el usuario")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
