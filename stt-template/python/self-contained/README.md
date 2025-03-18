# WoolBall Speech-to-Text Python Template (Self-Contained)

Este template fornece uma implementação Python para integração com a API WoolBall Speech-to-Text, permitindo transcrever áudio em texto com suporte a múltiplos idiomas e formatos.

## Requisitos

- Python 3.7+
- Pacotes: `requests`, `requests_toolbelt`, `aiofiles` (opcional, para uso assíncrono)

## Instalação

```bash
pip install requests requests_toolbelt
pip install aiofiles  # Opcional, para uso assíncrono
```

## Uso Básico

```python
from woolball_speech_to_text import WoolBallSpeechToTextService

# Inicializar o serviço 
service = WoolBallSpeechToTextService()  # Adicione sua chave API se necessário

# Transcrever a partir de uma URL
result = service.transcribe_from_url("https://exemplo.com/audio.mp3")
print(f"Transcrição: {result['data']}")

# Transcrever a partir de um arquivo local
with open("audio.mp3", "rb") as f:
    audio_data = f.read()
    result = service.transcribe_from_file(
        audio_data,
        filename="audio.mp3"
    )
    print(f"Transcrição: {result['data']}")
```

## Funcionalidades

### Transcrição com Timestamps

```python
# Transcrição com timestamps a partir de URL
result = service.transcribe_from_url_with_timestamps(
    "https://exemplo.com/audio.mp3",
    language="en"
)

print("Transcrição com timestamps:")
for chunk in result['data']['chunks']:
    print(f"{chunk['timestamp'][0]:.2f}s -> {chunk['timestamp'][1]:.2f}s: {chunk['text']}")

# Transcrição com timestamps a partir de arquivo
with open("audio.mp3", "rb") as f:
    audio_data = f.read()
    result = service.transcribe_from_file_with_timestamps(
        audio_data,
        language="pt",
        filename="audio.mp3"
    )
```

### Geração de Legendas WebVTT

```python
# Obter legendas WebVTT a partir de URL
result = service.transcribe_from_url_with_webvtt(
    "https://exemplo.com/audio.mp3",
    language="es"
)
print(f"Legendas WebVTT:\n{result['data']['webvtt']}")

# Obter legendas WebVTT a partir de arquivo e salvar em arquivo .vtt
import aiofiles
import asyncio

async def process_audio():
    async with aiofiles.open("audio.mp3", "rb") as file:
        audio_data = await file.read()
        
        result = service.transcribe_from_file_with_webvtt(
            audio_data,
            language="pt"
        )
        
        # Salvar as legendas em um arquivo .vtt
        async with aiofiles.open("legendas.vtt", "w") as vtt_file:
            await vtt_file.write(result['data']['webvtt'])
        print("Legendas salvas em 'legendas.vtt'")

asyncio.run(process_audio())
```

### Opções de Transcrição Personalizadas

O serviço aceita várias opções para personalizar as transcrições:

```python
from woolball_speech_to_text import TranscriptionOptions

# Configurar opções personalizadas
options = TranscriptionOptions(
    model="onnx-community/whisper-large-v3-turbo_timestamped",  # Modelo a ser usado
    language="pt",  # Idioma do áudio (pt, en, es, etc.)
    return_timestamps=True,  # Incluir timestamps para cada segmento
    webvtt=True  # Gerar legendas em formato WebVTT
)

# Usar as opções personalizadas
result = service.transcribe_from_url(
    "https://exemplo.com/audio.mp3",
    options
)
print(f"Transcrição com opções personalizadas:\n{result['data']['webvtt']}")
```

### Modelos Disponíveis

```python
# Obter modelos disponíveis
models = service.get_available_models()
print("Modelos disponíveis:")
for model in models['data']:
    print(f"- {model['model']}")
```

### Suporte a Diferentes Tipos de Entrada

O serviço aceita diferentes formatos de entrada para arquivos:

```python
# A partir de dados binários
with open("audio.mp3", "rb") as f:
    audio_data = f.read()
    result = service.transcribe_from_file(
        audio_data,
        TranscriptionOptions(language="pt"),
        filename="audio.mp3"
    )

# A partir de um objeto BytesIO
from io import BytesIO
audio_stream = BytesIO(audio_data)
result = service.transcribe_from_file(
    audio_stream,
    TranscriptionOptions(language="pt"),
    filename="audio.mp3"
)

# A partir do caminho de um arquivo (string)
result = service.transcribe_from_file(
    "caminho/para/audio.mp3",
    TranscriptionOptions(language="pt"),
    filename="audio.mp3"
)
```

## Exemplo Completo

Consulte o arquivo `usage.py` incluído neste template para ver exemplos completos de uso da API, incluindo:

1. Transcrição básica a partir de URL
2. Transcrição com timestamps
3. Transcrição com legendas WebVTT
4. Transcrição a partir de arquivo local
5. Uso avançado com opções personalizadas
6. Listagem de modelos disponíveis
7. Transcrição a partir de um caminho de arquivo

## Formatos Suportados

O serviço suporta diversos formatos de áudio e vídeo, incluindo:
- Áudio: MP3, WAV, OGG
- Vídeo: MP4, MOV, WEBM, MKV, AVI

## Observações

- Certifique-se de ter conexão à internet, pois o serviço requer acesso à API WoolBall
- Para usos intensivos, considere implementar um mecanismo de cache para evitar processamento duplicado
