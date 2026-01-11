# ==============================
# Marketing Beast AI v4.0 PRO
# Streamlit + Groq AI + Image Prompt + History
# ==============================

import streamlit as st
from groq import Groq, GroqError
import os
import urllib.parse
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Marketing Beast AI v4.0",
    page_icon="🦁",
    layout="wide"
)

# -----------------------------
# LOAD GROQ API KEY
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Add it to environment variables.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# HISTORY STORAGE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# UI HEADER
# -----------------------------
st.markdown("""
# 🦁 Marketing Beast AI v4.0
### AI-Powered Ad Copy & Visual Strategy
""")

# -----------------------------
# INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    niche = st.text_input("🎯 Niche", "Spiritual Growth & Mindset")
    platform = st.selectbox(
        "📢 Target Platform",
        ["Facebook Ads", "Instagram", "X (Twitter)", "Landing Page", "Email Marketing"]
    )
    tone = st.selectbox(
        "🎭 Tone",
        ["Emotional", "Luxury", "Aggressive", "Inspirational", "Minimal"]
    )

with col2:
    product = st.text_input("💎 Product Name", "The Spiritual Freedom Code")
    affiliate_link = st.text_input("🔗 Affiliate Link", "https://go.hotmart.com/L103130074K")
    pain_point = st.text_area("💔 Customer Pain Point", "Feeling trapped, lost, and disconnected from purpose")

benefits = st.text_area(
    "🌟 Main Benefits (comma separated)",
    "Financial freedom, Inner peace, Mental clarity, High vibration"
)

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.button("🔥 Generate Ad Copy & Image Prompt"):

    with st.spinner("🧠 AI is crafting your high-converting ad copy..."):

        # -----------------------------
        # AD COPY PROMPT
        # -----------------------------
        prompt_copy = f"""
You are a senior digital marketing expert.

Create a HIGH-CONVERTING ad copy with the following structure:

1. BIG BOLD HEADLINE
2. Emotional hook (2–3 lines)
3. Pain agitation
4. Bullet list of benefits
5. Strong CTA

Target Platform: {platform}
Niche: {niche}
Tone: {tone}
Product: {product}
Customer Pain Point: {pain_point}
Main Benefits: {benefits}
Affiliate Link: {affiliate_link}
"""

        # -----------------------------
        # IMAGE PROMPT PROMPT
        # -----------------------------
        prompt_image = f"""
Create a visually stunning, psychological, eye-catching image for AI generation.
Niche: {niche}, Product: {product}, Style: High conversion ad, inspirational.
"""

        # -----------------------------
        # Retry mechanism
        # -----------------------------
        ad_copy = ""
        image_prompt = ""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                completion_copy = client.chat.completions.create(
                    model="llama3-8b-instant",
                    messages=[{"role": "user", "content": prompt_copy}],
                    temperature=0.8,
                    max_tokens=500
                )
                ad_copy = completion_copy.choices[0].message.content

                completion_image = client.chat.completions.create(
                    model="llama3-8b-instant",
                    messages=[{"role": "user", "content": prompt_image}],
                    temperature=0.7,
                    max_tokens=200
                )
                image_prompt = completion_image.choices[0].message.content
                break

            except GroqError:
                st.warning(f"Attempt {attempt+1} failed. Retrying...")
                time.sleep(2)
        else:
            st.error("❌ Failed to get a response from Groq API. Check API key or network.")
            st.stop()

        # -----------------------------
        # SAVE TO HISTORY
        # -----------------------------
        st.session_state.history.append({
            "product": product,
            "ad_copy": ad_copy,
            "image_prompt": image_prompt
        })

    # -----------------------------
    # DISPLAY AD COPY
    # -----------------------------
    st.markdown("---")
    st.markdown("## 🚀 Generated Ad Copy")
    st.markdown(
        f"""
<div style="background:#0f172a;padding:25px;border-radius:12px;color:#e5e7eb;font-size:17px;">
<pre style="white-space:pre-wrap;">{ad_copy}</pre>
</div>
""",
        unsafe_allow_html=True
    )

    # -----------------------------
    # DISPLAY IMAGE PROMPT
    # -----------------------------
    st.markdown("## 🎨 AI Image Prompt")
    st.info(image_prompt)

    # -----------------------------
    # COPY & SHARE
    # -----------------------------
    st.code(ad_copy, language="markdown")
    encoded_text = urllib.parse.quote(ad_copy)
    fb_url = f"https://www.facebook.com/sharer/sharer.php?u={affiliate_link}&quote={encoded_text}"
    x_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={affiliate_link}"

    st.markdown("### 🔗 Share this Ad Copy")
    st.markdown(f"""
<a href="{fb_url}" target="_blank">📘 Facebook</a> | 
<a href="{x_url}" target="_blank">🐦 X (Twitter)</a> | 
<a href="{li_url}" target="_blank">💼 LinkedIn</a>
""", unsafe_allow_html=True)

# -----------------------------
# HISTORY DISPLAY
# -----------------------------
if st.session_state.history:
    st.markdown("---")
    st.markdown("## ⏱️ History")
    for idx, item in enumerate(reversed(st.session_state.history)):
        st.markdown(f"### {item['product']}")
        st.code(item['ad_copy'], language="markdown")
        st.info(item['image_prompt'])

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Built with ❤️ by Marketing Beast AI | Groq + Streamlit")
