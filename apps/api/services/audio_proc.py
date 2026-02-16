import hashlib

from apps.api.services.deid import Deidentifier
from apps.api.services.whisper_local import WhisperLocalService


class AudioProcessor:
    def __init__(self, whisper_service: WhisperLocalService | None = None, deidentifier: Deidentifier | None = None) -> None:
        self.whisper = whisper_service or WhisperLocalService()
        self.deidentifier = deidentifier or Deidentifier()

    def process_audio_bytes(self, audio_bytes: bytes, deidentify: bool) -> tuple[str, str, int]:
        buf = bytearray(audio_bytes)
        transcript = self.whisper.transcribe_bytes(bytes(buf))

        redaction_count = 0
        if deidentify:
            transcript, entities = self.deidentifier.deidentify(transcript)
            redaction_count = len(entities)

        transcript_id = hashlib.sha256(transcript.encode("utf-8")).hexdigest()[:16]
        self._purge_buffer(buf)
        return transcript_id, transcript, redaction_count

    @staticmethod
    def _purge_buffer(buf: bytearray) -> None:
        buf.clear()
