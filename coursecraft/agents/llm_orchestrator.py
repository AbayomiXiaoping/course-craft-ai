"""
llm_orchestrator.py
Centralized LLM client for educational synthesis.
Supports:
1. Google Gemini (GEMINI_API_KEY) - Free tier with high rate limits from Google AI Studio.
2. OpenAI (OPENAI_API_KEY)
3. Built-in academic heuristic synthesizer when offline or quota is exhausted.
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_gemini_key() -> Optional[str]:
    """Retrieves GEMINI_API_KEY from environment or root .env file."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            os.environ["GEMINI_API_KEY"] = val
                            return val
        except Exception:
            pass
    return None


def call_gemini_api(api_key: str, system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> Optional[str]:
    """Invokes Google's Gemini API via standard HTTPS REST."""
    model = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload: Dict[str, Any] = {
        "contents": [
            {
                "parts": [
                    {"text": f"System Context:\n{system_prompt}\n\nUser Request:\n{user_prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.3
        }
    }
    if "json" in system_prompt.lower():
        payload["generationConfig"]["responseMimeType"] = "application/json"

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts:
                    return parts[0].get("text", "")
    except Exception as e:
        print(f"[Gemini API Warning] Gemini invocation failed: {e}. Falling back to next provider.")
    return None


def get_openai_client():
    """Dynamically checks for OPENAI_API_KEY so runtime or .env changes are detected."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None, None
    try:
        from openai import OpenAI
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAI(api_key=api_key), model
    except Exception:
        return None, None


def generate_structured_synthesis(system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> Optional[str]:
    """Central orchestrator: checks Gemini first, then OpenAI, then heuristic fallback."""
    # 1. Check for Google Gemini free key
    gemini_key = get_gemini_key()
    if gemini_key:
        gemini_result = call_gemini_api(gemini_key, system_prompt, user_prompt, max_tokens=max_tokens)
        if gemini_result:
            return gemini_result

    # 2. Check for OpenAI key
    client, model = get_openai_client()
    if client:
        try:
            response = client.chat.completions.create(
                model=model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"} if "json" in system_prompt.lower() else None,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAI Warning] API invocation failed: {e}. Falling back to heuristic synthesizer.")

    # 3. Fallback to offline heuristic synthesizer
    return None
