"""Shared Anthropic client for TherapyNavigator.

Loads the API key from Streamlit secrets (cloud) or a local .env file, builds a
single cached Anthropic client, and exposes two thin call helpers used by the
four tool pages.
"""

import os

import streamlit as st
from anthropic import Anthropic, APIConnectionError, APIStatusError, RateLimitError

MODEL = "claude-sonnet-4-6"

FRIENDLY_ERRORS = {
    "no_key": (
        "No Anthropic API key found. Add ANTHROPIC_API_KEY to your .env file "
        "locally, or to your app secrets on Streamlit Cloud, then try again."
    ),
    "rate_limit": (
        "The AI service is busy right now (rate limited). Wait a few seconds "
        "and try again."
    ),
    "connection": (
        "Could not reach the AI service. Check your internet connection and "
        "try again."
    ),
}


def get_api_key():
    """Return the API key from st.secrets, falling back to .env / environment."""
    try:
        return st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except Exception:
            pass
        return os.getenv("ANTHROPIC_API_KEY")


@st.cache_resource(show_spinner=False)
def get_client():
    """Build the Anthropic client once per session process."""
    api_key = get_api_key()
    if not api_key or api_key == "your_key_here":
        return None
    return Anthropic(api_key=api_key)


def api_key_configured():
    """True when a usable key is present — used to warn before a call is made."""
    return get_client() is not None


def call_claude(system_prompt, user_message, max_tokens=1500):
    """Single-turn call. Returns the response text, or a friendly error string."""
    return call_claude_messages(
        system_prompt,
        [{"role": "user", "content": user_message}],
        max_tokens=max_tokens,
    )


def call_claude_messages(system_prompt, messages, max_tokens=1500):
    """Multi-turn call. `messages` is a list of {"role", "content"} dicts."""
    client = get_client()
    if client is None:
        return "ERROR: " + FRIENDLY_ERRORS["no_key"]

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=messages,
        )
        return "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()
    except RateLimitError:
        return "ERROR: " + FRIENDLY_ERRORS["rate_limit"]
    except APIConnectionError:
        return "ERROR: " + FRIENDLY_ERRORS["connection"]
    except APIStatusError as exc:
        return (
            "ERROR: The AI service returned an error (status {}). "
            "Please try again in a moment.".format(exc.status_code)
        )
    except Exception as exc:  # last-resort guard so a page never hard-crashes
        return "ERROR: Something went wrong ({}). Please try again.".format(
            type(exc).__name__
        )


def is_error(text):
    """True when a call helper returned a friendly error instead of a response."""
    return isinstance(text, str) and text.startswith("ERROR: ")


def error_body(text):
    """Strip the ERROR: prefix for display in st.error()."""
    return text[len("ERROR: "):] if is_error(text) else text
