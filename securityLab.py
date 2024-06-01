from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from datetime import datetime, timedelta
import cv2
from VideoStreamN import VideoStreamN
from kivy.graphics.texture  import Texture
from kivy.uix.image import Image

import paho.mqtt.client as mqttc
from paho.mqtt import publish
from _thread import start_new_thread

BROKER_URL = "192.168.192.4"
BROKER_PORT = 1883

class MyData:
    activatedAlarms = 0
    
    @staticmethod
    def getBtnAlarmsText():
        if MyData.activatedAlarms == 1:
            return "Apagar alarmas"
        return "Encender alarmas"
        

class Publisher:
    @staticmethod
    def send_message(message, topic):
        try:
            print(topic, message, BROKER_URL)
            publish.single(topic, message,
                           hostname=BROKER_URL, port = BROKER_PORT)
        except Exception as ex:
            print("Error enviando un mensaje ex: {}".format(ex))
            
class Listener:

    def __init__(self, observador, sensors):
        self.client = mqttc.Client(mqttc.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.observador = observador
        self.sensors = sensors
        try:
            self.client.connect(BROKER_URL, BROKER_PORT, 60)
        except:
            print("sin conexión al broker")

    def start(self):
        print('looping')
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        for v in self.sensors.values():
            topic = v['topic']
            print("Conectado ", str(rc), topic)
            client.subscribe(topic)
        client.subscribe("lab/alarms")


    def on_message(self, client, userdata, msg):
        print("Mensaje recibido")
        print("Message: {}".format(msg.payload.decode("utf-8")))
        print(f'Topic: {msg.topic}')
        self.observador.procesarDato(msg.topic, msg.payload.decode("utf-8"))



publisher = Publisher()

class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super(InicioScreen, self).__init__(**kwargs)
        window = GridLayout()
        window.cols = 1
        window.size_hint = (0.6, 0.7)
        window.pos_hint = {"center_x": 0.5, "center_y":0.5}
        btn_tabla = Button(
            text="Sensores",
            size_hint= (1, 0.5),
            bold= True,
            background_color ='#76D7C4',
            background_normal = '',
            color = '#000000',
            font_size = '24sp',
            )
        spacer = Widget(size_hint_y=None, height=10)
        btn_video = Button(
            text="Cámara",
            size_hint= (1, 0.5),
            bold= True,
            background_color ='#76D7C4',
            background_normal = '',
            color = '#000000',
            font_size = '24sp',
            )
        window.add_widget(btn_tabla)
        window.add_widget(spacer)
        window.add_widget(btn_video)
        self.add_widget(window)

        btn_tabla.bind(on_press=self.cambiar_a_tabla)
        btn_video.bind(on_press=self.cambiar_a_video)

    def cambiar_a_tabla(self, *args):
        self.manager.current = 'tabla'

    def cambiar_a_video(self, *args):
        self.manager.current = 'video'
        

class TablaScreen(Screen):
    def __init__(self, **kwargs):
        super(TablaScreen, self).__init__(**kwargs)
        # self.sensors = ["Humo", "Sísmico"]
        dt_now = datetime.now()
        delta = timedelta(seconds=15)
        self.sensors = {
            "smoke": {
                "name": "Humo",
                "topic": "lab/sensors/smoke",
                "last_time": dt_now-delta,
                "value": -1,
                "state": 2,
                "up_limit": 1,
                # "down_limit": 20,
                "labels": []
            },
            "seism": {
                "name": "Sísmico",
                "topic": "lab/sensors/seism",
                "last_time": dt_now-delta,
                "value": -1,
                "state": 2,
                "up_limit": 1,
                # "down_limit": 20,
                "labels": []
            }
        }
        # Layout principal con márgenes
        
        try:
            self.listener = Listener(self, self.sensors)
            start_new_thread(self.listener.start, ())
        except:
            print("Error al iniciar el listener")
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Título
        titulo = Label(text="Niveles de Sensores", font_size='20sp', size_hint=(1, 0.1))
        
        # Layout para la tabla
        table_layout = GridLayout(cols=3, size_hint=(1, 0.7))
        
        # Encabezados
        headers = ["Sensores", "Nivel", "Estado"]
        for header in headers:
            table_layout.add_widget(Label(text=header, bold=True))
        
        # Filas de datos
        # self.labels = []
        for v in self.sensors.values():
            table_layout.add_widget(Label(text=v['name']))
            valor_label = Label(text=self.getValue(v))  # Nivel inicial
            estado_label = Label(text=self.getTextState(v['state']))  # Estado inicial
            table_layout.add_widget(valor_label)
            table_layout.add_widget(estado_label)
            v['labels'] = [valor_label, estado_label]
        
        # Añadir widgets al layout principal
        main_layout.add_widget(titulo)
        main_layout.add_widget(table_layout)
        # Layout flotante para botones
        float_layout = FloatLayout()

        # Botón de volver
        btn_volver = Button(
            text="Volver",
            size_hint=(None, None),
            size=(100, 50),
            background_color='#76D7C4',
            background_normal='',
            color='#000000',
            pos_hint={"x": 0.02, "y": 0.02},
        )

        # Botón de activar alarmas
        self.btn_alarmas = Button(
            text=MyData.getBtnAlarmsText(),
            size_hint=(None, None),
            size=(140, 55),
            background_color='#E74C3C',
            background_normal='',
            color='#FFFFFF',
            pos_hint={"x": 0.75, "y": 0.02}
        )

        float_layout.add_widget(btn_volver)
        float_layout.add_widget(self.btn_alarmas)

        # Añadir layouts al screen
        self.add_widget(main_layout)
        self.add_widget(float_layout)

        btn_volver.bind(on_press=self.cambiar_a_inicio)
        self.btn_alarmas.bind(on_press=self.handleAlarms)

        # Simulación de actualización de datos cada 2 segundos
        Clock.schedule_interval(self.actualizar_datos, 1)
        
    def procesarDato(self, topic, message):
        if topic == "lab/alarms":
            MyData.activatedAlarms = float(message)
            return
        flag = False
        for v in self.sensors.values():
            if v['topic'] == topic:
                try:
                    v['value'] = float(message)
                    v['last_time'] = datetime.now()
                    flag = True
                except:
                    print("Error al procesar el mensaje")
                finally:
                    break
        if flag:
            print("Procesado")
        else:
            print("Mensage No procesado")
            
    def getValue(self, sensor):
        if sensor['state'] == 2:
            return "Uknown"
        return str(sensor['value'])
            
    def getTextState(slef, state):
        if state == 0:
            return "Apagado"
        if state == 1:
            return "Normal"
        if state == 2:
            return "Uknown"
        return "Alarm!!!"
    
    def calculateState(self, sensor):
        now = datetime.now()
        diff = now - sensor['last_time']
        if diff.total_seconds() > 10:
            sensor['state'] = 2
            return
        sensor['state'] = 1
        if 'up_limit' in sensor:
            if sensor['value'] >= sensor['up_limit']:
                sensor['state'] = -1
                publisher.send_message('1', 'lab/alarms')
                MyData.activatedAlarms = 1
                return
        if 'down_limit' in sensor:
            if sensor['value'] <= sensor['down_limit']:
                sensor['state'] = -1
                publisher.send_message('1', 'lab/alarms')
                MyData.activatedAlarms = 1
                return
        

    def actualizar_datos(self, dt):
        # Esta función simula la actualización de los datos
        # import random
        for v in self.sensors.values():
            self.calculateState(v)
            labels = v['labels']
            labels[0].text = self.getValue(v)
            labels[1].text = self.getTextState(v['state'])
        
        self.btn_alarmas.text = MyData.getBtnAlarmsText()

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'

    def handleAlarms(self, *args):
        if MyData.activatedAlarms == 0:
            print("¡Activando alarmas!")
            publisher.send_message('1', 'lab/alarms')
            MyData.activatedAlarms = 1
            print("Eviado 1 a lab/alarm")
        else:
            print("!Apagando alarmas!")
            publisher.send_message('0', 'lab/alarms')
            MyData.activatedAlarms = 0
            print("Eviado 0 a lab/alarm")
        

class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super(VideoScreen, self).__init__(**kwargs)
        
        # Layout principal con márgenes
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        titulo = Label(text="Cámara en vivo", font_size='20sp', size_hint=(1, 0.1))
        
        # Layout para el video
        video_layout = BoxLayout(size_hint=(1, 0.8))
        self.video_image = Image()
        video_layout.add_widget(self.video_image)
        
        # Añadir widgets al layout principal
        main_layout.add_widget(titulo)
        main_layout.add_widget(video_layout)
        # Layout flotante para botones
        float_layout = FloatLayout()

        # Botón de volver
        btn_volver = Button(
            text="Volver",
            size_hint=(None, None),
            size=(100, 50),
            background_color='#76D7C4',
            background_normal='',
            color='#000000',
            pos_hint={"x": 0.02, "y": 0.02}
        )

        # Botón de activar alarmas
        self.btn_alarmas = Button(
            text=MyData.getBtnAlarmsText(),
            size_hint=(None, None),
            size=(140, 55),
            background_color='#E74C3C',
            background_normal='',
            color='#FFFFFF',
            pos_hint={"x": 0.75, "y": 0.02}
        )

        float_layout.add_widget(btn_volver)
        float_layout.add_widget(self.btn_alarmas)

        # Añadir layouts al screen
        self.add_widget(main_layout)
        self.add_widget(float_layout)

        btn_volver.bind(on_press=self.cambiar_a_inicio)
        self.btn_alarmas.bind(on_press=self.handleAlarms)
        
        Clock.schedule_interval(self.updateData, 2)
        
    def updateData(self, *args):
        self.btn_alarmas.text = MyData.getBtnAlarmsText()

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'

    def handleAlarms(self, *args):
        if MyData.activatedAlarms == 0:
            print("¡Activando alarmas!")
            publisher.send_message('1', 'lab/alarms')
            MyData.activatedAlarms = 1
            print("Eviado 1 a lab/alarm")
        else:
            print("!Apagando alarmas!")
            publisher.send_message('0', 'lab/alarms')
            MyData.activatedAlarms = 0
            print("Eviado 0 a lab/alarm")
        
    def on_enter(self, *args):
        self.video_stream = VideoStreamN(src=0).start()
        Clock.schedule_interval(self.update_video, 1.0 / 15.0)  # 30 FPS
 
    def update_video(self, dt):
        frame = self.video_stream.read()
        if frame is not None:
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.video_image.texture = image_texture
 
    def on_leave(self, *args):
        Clock.unschedule(self.update_video)
        self.video_stream.stop()
        
class SecurityLab(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(TablaScreen(name='tabla'))
        sm.add_widget(VideoScreen(name='video'))
        return sm
    
    def on_stop(self):
        # Asegúrate de que todas las transmisiones se detengan cuando la aplicación se cierra
        for screen in self.root.screens:
            if isinstance(screen, VideoScreen):
                screen.video_stream.stop()

if __name__ == '__main__':
    SecurityLab().run()
