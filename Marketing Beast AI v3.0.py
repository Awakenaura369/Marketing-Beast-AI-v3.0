import streamlit as st
from groq import Groq
import os
import requests
from bs4 import BeautifulSoup
import json

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Marketing Beast AI v3.3",
    page_icon="⚡",
    layout="wide"
)

# ================== STYLES ==================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #f8fafc;
}
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stSelectbox>div>div>div {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    font-weight: bold;
    width: 100%;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(37,99,235,0.4);
}
[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #334155;
}
.content-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #3b82f6;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================== HELPERS ==================
def get_config(key):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key)

# ================== DATA ==================
NICHES = {
    "Spirituality & Awareness": "manifestation, vibration, inner peace",
    "Make Money Online / Affiliate": "income, urgency, financial freedom",
    "Health & Fitness": "energy, body transformation, confidence",
    "Relationships & Dating": "attraction, psychology, emotions",
    "Tech & AI Tools": "automation, productivity, future"
}

STYLES = ["Aggressive", "Spiritual", "Storytelling", "Direct"]
PLATFORMS = ["Facebook Ad", "Instagram Post", "TikTok Script", "Email Blast"]
EMOTIONS = ["Power", "Peace", "Mystery", "Urgency"]

HISTORY_FILE = "marketing_history.json"

# ================== AI GENERATOR ==================
def generate_all(niche, style, platform, product, benefits, pain, link, emotion):
    api_key = get_config("GROQ_API_KEY")
    if not api_key:
        return "⚠️ GROQ_API_KEY not found."

    client = Groq(api_key=api_key)

    prompt = f"""
You are a world-class copywriter.

Create:
- 3 high-converting {platform} ads
- Each ad has an A/B variation
- Style: {style}
- Niche: {niche}
- Emotion focus: {emotion}

Product: {product}
Customer pain: {pain}
Main benefits: {benefits}
Link: {link}

Format EXACTLY like this:

---COPY---
Post 1
Post 1B
Post 2
Post 2B
Post 3
Post 3B

---CTA---
CTA 1
CTA 2
CTA 3

---IMAGE---
One detailed AI image prompt
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content

# ================== SIDEBAR ==================
with st.sidebar:
    st.header("🎯 Strategy Center")
    niche = st.selectbox("Select Niche", list(NICHES.keys()))
    style = st.selectbox("Copy Style", STYLES)
    platform = st.selectbox("Target Platform", PLATFORMS)
    emotion = st.selectbox("Image Emotion", EMOTIONS)

# ================== INPUTS ==================
col1, col2 = st.columns(2)
with col1:
    product = st.text_input("💎 Product Name")
with col2:
    link = st.text_input("🔗 Affiliate Link")

pain = st.text_input("💔 Customer Pain Point")
benefits = st.text_area("🌟 Main Benefits", height=100)

# ================== ACTION ==================
if st.button("🚀 UNLEASH THE BEAST"):
    if product and link and benefits:
        with st.spinner("Generating marketing magic..."):
            result = generate_all(
                niche, style, platform,
                product, benefits, pain, link, emotion
            )

            if result.startswith("⚠️"):
                st.error(result)
            else:
                parts = result.split("---IMAGE---")
                text_part = parts[0]
                image_part = parts[1] if len(parts) > 1 else ""

                copy = text_part.split("---CTA---")[0].replace("---COPY---", "")
                cta = text_part.split("---CTA---")[1] if "---CTA---" in text_part else ""

                # Save history
                try:
                    history = json.load(open(HISTORY_FILE))
                except:
                    history = []

                history.append({
                    "product": product,
                    "copy": copy,
                    "cta": cta,
                    "image": image_part
                })

                json.dump(history, open(HISTORY_FILE, "w"), indent=2)

                st.markdown('<div class="content-box">', unsafe_allow_html=True)
                st.markdown("### 🔥 Sales Copy (A/B Testing)")
                st.markdown(copy)

                st.markdown("### 🎯 CTA Variations")
                st.info(cta)

                st.markdown("### 🎨 AI Image Prompt")
                st.info(image_part)

                st.download_button(
                    "💾 Download TXT",
                    data=f"{copy}\n\n{cta}\n\n{image_part}",
                    file_name=f"{product}_marketing.txt"
                )
                st.markdown('</div>', unsafe_allow_html=True)

                st.balloons()
    else:
        st.error("⚠️ عَمّر جميع الخانات")

# ================== HISTORY ==================
st.markdown("## 🕘 History")
try:
    history = json.load(open(HISTORY_FILE))[-10:]
    for i, item in enumerate(reversed(history), 1):
        with st.expander(f"{i}. {item['product']}"):
            st.markdown(item["copy"])
            st.info(item["cta"])
            st.info(item["image"])
except:
    st.info("No history yet.")
