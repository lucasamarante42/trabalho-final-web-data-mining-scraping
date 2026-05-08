# -*- coding: utf-8 -*-
"""
Trabalho Final Web Data Mining And Scraping

MBA Engenharia de Dados
Disciplina: Web Data Mining and Scraping

Integrantes:
- Lucas Amarante
"""

!pip install python-telegram-bot
!pip install youtube-transcript-api
!pip install google-genai
!pip install gtts
!pip install feedparser
!pip install requests
!pip install lxml
!pip install beautifulsoup4
!pip install yt-dlp
!pip install edge-tts

import requests
import re
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from gtts import gTTS

GEMINI_API_KEY = ""

YOUTUBE_CHANNEL = "https://www.youtube.com/@HernandesDiasLopesOficial"

TELEGRAM_BOT_API_KEY = ""

# Recupera a URL do bot do Telegram
import requests
import re
from bs4 import BeautifulSoup

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/getUpdates"

dados = requests.get(url).json()

if dados:
  mensagens = dados['result']

  ultima_url = None

  for item in reversed(mensagens):

      try:
          texto = item['message']['text']

          if "youtube.com" in texto:
              ultima_url = texto
              break

      except:
          pass

  if ultima_url:
    # Captura diretamente os shorts (id)
    YOUTUBE_CHANNEL = ultima_url

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    shorts_url = YOUTUBE_CHANNEL + "/shorts"

    # Requisição html
    response = requests.get(
        shorts_url,
        headers=headers
    )

    html = response.text

    # Extrai os vídeos ID
    video_ids = re.findall(
        r'"videoId":"(.*?)"',
        html
    )

    # Remove duplicados
    video_ids = list(dict.fromkeys(video_ids))

    # Captura apenas 5
    video_ids = video_ids[:5]

shorts = []

for video_id in video_ids:
  shorts.append({
      "video_id": video_id,
      "url": f"https://youtube.com/shorts/{video_id}"
  })

print(shorts)

# Transcrição dos vídeos
from youtube_transcript_api import YouTubeTranscriptApi

transcricoes = []

ytt_api = YouTubeTranscriptApi()

for short in shorts:

  try:
    video_id = short["video_id"]

    # NOVA API
    fetched_transcript = ytt_api.fetch(
        video_id,
        languages=['pt']
    )

    # converter para lista raw
    transcript = fetched_transcript.to_raw_data()

    texto = " ".join(
        [item['text'] for item in transcript]
    )

    transcricoes.append({
        "video_id": video_id,
        "texto": texto
    })

    print(f"TRANSCRIÇÃO OK: {video_id}")

  except Exception as e:
    print(f"ERRO: {video_id}")
    print(e)

print(transcricoes)

# Resumo das transcrições usando o Gemini
from google import genai

client = genai.Client(
    api_key=GEMINI_API_KEY
)

resumos = []

for i, item in enumerate(transcricoes):

    prompt = f"""
    Resuma a transcrição abaixo em português.

    Seja:
    - objetivo
    - claro
    - resumido

    TRANSCRIÇÃO:

    {item['texto']}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    resumo = response.text

    texto_resumo = f"""
    VIDEO {i+1}

    RESUMO:
    {resumo}
    """

    resumos.append(texto_resumo)

    print(f"RESUMO OK: VIDEO {i+1}")

texto_geral = "\n\n".join(resumos)

print(texto_geral)

# Transforma os resumos num único texto
prompt_final = f"""
Transforme os resumos abaixo em um único texto fluido,
como uma narração para podcast.

RESUMOS:

{texto_geral}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt_final
)

roteiro_audio = response.text

print(roteiro_audio)

import re

roteiro_limpo = roteiro_audio

# Remove markdown
roteiro_limpo = re.sub(r'#+', '', roteiro_limpo)
roteiro_limpo = re.sub(r'\*+', '', roteiro_limpo)
roteiro_limpo = re.sub(r'`+', '', roteiro_limpo)

# Remove textos entre parenteses
roteiro_limpo = re.sub(r'\(.*?\)', '', roteiro_limpo)

# Remove markdown **
roteiro_limpo = re.sub(r'\*\*', '', roteiro_limpo)

# Remove "Locutor:"
roteiro_limpo = re.sub(r'Locutor:', '', roteiro_limpo)

# Remove espaços extras
roteiro_limpo = re.sub(r'\n\s*\n', '\n\n', roteiro_limpo)

roteiro_limpo = roteiro_limpo.strip()

print(roteiro_limpo)

# Gera audio a partir do resumo
import edge_tts
import asyncio

texto = roteiro_limpo

async def gerar_audio():

    communicate = edge_tts.Communicate(
        texto,
        voice="pt-BR-AntonioNeural"
    )

    await communicate.save("audio_edge2.mp3")

await gerar_audio()

!apt-get install ffmpeg -y

# Converte mp3 para wav
!ffmpeg -i audio_edge2.mp3 audio_edge2.wav

# Envia áudio ao bot Telegram
import requests

CHAT_ID = "6553931753"

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendAudio"

files = {
    'audio': open('audio_edge2.mp3', 'rb')
}

data = {
    'chat_id': CHAT_ID
}

response = requests.post(
    url,
    files=files,
    data=data
)

print(response.text)

# Envia mensagem ao bot Telegram
import requests

CHAT_ID = "6553931753"

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": roteiro_limpo
}

response = requests.post(
    url,
    data=data
)

print(response.text)

# Cria um arquivo texto com o roteiro
with open("roteiro.txt", "w", encoding="utf-8") as f:
    f.write(roteiro_audio)

print("TXT salvo!")

# Download dos arquivos
from google.colab import files

files.download("roteiro.txt")
files.download("audio.mp3")
files.download("audio.wav")
files.download("audio_edge2.mp3")
files.download("audio_edge2.wav")
