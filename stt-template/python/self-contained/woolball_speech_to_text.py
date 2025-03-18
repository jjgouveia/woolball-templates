import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
import io
from requests_toolbelt import MultipartEncoder
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class TranscriptionOptions:
    model: str = "onnx-community/whisper-large-v3-turbo_timestamped"
    language: str = "pt"
    return_timestamps: bool = False
    webvtt: bool = False

class WoolBallSpeechToTextService:
    """Service client for WoolBall Speech-to-Text API."""
    
    def __init__(self, api_key: str = ""):
        """
        Initialize the WoolBall Speech-to-Text service.
        
        Args:
            api_key: Your WoolBall API key
        """
        self.base_url = "https://api.woolball.xyz/v1"
        self.headers = {'Authorization': f'Bearer {api_key}'}
    
    def transcribe_from_url(self, audio_url: str, options: Optional[TranscriptionOptions] = None) -> Dict[str, Any]:
        """
        Transcribe audio from a URL.
        
        Args:
            audio_url: URL of the audio file to transcribe
            options: Optional transcription options
            
        Returns:
            Transcription response from the API
        """
        if options is None:
            options = TranscriptionOptions()
        
        files = {
            'url': (None, audio_url),
            'model': (None, options.model),
            'language': (None, options.language),
            'returnTimestamps': (None, str(options.return_timestamps).lower()),
            'webvtt': (None, str(options.webvtt).lower())
        }
        
        response = requests.post(
            f"{self.base_url}/speech-to-text",
            headers=self.headers,
            files=files
        )
        
        response.raise_for_status()
        return response.json()
    
    def transcribe_from_url_with_timestamps(self, audio_url: str, language: str = "pt") -> Dict[str, Any]:
        """
        Transcribe audio from a URL with timestamps.
        
        Args:
            audio_url: URL of the audio file to transcribe
            language: Language of the audio
            
        Returns:
            Transcription response with timestamps
        """
        options = TranscriptionOptions(
            language=language,
            return_timestamps=True
        )
        return self.transcribe_from_url(audio_url, options)
    
    def transcribe_from_url_with_webvtt(self, audio_url: str, language: str = "pt") -> Dict[str, Any]:
        """
        Transcribe audio from a URL and get WebVTT subtitles.
        
        Args:
            audio_url: URL of the audio file to transcribe
            language: Language of the audio
            
        Returns:
            Transcription response with WebVTT subtitles
        """
        options = TranscriptionOptions(
            language=language,
            return_timestamps=True,
            webvtt=True
        )
        return self.transcribe_from_url(audio_url, options)
    
    def transcribe_from_file(self, 
                            audio_data: Union[bytes, io.BytesIO, str], 
                            options: Optional[TranscriptionOptions] = None,
                            filename: str = "audio.mp3") -> Dict[str, Any]:
        """
        Transcribe audio from file data.
        
        Args:
            audio_data: Binary audio data, BytesIO object, or path to audio file
            options: Optional transcription options
            filename: Original filename to send to API
            
        Returns:
            Transcription response from the API
        """
        if options is None:
            options = TranscriptionOptions()
        
        if isinstance(audio_data, str):
            with open(audio_data, 'rb') as f:
                file_content = f.read()
        elif isinstance(audio_data, io.BytesIO):
            file_content = audio_data.getvalue()
        else:
            file_content = audio_data
        
        mime_type = "audio/mpeg"
        if filename.lower().endswith('.wav'):
            mime_type = "audio/wav"
        elif filename.lower().endswith('.ogg'):
            mime_type = "audio/ogg"
        elif filename.lower().endswith('.mp4') or filename.lower().endswith('.mov'):
            mime_type = "video/mp4"
        elif filename.lower().endswith('.webm'):
            mime_type = "video/webm"
        elif filename.lower().endswith('.mkv'):
            mime_type = "video/x-matroska"
        elif filename.lower().endswith('.avi'):
            mime_type = "video/x-msvideo"

        
        multipart_data = MultipartEncoder(
            fields={
                'audio': (filename, file_content, mime_type),
                'model': options.model,
                'language': options.language,
                'returnTimestamps': str(options.return_timestamps).lower(),
                'webvtt': str(options.webvtt).lower()
            }
        )
        
        headers = self.headers.copy()
        headers['Content-Type'] = multipart_data.content_type

        response = requests.post(
            f"{self.base_url}/speech-to-text",
            headers=headers,
            data=multipart_data
        )

        try:
            if response.status_code != 200:
                if response.text:
                    try:
                        error_data = response.json()
                        logger.error(f"Erro: {error_data}")
                        return error_data
                    except:
                        logger.error(f"Resposta de erro não-JSON: {response.text}")
                        return {"error": f"HTTP {response.status_code}: {response.reason}", "details": response.text}
                else:
                    return {"error": f"HTTP {response.status_code}: {response.reason}"}
            
            if response.text:
                return response.json()
            else:
                return {"warning": "Resposta vazia do servidor"}
        except Exception as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return {"error": str(e)}
    
    def transcribe_from_file_with_timestamps(self, 
                                           audio_data: Union[bytes, io.BytesIO, str], 
                                           language: str = "pt",
                                           filename: str = "audio.mp3") -> Dict[str, Any]:
        """
        Transcribe audio from file data with timestamps.
        
        Args:
            audio_data: Binary audio data, BytesIO object, or path to audio file
            language: Language of the audio
            filename: Original filename to send to API
            
        Returns:
            Transcription response with timestamps
        """
        options = TranscriptionOptions(
            language=language,
            return_timestamps=True
        )
        return self.transcribe_from_file(audio_data, options, filename)
    
    def transcribe_from_file_with_webvtt(self, 
                                        audio_data: Union[bytes, io.BytesIO, str], 
                                        language: str = "pt",
                                        filename: str = "audio.mp3") -> Dict[str, Any]:
        """
        Transcribe audio from file data and get WebVTT subtitles.
        
        Args:
            audio_data: Binary audio data, BytesIO object, or path to audio file
            language: Language of the audio
            filename: Original filename to send to API
            
        Returns:
            Transcription response with WebVTT subtitles
        """
        options = TranscriptionOptions(
            language=language,
            return_timestamps=True,
            webvtt=True
        )
        logger.info("Enviando arquivo para transcrição com WebVTT...")
        return self.transcribe_from_file(audio_data, options, filename)
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get available speech-to-text models.
        
        Returns:
            List of available models
        """
        response = requests.get(
            f"{self.base_url}/models/speech-to-text",
            headers=self.headers
        )
        
        response.raise_for_status()
        return response.json()
