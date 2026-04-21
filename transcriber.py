"""
Real-time Japanese audio transcription using faster-whisper.
"""
import queue
import threading
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
CHUNK_SECONDS = 3  # process every N seconds
CHUNK_SAMPLES = SAMPLE_RATE * CHUNK_SECONDS


class Transcriber:
    def __init__(self, model_size="medium", device_index=None, on_transcript=None):
        print(f"Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(model_size, device="auto", compute_type="auto")
        print("Model loaded.")
        self.device_index = device_index
        self.on_transcript = on_transcript
        self.audio_queue = queue.Queue()
        self.running = False
        self._buffer = np.array([], dtype=np.float32)

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[Audio status] {status}")
        self._buffer = np.concatenate([self._buffer, indata[:, 0]])
        if len(self._buffer) >= CHUNK_SAMPLES:
            chunk = self._buffer[:CHUNK_SAMPLES].copy()
            self._buffer = self._buffer[CHUNK_SAMPLES:]
            self.audio_queue.put(chunk)

    def _process_loop(self):
        while self.running:
            try:
                chunk = self.audio_queue.get(timeout=1)
            except queue.Empty:
                continue
            segments, _ = self.model.transcribe(
                chunk,
                language="ja",
                beam_size=5,
                vad_filter=True,
            )
            text = "".join(s.text for s in segments).strip()
            if text and self.on_transcript:
                self.on_transcript(text)

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._process_loop, daemon=True)
        self._thread.start()
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=self.device_index,
            callback=self._audio_callback,
        )
        self._stream.start()
        print("Transcriber started. Listening...")

    def stop(self):
        self.running = False
        self._stream.stop()
        self._stream.close()
