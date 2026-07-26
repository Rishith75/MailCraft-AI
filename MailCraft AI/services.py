"""Groq and LangChain integration."""

from __future__ import annotations

import os
import traceback
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from prompts import EMAIL_SYSTEM

PRIMARY_MODEL = "llama-3.1-8b-instant"
FALLBACK_MODEL = "llama-3.1-8b-instant"

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)
print("Loaded key:", os.getenv("GROQ_API_KEY"))

def api_key_available() -> bool:
    """Return whether a Groq key is configured without exposing it."""
    return bool(os.getenv("GROQ_API_KEY"))


def ask_groq(prompt: str):
    messages = [
        SystemMessage(content=EMAIL_SYSTEM),
        HumanMessage(content=prompt),
    ]

    model = "llama-3.1-8b-instant"

    try:
        llm = ChatGroq(
            model=model,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.45,
            max_tokens=900,
        )

        response = llm.invoke(messages)

        return response.content, model

    except Exception as e:
        raise RuntimeError(f"{type(e).__name__}: {repr(e)}")
