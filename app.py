import os
from tkinter import *
import yt_dlp
from tqdm import tqdm

# Obtem o caminho da área de trabalho de forma mais garantida
if os.name == 'nt':  # Para Windows
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
else:  # Para macOS/Linux
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            progress = int(downloaded_bytes * 100 / total_bytes)
            texto_resultado['text'] = f"Baixando: {progress}%"
        janela.update_idletasks()  # Atualiza a interface

def downloadvideo():
    videourl = url_video.get()  # Pega a URL do vídeo
    if videourl:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),  # Direciona o download para a área de trabalho
            'merge_output_format': 'mp4',
            'progress_hooks': [progress_hook],  # mostra a barra de progresso
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'postprocessor_args': [
                '-c:a', 'aac',
                '-b:a', '192k',
            ],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([videourl])
            texto_resultado['text'] = 'Download de vídeo concluído!'
        except Exception as e:
            texto_resultado['text'] = f"Erro: {e}"

def downloadaudio():
    musicaurl = url_musica.get()  # Pega a URL da música
    if musicaurl:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),  # Direciona o download para a área de trabalho
            'progress_hooks': [progress_hook],  # mostra a barra de progresso
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([musicaurl])
            texto_resultado['text'] = 'Download de áudio concluído!'
        except Exception as e:
            texto_resultado['text'] = f"Erro: {e}"

janela = Tk()
janela.title('Downloader Video e Música')
janela.geometry('600x350')
janela.config(bg='#6a89ba')

texto_orientacao = Label(janela, text="Digite a URL para download do vídeo:", bg='#6a89ba', font=('Times New Roman', 16)) 
texto_orientacao.grid(column=2, row=1)

url_video = Entry(janela, width=50)
url_video.grid(column=2, row=2, padx=10, pady=10)

download_video = Button(janela, text='Download Vídeo', bg='#D3D3D3', command=downloadvideo)
download_video.grid(column=2, row=3, padx=250, pady=10)

texto_orientacao2 = Label(janela, text="Digite a URL para download da música:", bg='#6a89ba', font=('Times New Roman', 16))
texto_orientacao2.grid(column=2, row=8, pady=20)

url_musica = Entry(janela, width=50)
url_musica.grid(column=2, row=9)

download_musica = Button(janela, text='Download Música', bg='#D3D3D3', command=downloadaudio)
download_musica.grid(column=2, row=10, pady=12)

# Exibe o resultado
texto_resultado = Label(janela, text='', bg='#6a89ba')
texto_resultado.grid(column=2, row=12, pady=13)

janela.mainloop()
