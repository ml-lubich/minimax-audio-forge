"""MiniMax API client wrapper."""

import httpx
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

BASE_URL = "https://api.minimaxi.chat/v1"


class MiniMaxClient:
    """HTTP client for the MiniMax API."""

    def __init__(self, api_key: Optional[str] = None, group_id: Optional[str] = None):
        self.api_key = api_key or os.getenv("MINIMAX_API_KEY")
        self.group_id = group_id or os.getenv("MINIMAX_GROUP_ID", "")
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY is required. Set it in .env or pass it directly.")
        self._http = httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout=120.0,
        )

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "male-qn-qingse",
        model: str = "speech-01-turbo",
        speed: float = 1.0,
        pitch: int = 0,
    ) -> bytes:
        """Convert text to speech audio using MiniMax TTS."""
        payload = {
            "model": model,
            "text": text,
            "stream": False,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": speed,
                "vol": 1.0,
                "pitch": pitch,
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3",
            },
        }
        if self.group_id:
            resp = self._http.post(f"/t2a_v2?GroupId={self.group_id}", json=payload)
        else:
            resp = self._http.post("/t2a_v2", json=payload)
        resp.raise_for_status()
        data = resp.json()
        if "data" in data and "audio" in data["data"]:
            import base64
            return base64.b64decode(data["data"]["audio"])
        if "extra_info" in data:
            raise RuntimeError(f"MiniMax TTS error: {data.get('base_resp', data)}")
        raise RuntimeError(f"Unexpected TTS response: {data}")

    def generate_music(
        self,
        prompt: str,
        model: str = "music-01",
        duration: int = 30,
    ) -> bytes:
        """Generate music from a text prompt using MiniMax Music."""
        payload = {
            "model": model,
            "prompt": prompt,
            "duration": duration,
        }
        if self.group_id:
            resp = self._http.post(f"/music_generation?GroupId={self.group_id}", json=payload)
        else:
            resp = self._http.post("/music_generation", json=payload)
        resp.raise_for_status()
        data = resp.json()
        if "data" in data and "audio" in data["data"]:
            import base64
            return base64.b64decode(data["data"]["audio"])
        raise RuntimeError(f"Unexpected music generation response: {data}")

    def chat(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful creative writing assistant.",
        model: str = "MiniMax-Text-01",
        max_tokens: int = 2048,
    ) -> str:
        """Send a chat completion request to MiniMax."""
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_tokens,
        }
        resp = self._http.post("/text/chatcompletion_v2", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
