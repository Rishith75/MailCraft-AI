"""MailCraft AI — a polished, beginner-friendly Groq email assistant."""

from __future__ import annotations

import streamlit as st

import os
from pathlib import Path


from prompts import build_generation_prompt, build_grammar_prompt, build_rewrite_prompt, build_template_prompt
from services import FALLBACK_MODEL, PRIMARY_MODEL, api_key_available, ask_groq
from templates import TEMPLATES
from utils import copy_widget, download_button, validate_text

st.set_page_config(page_title="MailCraft AI", page_icon="✉️", layout="wide")

st.markdown("""<style>
 .stApp { background: #f8f8fc; } .hero {padding: 1.5rem 0 .8rem;} .card {background:white;padding:1rem;border-radius:12px;border:1px solid #e8e7f0;min-height:105px;}
 </style>""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


def generate(prompt: str, category: str) -> str | None:
    """Run generation, save a result in session history, and return it."""
    try:
        with st.spinner("MailCraft is writing your email…"):
            result, model = ask_groq(prompt)
        st.session_state.history.insert(0, {"category": category, "content": result, "model": model})
        st.success(f"Ready — generated with {model}.")
        return result
    except ValueError as exc:
        st.error(str(exc))
    except RuntimeError as exc:
        st.error(str(exc))
    return None


def result_panel(result: str, key: str) -> None:
    st.text_area("Result", result, height=330, key=f"result_{key}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Characters", len(result))
    col2.metric("Words", len(result.split()))
    with col3:
        download_button(result, "mailcraft-email.txt", f"download_{key}")
    copy_widget(result, f"copy_{key}")


with st.sidebar:
    st.title("✉️ MailCraft AI")
    st.caption("Intelligent Email Assistant")
    st.divider()
    st.subheader("Project information")
    st.write("A free GenAI portfolio project powered by Groq + LangChain.")
    st.write(f"**Primary model:** `{PRIMARY_MODEL}`")
    st.write(f"**Fallback:** `{FALLBACK_MODEL}`")
    st.write("api_key_available():", api_key_available())
    if api_key_available():
        st.success("Groq API key detected")
    else:
        st.warning("Add GROQ_API_KEY to .env to generate emails")
    with st.expander("Tips"):
        st.write("Include concrete context, names, dates, and outcomes for better drafts.")
    with st.expander("About prompt engineering"):
        st.write("MailCraft uses structured prompts for purpose, audience, tone, and length while instructing the model not to invent facts.")
    st.divider()
    st.subheader("Generation history")
    if not st.session_state.history:
        st.caption("Your generated emails will appear here.")
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"{item['category']} · {item['model']}"):
            st.write(item["content"])
            download_button(item["content"], f"mailcraft-history-{i}.txt", f"hist_down_{i}")
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.history.pop(i)
                st.rerun()

st.markdown("<div class='hero'><h1>Craft better emails, faster.</h1><p>Generate, rewrite, polish, and personalize professional emails with free open-source LLMs.</p></div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
for col, icon, title, detail in [(c1,"✍️","Generate","Draft tailored emails"),(c2,"✨","Rewrite","Refine your message"),(c3,"🧹","Check","Improve grammar & tone"),(c4,"📄","Templates","Start from proven formats")]:
    col.markdown(f"<div class='card'><h3>{icon} {title}</h3><p>{detail}</p></div>", unsafe_allow_html=True)

tab_generate, tab_rewrite, tab_grammar, tab_templates = st.tabs(["✍️ Generate Email", "✨ Rewrite Email", "🧹 Grammar Checker", "📄 Email Templates"])

with tab_generate:
    left, right = st.columns(2)
    with left:
        purpose = st.selectbox("Purpose", ["Internship Request", "Job Application", "Leave Request", "Meeting Request", "Project Update", "Thank You", "Follow Up", "Networking"])
        recipient = st.selectbox("Recipient", ["Manager", "Professor", "Recruiter", "HR", "Friend", "Client", "Custom"])
    with right:
        tone = st.selectbox("Tone", ["Formal", "Professional", "Friendly", "Confident", "Persuasive", "Apologetic", "Grateful", "Casual"])
        length = st.selectbox("Length", ["Short", "Medium", "Detailed"], index=1)
    instructions = st.text_area("Additional Instructions", placeholder="Example: Mention my experience in Machine Learning.")
    if st.button("Generate Email", type="primary", key="generate"):
        if validate_text(instructions, "additional instructions"):
            result = generate(build_generation_prompt(purpose, recipient, tone, length, instructions), "Generated Email")
            if result: result_panel(result, "generate")

with tab_rewrite:
    email = st.text_area("Paste your email", height=220, key="rewrite_email")
    style = st.selectbox("Make it", ["More Professional", "More Friendly", "More Concise", "More Formal", "Simplify Language", "Correct Grammar", "Improve Clarity"])
    if st.button("Improve Email", type="primary", key="rewrite") and validate_text(email, "an email"):
        result = generate(build_rewrite_prompt(email, style), "Rewrite Email")
        if result: result_panel(result, "rewrite")

with tab_grammar:
    email = st.text_area("Paste an email to review", height=220, key="grammar_email")
    if st.button("Check Email", type="primary", key="grammar") and validate_text(email, "an email"):
        result = generate(build_grammar_prompt(email), "Grammar Check")
        if result: result_panel(result, "grammar")

with tab_templates:
    name = st.selectbox("Choose a template", list(TEMPLATES))
    st.text_area("Template preview", TEMPLATES[name], height=230, disabled=True)
    instructions = st.text_area("Customize it", placeholder="Example: I am a final-year CS student applying to the data team at Acme.", key="template_instructions")
    if st.button("Customize with AI", type="primary", key="template"):
        result = generate(build_template_prompt(name, TEMPLATES[name], instructions), f"Template: {name}")
        if result: result_panel(result, "template")
