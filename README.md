# MiniMax Audio Forge

AI-powered audio content generation pipeline using the [MiniMax](https://www.minimaxi.com/) API. Generate speech, music, and narrated stories from text prompts.

```mermaid
flowchart LR
    USER(("👤<br/>Prompt"))
    CLI{{"💻 cli.py<br/>speak · music · story · voices"}}
    TTS["🗣 src/tts.py<br/>text → speech"]
    MUSIC["🎵 src/music.py<br/>text → music"]
    STORY["📖 src/story.py<br/>LLM + TTS"]
    CLIENT["🔌 src/client.py<br/>MiniMax API"]
    MINI(("🤖 MiniMax"))
    OUT[/"🔊 output/*.mp3 / *.wav"/]

    USER --> CLI
    CLI --> TTS
    CLI --> MUSIC
    CLI --> STORY
    TTS --> CLIENT
    MUSIC --> CLIENT
    STORY --> CLIENT
    CLIENT --> MINI
    TTS --> OUT
    MUSIC --> OUT
    STORY --> OUT

    classDef io fill:#0e1116,stroke:#2f81f7,stroke-width:1.5px,color:#e6edf3;
    classDef brain fill:#161b22,stroke:#d29922,stroke-width:1.5px,color:#e6edf3;
    classDef tool fill:#161b22,stroke:#3fb950,stroke-width:1.5px,color:#e6edf3;
    classDef out fill:#0e1116,stroke:#a371f7,stroke-width:1.5px,color:#e6edf3;
    class USER,MINI io;
    class CLI brain;
    class TTS,MUSIC,STORY,CLIENT tool;
    class OUT out;
```

## Table of contents

- [Features](#features)
- [Generation pipeline (algorithm)](#generation-pipeline-algorithm)
- [Story narration sequence](#story-narration-sequence)
- [Setup](#setup)
- [Usage](#usage)
- [Environment variables](#environment-variables)
- [Project structure](#project-structure)
- [License](#license)

## Generation pipeline (algorithm)

```mermaid
flowchart LR
    A([cli.py prompt])
    B{"subcommand?"}
    C["tts.py<br/>build TTS payload"]
    D["music.py<br/>build music payload"]
    E["story.py<br/>LLM gen story"]
    F["client.py<br/>POST MiniMax"]
    G["recv mp3 / wav bytes"]
    H["write output/&lt;name&gt;.mp3"]
    Z([done])
    A --> B
    B -- speak --> C --> F --> G --> H --> Z
    B -- music --> D --> F
    B -- story --> E --> C
    B -- voices --> F
```

## Story narration sequence

```mermaid
sequenceDiagram
    participant U as user
    participant CLI as cli.py story
    participant S as story.py
    participant T as tts.py
    participant C as client.py
    participant MM as MiniMax

    U->>CLI: "a detective on Mars"
    CLI->>S: generate(prompt)
    S->>C: chat(LLM)
    C->>MM: completion
    MM-->>C: story text
    C-->>S: text
    S->>T: speak(text, voice)
    T->>C: tts request
    C->>MM: tts
    MM-->>C: mp3 bytes
    C-->>T: bytes
    T-->>U: output/story.mp3
```

## Features

- **Text-to-Speech** — Convert any text to natural-sounding speech with multiple voice presets
- **Music Generation** — Create original music from text descriptions
- **AI Story Narrator** — Generate a short story with MiniMax LLM, then automatically narrate it with TTS

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your MiniMax API key to .env
```

## Usage

```bash
# Text-to-Speech
python cli.py speak "Hello, welcome to MiniMax Audio Forge" --voice narrator

# Generate music
python cli.py music "upbeat lo-fi hip hop beat with piano" --duration 30

# AI-generated narrated story
python cli.py story "a detective solving a mystery on Mars"

# List available voices
python cli.py voices
```

## Environment Variables

| Variable | Description |
|---|---|
| `MINIMAX_API_KEY` | Your MiniMax API key (required) |
| `MINIMAX_GROUP_ID` | Your MiniMax group ID (optional) |

## Project Structure

```
├── cli.py           # CLI entry point
├── src/
│   ├── client.py    # MiniMax API client
│   ├── tts.py       # Text-to-Speech pipeline
│   ├── music.py     # Music generation pipeline
│   └── story.py     # AI Story Narrator (LLM + TTS)
├── requirements.txt
└── .env.example
```

## License

MIT
