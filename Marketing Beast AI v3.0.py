# ==============================
# Marketing Beast AI v3.0 (PRO)
# Streamlit + Groq AI
# ==============================

import streamlit as st
from groq import Groq
import os
import urllib.parse

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Marketing Beast AI v3.0",
    page_icon="🔥",
    layout="wide"
)

# -----------------------------
# LOAD GROQ API KEY
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please add it to environment variables.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# UI HEADER
# -----------------------------
st.markdown("""
# ⚡ Marketing Beast AI v3.0
### AI-Powered Content & Visual Strategy
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
if st.button("🔥 Generate Pro Ad Copy"):

    with st.spinner("🧠 AI is crafting a high-converting ad copy..."):

        prompt = f"""
You are a senior digital marketing expert.

Create a HIGH-CONVERTING ad copy with the following structure:

1. BIG BOLD HEADLINE (short & powerful)
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

Make it persuasive, emotional and conversion-focused.
"""

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=700
        )

        ad_copy = completion.choices[0].message.content

    # -----------------------------
    # OUTPUT
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
    # COPY BUTTON
    # -----------------------------
    st.code(ad_copy, language="markdown")

    # -----------------------------
    # SHARE BUTTONS
    # -----------------------------
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
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("Built with ❤️ by Marketing Beast AI | Groq + Streamlit")
