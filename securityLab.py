import cv2
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from VideoStream import VideoStream

class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super(InicioScreen, self).__init__(**kwargs)
        window = GridLayout()
        window.cols = 1
        window.size_hint = (0.6, 0.7)
        window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        btn_tabla = Button(
            text="Sensores",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#76D7C4',
            background_normal='',
            color='#000000',
            font_size='24sp',
        )
        spacer = Widget(size_hint_y=None, height=20)
        btn_video = Button(
            text="Cámara",
            size_hint=(1, 0.5),
            bold=True,
            background_color='#76D7C4',
            background_normal='',
            color='#000000',
            font_size='24sp',
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

        self.sensors = {
            "humo": {
                "name": "Humo",
                "value": 0,
                "state": 0,
                "labels": []
            },
            "seism": {
                "name": "Sísmico",
                "value": 0,
                "state": 0,
                "labels": []
            }
        }

        # Layout principal con márgenes
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="Niveles de Sensores", font_size='20sp', size_hint=(1, 0.1))

        # Layout para la tabla
        table_layout = GridLayout(cols=3, size_hint=(1, 0.8))

        # Encabezados
        headers = ["Sensores", "Nivel", "Estado"]
        for header in headers:
            table_layout.add_widget(Label(text=header, bold=True))

        # Filas de datos
        for v in self.sensors.values():
            table_layout.add_widget(Label(text=v['name']))
            valor_label = Label(text=str(v['value']))  # Nivel inicial
            estado_label = Label(text='Unknown')  # Estado inicial
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
            pos_hint={"x": 0.02, "y": 0.02}
        )

        # Botón de activar alarmas
        btn_alarmas = Button(
            text="Activar Alarmas",
            size_hint=(None, None),
            size=(140, 55),
            background_color='#E74C3C',
            background_normal='',
            color='#FFFFFF',
            pos_hint={"x": 0.75, "y": 0.02}
        )

        float_layout.add_widget(btn_volver)
        float_layout.add_widget(btn_alarmas)

        # Añadir layouts al screen
        self.add_widget(main_layout)
        self.add_widget(float_layout)

        btn_volver.bind(on_press=self.cambiar_a_inicio)
        btn_alarmas.bind(on_press=self.activar_alarmas)

        # Simulación de actualización de datos cada 2 segundos
        Clock.schedule_interval(self.actualizar_datos, 2)

    def actualizar_datos(self, dt):
        # Esta función simula la actualización de los datos
        import random
        for v in self.sensors.values():
            labels = v['labels']
            labels[0].text = str(random.randint(0, 100))
            labels[1].text = "Alerta" if random.random() > 0.5 else "Normal"

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'

    def activar_alarmas(self, *args):
        print("¡Alarmas activadas!")


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
        btn_alarmas = Button(
            text="Activar Alarmas",
            size_hint=(None, None),
            size=(140, 55),
            background_color='#E74C3C',
            background_normal='',
            color='#FFFFFF',
            pos_hint={"x": 0.75, "y": 0.02}
        )

        float_layout.add_widget(btn_volver)
        float_layout.add_widget(btn_alarmas)

        # Añadir layouts al screen
        self.add_widget(main_layout)
        self.add_widget(float_layout)

        btn_volver.bind(on_press=self.cambiar_a_inicio)
        btn_alarmas.bind(on_press=self.activar_alarmas)

    def on_enter(self, *args):
        self.video_stream = VideoStream(src=0).start()
        Clock.schedule_interval(self.update_video, 1.0 / 30.0)  # 30 FPS

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

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'

    def activar_alarmas(self, *args):
        print("¡Alarmas activadas!")


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
