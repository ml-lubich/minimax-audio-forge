"""Music generation pipeline using MiniMax."""

from pathlib import Path
from rich.console import Console
from .client import MiniMaxClient

console = Console()


def generate(
    prompt: str,
    duration: int = 30,
    output_dir: str = "output",
    filename: str = "music_output.mp3",
) -> Path:
    """Generate music from a text prompt and save to file."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    output_path = out / filename

    console.print(f"[bold blue]Generating music...[/]")
    console.print(f"  Prompt: {prompt}")
    console.print(f"  Duration: {duration}s")

    with MiniMaxClient() as client:
        audio_bytes = client.generate_music(prompt=prompt, duration=duration)

    output_path.write_bytes(audio_bytes)
    console.print(f"[bold green]Saved:[/] {output_path} ({len(audio_bytes)} bytes)")
    return output_path
