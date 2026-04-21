"""
main.py - Live Japanese caption + translation
Usage: python main.py [--device N] [--model medium|large-v3] [--list-devices]
"""
import argparse
import threading
import sounddevice as sd

from transcriber import Transcriber
from translator import translate
from ui import CaptionWindow


def list_devices():
    print("\nAvailable audio input devices:")
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            print(f"  [{i}] {d['name']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Live Japanese caption & translation")
    parser.add_argument("--device", type=int, default=None, help="Audio input device index")
    parser.add_argument("--model", default="medium", help="Whisper model: medium or large-v3")
    parser.add_argument("--list-devices", action="store_true", help="List audio input devices and exit")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    window = CaptionWindow()

    def on_transcript(japanese: str):
        print(f"[JP] {japanese}")
        chinese = translate(japanese)
        print(f"[中] {chinese}")
        window.add_line(f"🇯🇵 {japanese}")
        window.add_line(f"💬 {chinese}")

    transcriber = Transcriber(
        model_size=args.model,
        device_index=args.device,
        on_transcript=on_transcript,
    )

    # Start transcriber in background thread
    t = threading.Thread(target=transcriber.start, daemon=True)
    t.start()

    try:
        window.run()
    finally:
        transcriber.stop()
        print("Stopped.")


if __name__ == "__main__":
    main()
