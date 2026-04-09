"""AI Story Narrator — generates a story with MiniMax chat, then narrates it with TTS."""

from pathlib import Path
from rich.console import Console
from .client import MiniMaxClient
from . import tts

console = Console()

STORY_SYSTEM_PROMPT = (
    "You are a world-class storyteller. Write vivid, engaging short stories "
    "that are perfect for audio narration. Keep stories between 200-500 words. "
    "Use descriptive language and natural dialogue."
)


def generate_story(
    topic: str,
    voice: str = "narrator",
    output_dir: str = "output",
) -> dict:
    """Generate a story about a topic, then narrate it as audio."""
    console.print(f"\n[bold magenta]AI Story Narrator[/]")
    console.print(f"  Topic: {topic}\n")

    # Step 1: Generate the story text
    console.print("[bold blue]Step 1:[/] Generating story with MiniMax LLM...")
    with MiniMaxClient() as client:
        story_text = client.chat(
            prompt=f"Write a short story about: {topic}",
            system_prompt=STORY_SYSTEM_PROMPT,
        )
    console.print(f"[dim]{story_text[:200]}...[/]\n")

    # Step 2: Save the story text
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    story_file = out / "story.txt"
    story_file.write_text(story_text)
    console.print(f"[bold green]Story saved:[/] {story_file}")

    # Step 3: Narrate the story
    console.print("\n[bold blue]Step 2:[/] Narrating story with MiniMax TTS...")
    audio_path = tts.synthesize(
        text=story_text,
        voice=voice,
        output_dir=output_dir,
        filename="story_narration.mp3",
    )

    return {
        "story_text": story_text,
        "story_file": str(story_file),
        "audio_file": str(audio_path),
    }
