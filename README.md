# MBA - Web Data Mining and Scraping

Projeto desenvolvido para a disciplina **Web Data Mining and Scraping** do MBA em Engenharia de Dados.

---

# Objetivo

Construir um pipeline automatizado para:

* Captura de URLs do YouTube via Telegram
* Mineração de dados de canais do YouTube
* Extração de Shorts
* Transcrição automática de vídeos
* Sumarização utilizando IA Generativa (Google Gemini)
* Geração automática de áudio
* Retorno automatizado via Telegram

---

# Arquitetura do Pipeline

```text
Telegram Bot
↓
Captura URL do Canal YouTube
↓
Scraping dos Shorts
↓
Extração de Video IDs
↓
Transcrição Automática
↓
Sumarização com Gemini AI
↓
Geração de Roteiro
↓
Conversão Texto → Áudio
↓
Envio para Telegram
```

---

# Tecnologias Utilizadas

* Python
* Google Colab
* Telegram Bot API
* YouTube Transcript API
* Google Gemini API
* Edge-TTS / gTTS
* BeautifulSoup
* Requests
* Regex
* FFmpeg

---

# Estrutura do Projeto

```bash
.
├── notebook/
│   └── web_data_mining_and_scraping.py
│
├── outputs/
│   ├── roteiro.txt
│   ├── audio_resumo_shorts.mp3
│
├── images/
│   └── bot-telegram-print-1.jpeg
│   └── bot-telegram-print-2.jpeg
│
└── README.md
```

---

# Configurações Necessárias

## Telegram Bot

Criar bot utilizando:

```text
@BotFather
```

---

## Gemini API Key

Gerar gratuitamente em:

```text
https://aistudio.google.com/app/apikey
```

---

# Funcionalidades

* Captura automática de URLs do Telegram
* Extração de Shorts do YouTube
* Transcrição automática
* IA Generativa aplicada
* Geração automática de resumos
* Conversão texto → áudio
* Integração ponta a ponta

---

# Resultados

O projeto gera automaticamente:

* roteiro.txt
* audio_resumo_shorts.mp3

e envia o resultado diretamente para o Telegram.