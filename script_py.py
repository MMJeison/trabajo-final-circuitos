import random
import time
import paho.mqtt.client as mqttc
from paho.mqtt import publish

BROKER_URL = "192.168.192.5"
BROKER_PORT = 1883

class Publisher:

    @staticmethod
    def send_message(message, topic):
        try:
            print(topic, message, BROKER_URL)
            publish.single(topic, message,
                           hostname= BROKER_URL, port = BROKER_PORT)
        except Exception as ex:
            print("Error enviando un mensaje ex: {}".format(ex))

# class Listener:

#     def __init__(self, observador):
#         self.client = mqttc.Client(mqttc.CallbackAPIVersion.VERSION1)
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#         self.observador = observador
#         try:
#             self.client.connect(BROKER_URL, BROKER_PORT, 60)
#         except:
#             print("sin conexión al broker")

#     def start(self):
#         print('looping')
#         self.client.loop_forever()

#     def on_connect(self, client, userdata, flags, rc):
#         print("Conectado ", str(rc), 'INBOUND_TOPIC')
#         client.subscribe('INBOUND_TOPIC')


#     def on_message(self, client, userdata, msg):
#         print("Mensaje recibido: {}".format(msg))
#         self.observador.procesarMensajeLuz(msg.payload.decode("utf-8"))

# Lista de tópicos a los que se enviarán los mensajes
topics = ["lab/sensors/humo", "lab/sensors/seism"]

# Función para generar valores aleatorios (puedes modificarla según tus necesidades)
def generate_random_value():
    return random.uniform(0, 100)  # Por ejemplo, un valor entre 0 y 100


# Función principal
def main():
    
    publisher = Publisher()
    
    try:
        while True:
            for topic in topics:
                value = generate_random_value()
                publisher.send_message(value, topic)
                print(f"Publicado {value} en {topic}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Detenido por el usuario")

if __name__ == "__main__":
    main()
