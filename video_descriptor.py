import cv2
import base64
import json
import os
import threading
import logging
import wx
import pyperclip
from openai import OpenAI, OpenAIError
from tkinter.filedialog import askopenfilename

# Configuración del logger para trazar errores y eventos
logging.basicConfig(
    filename='video_descriptor.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class VideoDescriptorApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(VideoDescriptorApp, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(self.panel, label="Seleccione un video para describir:")
        self.vbox.Add(self.label, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.progress = wx.Gauge(self.panel, range=100, size=(250, 25))
        self.vbox.Add(self.progress, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.btn_select = wx.Button(self.panel, label='Seleccionar Video')
        self.btn_select.Bind(wx.EVT_BUTTON, self.on_select_video)
        self.vbox.Add(self.btn_select, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.panel.SetSizer(self.vbox)
        self.Centre()

    def on_select_video(self, event):
        video_name = askopenfilename(title="Selecciona el video que deseas describir", filetypes=[("Video Files", "*.mp4;*.mov;*.avi")])
        if video_name:
            self.thread = threading.Thread(target=self.process_video, args=(video_name,))
            self.thread.start()
        else:
            wx.MessageBox('No se seleccionó ningún video.', 'Advertencia', wx.OK | wx.ICON_WARNING)

    def process_video(self, video_name):
        api_key, prompt = self.load_api_key()
        if api_key and prompt:
            description = self.get_description(video_name, api_key, prompt)
            if description:
                wx.CallAfter(self.show_result_window, description)
            else:
                wx.CallAfter(self.show_error_message, "No se pudo generar la descripción del video. Verifica los registros para más detalles.")
        else:
            wx.CallAfter(self.show_error_message, "No se pudo cargar la clave API.")

    def load_api_key(self, file_path='data.json'):
        try:
            with open(file_path, 'r') as data_file:
                app_data = json.load(data_file)
                return app_data['key'], app_data['prompt']
        except Exception as e:
            logging.error(f"Error al cargar el archivo de configuración: {e}")
            return None, None

    def get_description(self, video_name, api_key, prompt):
        duration = self.get_video_length(video_name)

        if not os.path.exists(video_name) or duration > 30:
            logging.warning("El video no existe o tiene más de 30 segundos de duración.")
            return None

        try:
            video = cv2.VideoCapture(video_name)
            base64Frames = []

            while video.isOpened():
                success, frame = video.read()
                if not success:
                    break
                _, buffer = cv2.imencode(".jpg", frame)
                base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

                # Actualizar barra de progreso
                wx.CallAfter(self.progress.SetValue, int(video.get(cv2.CAP_PROP_POS_FRAMES) / video.get(cv2.CAP_PROP_FRAME_COUNT) * 100))

            video.release()

            prompt_messages = [
                {
                    "role": "user",
                    "content": [
                        prompt,
                        *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
                    ],
                },
            ]

            params = {
                "model": "gpt-4o",
                "messages": prompt_messages,
                "max_tokens": 600
            }

            client = OpenAI(api_key=api_key)
            result = client.chat.completions.create(**params)
            description = result.choices[0].message.content
            return description

        except OpenAIError as e:
            logging.error(f"Error en la llamada a la API de OpenAI: {e}")
            return f"Error en la llamada a la API: {str(e)}"

        except Exception as e:
            logging.error(f"Error en la generación de la descripción: {e}")
            return f"Error inesperado: {str(e)}"

    def get_video_length(self, video_path):
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            logging.warning(f"El video no se pudo abrir: {video_path}")
            return 0

        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        video.release()

        if fps > 0:
            return total_frames / fps
        else:
            return 0

    def show_result_window(self, description):
        result_window = wx.Frame(self, title="Descripción Generada", size=(600, 400))
        panel = wx.Panel(result_window)

        vbox = wx.BoxSizer(wx.VERTICAL)
        text_box = wx.TextCtrl(panel, value=description, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        vbox.Add(text_box, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_copy = wx.Button(panel, label='Copiar al Portapapeles')
        btn_copy.Bind(wx.EVT_BUTTON, lambda event: pyperclip.copy(description))
        hbox.Add(btn_copy, flag=wx.RIGHT, border=10)

        btn_close = wx.Button(panel, label='Copiar y Salir')
        btn_close.Bind(wx.EVT_BUTTON, lambda event: self.exit_application(description, result_window))
        hbox.Add(btn_close, flag=wx.LEFT, border=10)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        result_window.Show()

    def show_error_message(self, message):
        wx.MessageBox(message, 'Error', wx.OK | wx.ICON_ERROR)

    def exit_application(self, description, window):
        pyperclip.copy(description)
        window.Close()
        self.Close()


if __name__ == '__main__':
    app = wx.App(False)
    frame = VideoDescriptorApp(None, title="Generador de Descripción de Video")
    frame.Show()
    app.MainLoop()
