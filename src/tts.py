"""Text-to-Speech pipeline using MiniMax."""

import os
from pathlib import Path
from rich.console import Console
from .client import MiniMaxClient

console = Console()

VOICE_PRESETS = {
    "male-calm": "male-qn-qingse",
    "male-warm": "male-qn-jingying",
    "female-gentle": "female-shaonv",
    "female-warm": "female-yujie",
    "narrator": "presenter_male",
    "audiobook": "audiobook_male_1",
}


def list_voices() -> dict:
    """Return available voice presets."""
    return VOICE_PRESETS


def synthesize(
    text: str,
    voice: str = "narrator",
    output_dir: str = "output",
    filename: str = "tts_output.mp3",
    speed: float = 1.0,
) -> Path:
    """Synthesize speech from text and save to file."""
    voice_id = VOICE_PRESETS.get(voice, voice)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    output_path = out / filename

    console.print(f"[bold blue]Synthesizing speech...[/]")
    console.print(f"  Voice: {voice} ({voice_id})")
    console.print(f"  Text length: {len(text)} chars")

    with MiniMaxClient() as client:
        audio_bytes = client.text_to_speech(text=text, voice_id=voice_id, speed=speed)

    output_path.write_bytes(audio_bytes)
    console.print(f"[bold green]Saved:[/] {output_path} ({len(audio_bytes)} bytes)")
    return output_path
