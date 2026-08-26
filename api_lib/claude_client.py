"""Anthropic client for the TherapyNavigator API.

Framework-free: reads the key from the environment (Vercel project env vars in
production, a local .env in development) so the same module serves the FastAPI
routes and any script.
"""

import os

from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    RateLimitError,
)

MODEL = "claude-sonnet-4-6"

FRIENDLY = {
    "no_key": (
        "The server is missing its Anthropic API key. Set ANTHROPIC_API_KEY "
        "and try again."
    ),
    "rate_limit": (
        "The AI service is busy right now. Wait a few seconds and try again."
    ),
    "connection": (
        "Could not reach the AI service. Check the connection and try again."
    ),
}


class ClaudeError(Exception):
    """Raised with a message safe to show a user."""


_client = None


def _load_env():
    """Populate os.environ from a local .env when python-dotenv is available."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except Exception:
        pass


def get_client():
    """Build the Anthropic client once per warm function instance."""
    global _client
    if _client is not None:
        return _client
    _load_env()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_key_here":
        return None
    _client = Anthropic(api_key=api_key)
    return _client


def api_key_configured():
    return get_client() is not None


def call_claude(system_prompt, user_message, max_tokens=1500):
    """Single-turn call. Returns text, or raises ClaudeError with a safe message."""
    return call_claude_messages(
        system_prompt,
        [{"role": "user", "content": user_message}],
        max_tokens=max_tokens,
    )


def call_claude_messages(system_prompt, messages, max_tokens=1500):
    """Multi-turn call. `messages` is a list of {"role", "content"} dicts."""
    client = get_client()
    if client is None:
        raise ClaudeError(FRIENDLY["no_key"])

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
    except RateLimitError:
        raise ClaudeError(FRIENDLY["rate_limit"])
    except APIConnectionError:
        raise ClaudeError(FRIENDLY["connection"])
    except APIStatusError as exc:
        raise ClaudeError(
            "The AI service returned an error (status {}). "
            "Please try again in a moment.".format(exc.status_code)
        )
    except Exception as exc:
        raise ClaudeError(
            "Something went wrong ({}). Please try again.".format(
                type(exc).__name__
            )
        )

    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()
