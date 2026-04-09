#!/usr/bin/env python3
"""MiniMax Audio Forge — CLI interface."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def main():
    """MiniMax Audio Forge — AI-powered audio content generation."""
    pass


@main.command()
@click.argument("text")
@click.option("--voice", "-v", default="narrator", help="Voice preset or voice_id")
@click.option("--output", "-o", default="output", help="Output directory")
@click.option("--filename", "-f", default="tts_output.mp3", help="Output filename")
@click.option("--speed", "-s", default=1.0, help="Speech speed (0.5–2.0)")
def speak(text, voice, output, filename, speed):
    """Convert text to speech."""
    from src.tts import synthesize
    synthesize(text=text, voice=voice, output_dir=output, filename=filename, speed=speed)


@main.command()
@click.argument("prompt")
@click.option("--duration", "-d", default=30, help="Duration in seconds")
@click.option("--output", "-o", default="output", help="Output directory")
@click.option("--filename", "-f", default="music_output.mp3", help="Output filename")
def music(prompt, duration, output, filename):
    """Generate music from a text prompt."""
    from src.music import generate
    generate(prompt=prompt, duration=duration, output_dir=output, filename=filename)


@main.command()
@click.argument("topic")
@click.option("--voice", "-v", default="narrator", help="Narrator voice preset")
@click.option("--output", "-o", default="output", help="Output directory")
def story(topic, voice, output):
    """Generate and narrate an AI story."""
    from src.story import generate_story
    result = generate_story(topic=topic, voice=voice, output_dir=output)
    console.print(f"\n[bold green]Done![/]")
    console.print(f"  Story: {result['story_file']}")
    console.print(f"  Audio: {result['audio_file']}")


@main.command()
def voices():
    """List available voice presets."""
    from src.tts import list_voices
    table = Table(title="Voice Presets")
    table.add_column("Name", style="cyan")
    table.add_column("Voice ID", style="green")
    for name, vid in list_voices().items():
        table.add_row(name, vid)
    console.print(table)


if __name__ == "__main__":
    main()
