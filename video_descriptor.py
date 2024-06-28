from IPython.display import display, Image, Audio
import cv2
import base64
import time
from openai import OpenAI
import json
import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os

# Cargar clave API desde el archivo key.json
with open('key.json', 'r') as key_file:
    key_data = json.load(key_file)
    api_key = key_data['key']

client = OpenAI(api_key=api_key)

def get_description(video_name, prompt="Estos son los frames de un video cuyo contenido quiero saber. Tu misión es brindarme una descripción concisa, completamente descriptiva dado a que soy una persona con discapacidad visual por lo cual no puedo ver la pantalla, y en resumen, explicarme lo que sale en el video usando los frames brindados. Recuerda también que no tienes más de 600 palabras, así que intenta ser lo más conciso. no separes los frames, analiza todo el video e intenta describirlo en un aspecto completo, pero sin omitir detalles."):
    if os.path.exists(video_name):
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

        except Exception as e:
            return str(e)

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
