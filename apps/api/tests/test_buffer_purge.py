import pytest

from apps.api.services.audio_proc import AudioProcessor


class StubWhisper:
    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        return "patient has cough"


class FailingWhisper:
    def transcribe_bytes(self, audio_bytes: bytes) -> str:
        raise RuntimeError("transcription error")


class StubDeid:
    def deidentify(self, text: str):
        return text, []


def test_buffer_and_purge_no_disk_write(monkeypatch):
    wrote_files = []

    def fail_open(*args, **kwargs):
        mode = kwargs.get("mode") or (args[1] if len(args) > 1 else "r")
        if any(flag in mode for flag in ["w", "a", "x", "+"]):
            wrote_files.append(args[0] if args else "unknown")
            raise AssertionError("unexpected file write")
        return open(*args, **kwargs)

    processor = AudioProcessor(whisper_service=StubWhisper(), deidentifier=StubDeid())
    purge_sizes = []

    def capture_purge(buf: bytearray):
        purge_sizes.append(len(buf))
        buf.clear()
        purge_sizes.append(len(buf))

    monkeypatch.setattr("apps.api.services.audio_proc.open", fail_open, raising=False)
    monkeypatch.setattr(processor, "_purge_buffer", capture_purge)

    _, transcript, _ = processor.process_audio_bytes(b"123456", deidentify=False)

    assert transcript == "patient has cough"
    assert wrote_files == []
    assert purge_sizes == [6, 0]


def test_buffer_purged_when_transcription_fails(monkeypatch):
    processor = AudioProcessor(whisper_service=FailingWhisper(), deidentifier=StubDeid())
    purge_sizes = []

    def capture_purge(buf: bytearray):
        purge_sizes.append(len(buf))
        buf.clear()
        purge_sizes.append(len(buf))

    monkeypatch.setattr(processor, "_purge_buffer", capture_purge)

    with pytest.raises(RuntimeError):
        processor.process_audio_bytes(b"abcdef", deidentify=True)

    assert purge_sizes == [6, 0]
