import asyncio
import aiofiles
from woolball_speech_to_text import WoolBallSpeechToTextService, TranscriptionOptions


async def main():
    service = WoolBallSpeechToTextService()  # Substitua por sua chave API real

    try:
        url_en = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_64f911f820.mp3?filename=hello-what-you-doing-42455.mp3"
        url_es = "http://pt.nemolanguageapps.com/audio/mp3/SPAFND1_0042.mp3"

        mp3_file = "audio_pt.mp3"

        # Exemplo 1: Transcrição básica a partir de URL ✔️
        print("Processando casos de teste...")

        result1 = service.transcribe_from_url(url_en)
        print(f"Transcrição básica: {result1['data']}")

        # # Exemplo 2: Transcrição a partir de URL com timestamps (áudio em inglês) ✔️
        result2 = service.transcribe_from_url_with_timestamps(
            url_en,
            language="en"
        )

        print("\nTranscrição com timestamps:")
        for chunk in result2['data']['chunks']:
            print(f"{chunk['timestamp'][0]:.2f}s -> {chunk['timestamp'][1]:.2f}s: {chunk['text']}")

        # Exemplo 3: Transcrição a partir de URL com legendas WebVTT (áudio em espanhol) ✔️
        result3 = service.transcribe_from_url_with_webvtt(
            url_es,
            language="es"
        )
        print(f"\nLegendas WebVTT:\n{result3['data']['webvtt']}")

        #Exemplo 4: Transcrição a partir de arquivo local ✔️
        async with aiofiles.open("audio_pt.mp3", "rb") as file:
            audio_data = await file.read()
            
            
            result4 = service.transcribe_from_file_with_webvtt(
                audio_data,
                language="pt"
            )

            print(f"\nLegendas WebVTT:\n{result4['data']}")
            
            # Salvar as legendas em um arquivo .vtt
           
            async with aiofiles.open("legendas.vtt", "w") as vtt_file:
                await vtt_file.write(result4['data']['webvtt'])
            print("\nLegendas salvas em 'legendas.vtt'")

        #Exemplo 5: Uso avançado com opções personalizadas ✔️
        options = TranscriptionOptions(
            model="onnx-community/whisper-large-v3-turbo_timestamped",
            language="pt",
            return_timestamps=True,
            webvtt=True
        )
        result5 = service.transcribe_from_url(
            url_en,
            options
        )
        print(f"\nTranscrição com timestamps e WebVTT:\n{result5['data']['webvtt']}")
        
        #Exemplo 6: Obter modelos disponíveis ✔️
        models = service.get_available_models()
        print("\nModelos disponíveis:")
        for model in models['data']:
            print(f"- {model['model']}")
            
        # Exemplo 7: Transcrição a partir de um caminho de arquivo ✔️
        with open("audio_pt.mp3", "rb") as f:
            audio_data = f.read()
            
            result7 = service.transcribe_from_file(
                audio_data,
                TranscriptionOptions(language="pt"),
                filename="audio_pt.mp3"
            )
        
        print(f"\nTranscrição do arquivo: {result7['data']}")

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
