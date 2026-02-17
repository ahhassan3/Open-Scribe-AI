from io import BytesIO

from apps.api.core.config import get_settings


class TranscriptionUnavailableError(RuntimeError):
    """Raised when local transcription cannot be performed safely."""


class WhisperLocalService:
    def __init__(self) -> None:
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model
        settings = get_settings()
        try:
            from faster_whisper import WhisperModel

            self._model = WhisperModel(settings.whisper_model, device="cpu", compute_type="int8")
        except Exception as exc:
            raise TranscriptionUnavailableError("Failed to initialize local Whisper model") from exc
        return self._model

    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        model = self._load_model()
        audio_stream = BytesIO(audio_bytes)
        try:
            segments, _ = model.transcribe(audio_stream, beam_size=1)
        except Exception as exc:
            raise TranscriptionUnavailableError("Local transcription failed") from exc

        transcript = " ".join(segment.text.strip() for segment in segments).strip()
        if not transcript:
            raise TranscriptionUnavailableError("Transcription produced empty output")
        return transcript
