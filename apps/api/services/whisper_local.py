from io import BytesIO

from apps.api.core.config import get_settings


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
        except Exception:
            self._model = False
        return self._model

    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        model = self._load_model()
        if not model:
            return "mock transcription"
        audio_stream = BytesIO(audio_bytes)
        segments, _ = model.transcribe(audio_stream, beam_size=1)
        return " ".join(segment.text.strip() for segment in segments).strip() or ""
