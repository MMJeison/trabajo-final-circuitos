from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.widget import Widget
from kivy.clock import Clock

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
        spacer = Widget(size_hint_y=None, height=20)
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
        # self.labels = []
        for v in self.sensors.values():
            table_layout.add_widget(Label(text=v['name']))
            valor_label = Label(text=str(v['value']))  # Nivel inicial
            estado_label = Label(text='Uknown')  # Estado inicial
            table_layout.add_widget(valor_label)
            table_layout.add_widget(estado_label)
            v['labels'] = [valor_label, estado_label]
        
        # Botón de volver
        btn_volver = Button(
            text="Volver", 
            size_hint=(None, None), 
            size=(100, 50),
            background_color ='#76D7C4',
            background_normal = '',
            color = '#000000',
            )
        
        # Añadir widgets al layout principal
        main_layout.add_widget(titulo)
        main_layout.add_widget(table_layout)
        main_layout.add_widget(btn_volver)
        
        self.add_widget(main_layout)
        
        btn_volver.bind(on_press=self.cambiar_a_inicio)
        
        # Simulación de actualización de datos cada 2 segundos
        Clock.schedule_interval(self.actualizar_datos, 2)

    def actualizar_datos(self, dt):
        # Esta función simula la actualización de los datos
        # import random
        for v in self.sensors.values():
            labels = v['labels']
            labels[0].text = str(v['value'])
            labels[0].text = "Alerta" if v['value'] > 0.5 else "Normal"

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'
        

class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super(VideoScreen, self).__init__(**kwargs)
        
        # Layout principal con márgenes
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        titulo = Label(text="Cámara en vivo", font_size='20sp', size_hint=(1, 0.1))
        
        # Layout para el video
        video_layout = BoxLayout(size_hint=(1, 0.8))
        video = VideoPlayer(source='path_to_your_video.mp4', size_hint=(1, 1))
        video_layout.add_widget(video)
        
        # Botón de volver
        btn_volver = Button(
            text="Volver", 
            size_hint=(None, None), 
            size=(100, 50),
            background_color ='#76D7C4',
            background_normal = '',
            color = '#000000',
            )
        
        # Añadir widgets al layout principal
        main_layout.add_widget(titulo)
        main_layout.add_widget(video_layout)
        main_layout.add_widget(btn_volver)
        
        self.add_widget(main_layout)
        
        btn_volver.bind(on_press=self.cambiar_a_inicio)

    def cambiar_a_inicio(self, *args):
        self.manager.current = 'inicio'
        
        
class SecurityLab(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(TablaScreen(name='tabla'))
        sm.add_widget(VideoScreen(name='video'))
        return sm

if __name__ == '__main__':
    SecurityLab().run()
