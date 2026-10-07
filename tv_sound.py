from __future__ import annotations

import io
import math
import struct
import wave


def notification_tone() -> bytes:
    sample_rate = 22050
    duration_seconds = 0.24
    frequency_hz = 880
    sample_count = int(sample_rate * duration_seconds)
    audio_buffer = io.BytesIO()

    with wave.open(audio_buffer, "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(sample_rate)
        for sample_index in range(sample_count):
            elapsed = sample_index / sample_rate
            envelope = min(1.0, elapsed / 0.015, (duration_seconds - elapsed) / 0.04)
            amplitude = int(0.16 * 32767 * envelope * math.sin(2 * math.pi * frequency_hz * elapsed))
            output.writeframesraw(struct.pack("<h", amplitude))

    return audio_buffer.getvalue()