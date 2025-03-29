import asyncio
import aiofiles
from woolball_speech_to_text import WoolBallSpeechToTextService, TranscriptionOptions


async def main():
    service = WoolBallSpeechToTextService(api_key="")

    try:
        url_en = "https://cdn.pixabay.com/download/audio/2022/03/10/audio_64f911f820.mp3?filename=hello-what-you-doing-42455.mp3"
        url_es = "http://pt.nemolanguageapps.com/audio/mp3/SPAFND1_0042.mp3"

        # Example 1: Basic speech-to-text extraction from URL
        print("Processing test cases...")
        result1 = service.transcribe_from_url(url_en)
        print(f"Transcription: {result1['data']}\n")
        # Example 2: Speech-to-text extraction from URL with timestamps (English audio) ✔️
        result2 = service.transcribe_from_url_with_timestamps(
            url_en,
            language="en"
        )

        print("\nTranscription with timestamps:")
        for chunk in result2['data']['chunks']:
            print(f"{chunk['timestamp'][0]:.2f}s -> {chunk['timestamp'][1]:.2f}s: {chunk['text']}")

        # Example 3: Transcription from URL with WebVTT subtitles (Spanish audio)
        result3 = service.transcribe_from_url_with_webvtt(
            url_es,
            language="es"
        )
        print(f"\nTranscription with WebVTT:\n{result3['data']['webvtt']}")

        # Example 4: Transcription from file with WebVTT subtitles (Portuguese audio)
        async with aiofiles.open("audio_pt.mp3", "rb") as file:
            audio_data = await file.read()
            result4 = service.transcribe_from_file_with_webvtt(
                audio_data,
                language="pt"
            )

            print(f"\nTranscription with WebVTT:\n{result4['data']['webvtt']}")
            
            # Save WebVTT subtitles to file
            async with aiofiles.open("subtitles.vtt", "w") as vtt_file:
                await vtt_file.write(result4['data']['webvtt'])
            print("\nWebVTT subtitles saved to 'subtitles.vtt'")

        # Example 5: Advanced usage with custom options
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
        print(f"\nTranscription with timestamps and WebVTT:\n{result5['data']['webvtt']}")
        
        # Example 6: Get available models
        models = service.get_available_models()
        print("\nAvailable models:")
        for model in models['data']:
            print(f"- {model['model']}")
            
        # Example 7: Transcription from file
        with open("audio_pt.mp3", "rb") as f:
            audio_data = f.read()
            
            result7 = service.transcribe_from_file(
                audio_data,
                TranscriptionOptions(language="pt"),
                filename="audio_pt.mp3"
            )
        
        print(f"\nTranscription from file: {result7['data']}")

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
