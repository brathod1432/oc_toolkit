# Skill: NVIDIA API Integration (nvidia-custom provider)

**When to use this skill:**
User asks to call NVIDIA models directly in code, build an LLM-powered
feature, or test model connectivity outside of opencode.

---

## Active Provider Details

```
Provider : nvidia-custom
Base URL : https://integrate.api.nvidia.com/v1
Auth     : Bearer token via NVIDIA_API_KEY env var
Protocol : OpenAI-compatible (uses @ai-sdk/openai-compatible in opencode)
```

---

## Available Models (as of project setup)

| Model ID | Best for | Temp |
|---|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b` | Reasoning, code, planning | 0.1–0.3 |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning` | Math, finance, step-by-step | 0.0–0.1 |
| `nvidia/nemotron-3.5-lightning-30b-a3b` | Fast lightweight tasks | 0.2–0.4 |
| `meta/muse-glimmer-30b` | Creative, social, email | 0.7–0.9 |
| `google/gemma-4-31b-it` | Structured output, ads | 0.3–0.5 |
| `z-ai/glm-5.3` | Classification, support | 0.2–0.4 |

---

## Python Client Pattern

```python
# path/to/nvidia_client.py
import os
import httpx
from typing import Any

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
if not NVIDIA_API_KEY:
    raise RuntimeError("NVIDIA_API_KEY not set")

BASE_URL = "https://integrate.api.nvidia.com/v1"

HEADERS = {
    "Authorization": f"Bearer {NVIDIA_API_KEY}",
    "Content-Type": "application/json",
}


async def chat(
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    max_tokens: int = 1024,
) -> str:
    """Call NVIDIA chat completions endpoint. Returns the assistant reply text."""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{BASE_URL}/chat/completions",
            headers=HEADERS,
            json={
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


# ── Example usage ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import asyncio

    async def main():
        reply = await chat(
            model="nvidia/nemotron-3-ultra-550b-a55b",
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
        )
        print(reply)

    asyncio.run(main())
```

---

## Streaming Pattern

```python
async def chat_stream(model: str, messages: list[dict]) -> AsyncIterator[str]:
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST",
            f"{BASE_URL}/chat/completions",
            headers=HEADERS,
            json={"model": model, "messages": messages, "stream": True},
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    chunk = json.loads(line[6:])
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
```

---

## Error Handling

```python
try:
    reply = await chat(model=MODEL, messages=msgs)
except httpx.HTTPStatusError as exc:
    if exc.response.status_code == 429:
        # rate limited — back off and retry
        await asyncio.sleep(5)
    elif exc.response.status_code == 401:
        raise RuntimeError("Invalid NVIDIA API key") from exc
    else:
        raise
except httpx.TimeoutException:
    # model took >60s — consider a lighter model or smaller max_tokens
    raise
```

---

## Requirements

```
httpx>=0.27
```

No openai SDK needed — the endpoint is OpenAI-compatible but plain httpx
keeps the dependency footprint minimal and avoids SDK version conflicts.

---

## Security Rules

- NEVER hardcode the API key value in any file
- NEVER log the key even partially
- NEVER commit `.env` to git
- The key format is `nvapi-...` — if it appears in a diff, abort and rotate it
