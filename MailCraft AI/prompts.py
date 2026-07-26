"""Prompt builders for MailCraft AI.

Keeping prompts here makes them easy to inspect and improve without touching UI code.
"""

from __future__ import annotations

EMAIL_SYSTEM = """You are MailCraft AI, a careful professional email-writing assistant.
Write accurate, natural, ready-to-send emails. Never invent names, dates, job titles,
achievements, links, or commitments that the user did not give you. If a detail is
missing, use neutral wording or a short [placeholder]. Avoid repetition, filler,
exaggerated claims, and markdown. Return only the requested result."""


def build_generation_prompt(purpose: str, recipient: str, tone: str, length: str, instructions: str) -> str:
    """Create a focused prompt for an original email."""
    length_guidance = {
        "Short": "60-100 words",
        "Medium": "120-180 words",
        "Detailed": "200-300 words",
    }[length]
    custom_recipient = recipient if recipient != "Custom" else "the recipient described in the instructions"
    return f"""Create an email for this purpose: {purpose}.
Recipient: {custom_recipient}.
Tone: {tone}.
Target length: {length_guidance}.
Additional instructions: {instructions or 'None provided.'}

Use exactly this format:
Subject: <concise realistic subject>

<email body with greeting, concise paragraphs, and sign-off>."""


def build_rewrite_prompt(email: str, style: str) -> str:
    return f"""Rewrite the email below to be {style}. Preserve its facts and intent.
Then add a section headed 'Improvements made:' with 3-5 short bullet points explaining
the changes. Do not add facts.

EMAIL:
{email}"""


def build_grammar_prompt(email: str) -> str:
    return f"""Review the email below. Return these four clearly headed sections:
1. Grammar corrections (specific corrections, or 'No major errors found')
2. Professional suggestions (up to 4 practical points)
3. Improved version (the complete corrected email)
4. Tone and readability (tone summary plus a readability score from 1-100 with one-sentence explanation)
Do not invent facts or change the sender's meaning.

EMAIL:
{email}"""


def build_template_prompt(template_name: str, template: str, instructions: str) -> str:
    return f"""Customize this {template_name} email template using only the user's supplied details.
Keep bracketed details as placeholders when they are not supplied. Provide a subject and ready-to-send email.

TEMPLATE:
{template}

USER CUSTOMIZATION:
{instructions or 'Keep the template general.'}"""
