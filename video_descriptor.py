from IPython.display import display, Image, Audio
import cv2
import base64
import time
from openai import OpenAI, OpenAIError
import json
import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os

# Cargar clave API desde el archivo key.json
with open('data.json', 'r') as data_file:
    app_data = json.load(data_file)
    api_key=app_data['key']
    prompt=app_data['prompt']

client = OpenAI(api_key=api_key)

def get_description(video_name, prompt=prompt):
    duration=get_video_length(video_name)
    if os.path.exists(video_name) and duration<=30:
        video = cv2.VideoCapture(video_name)
        base64Frames = []
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break
            _, buffer = cv2.imencode(".jpg", frame)
            base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

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

        try:
            result = client.chat.completions.create(**params)
            description = result.choices[0].message.content
            return description
        except OpenAIError as e:
            return str(e)
    else:
        messagebox.showwarning("error", "el video no existe, o tiene más de 30 segundos de duración")
        return None
def get_video_length(video_path):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        return 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        duration = total_frames / fps
    else:
        duration = 0
    video.release()
    return duration
def main():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    video_name = askopenfilename(title="Busca el video que quieres describir")
    if video_name:
        result = get_description(video_name)
        if result:

            messagebox.showinfo("Éxito", f"La descripción brindada por la IA: {result}")
        else:
            messagebox.showwarning("error", f"un error en tiempo de ejecución ocurrió. Se pasará a mostrar el error. envíale este mensage al desarrollador: {e}")
    else:

        messagebox.showwarning("Advertencia", "No se seleccionó ningún video.")

if __name__ == '__main__':
    main()
