"""Small reusable UI and validation helpers."""

from __future__ import annotations

import json
import streamlit as st


def validate_text(value: str, label: str) -> bool:
    if not value or not value.strip():
        st.warning(f"Please provide {label} before continuing.")
        return False
    return True


def copy_widget(value: str, key: str) -> None:
    """Render a browser-side clipboard button."""
    # JSON safely escapes quotes, newlines, and backticks before browser-side use.
    safe_value = json.dumps(value)
    st.components.v1.html(
        f'''<button id="{key}" style="padding:8px 14px;border:0;border-radius:6px;background:#5b4bdb;color:white;cursor:pointer">Copy to clipboard</button>
        <script>document.getElementById("{key}").onclick=async()=>{{await navigator.clipboard.writeText({safe_value});document.getElementById("{key}").innerText="Copied!"}}</script>''',
        height=45,
    )


def download_button(value: str, filename: str, key: str) -> None:
    st.download_button("Download as TXT", data=value, file_name=filename, mime="text/plain", key=key)
