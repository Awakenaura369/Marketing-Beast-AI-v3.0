# ==============================
# Marketing Beast AI v4.0 PRO (FIXED)
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
# LOAD API KEY FROM SECRETS (FIXED)
# -----------------------------
# هاد السطر هو اللي كان خاصو يتبدل باش يقرا من الخانة اللي عمرتي
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in Secrets. Please check your Streamlit dashboard.")
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

        prompt_copy = f"""
You are a senior digital marketing expert. Create a HIGH-CONVERTING ad copy for {platform}.
Niche: {niche}
Product: {product}
Tone: {tone}
Pain Point: {pain_point}
Benefits: {benefits}
Link: {affiliate_link}
"""

        prompt_image = f"""
Create a professional AI image generation prompt for: {product}. 
The style should be {tone} and visually stunning for {platform}.
"""

        ad_copy = ""
        image_prompt = ""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # استعملنا موديل أحدث وأكثر استقراراً
                completion_copy = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_copy}],
                    temperature=0.8
                )
                ad_copy = completion_copy.choices[0].message.content

                completion_image = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt_image}],
                    temperature=0.7
                )
                image_prompt = completion_image.choices[0].message.content
                break

            except Exception as e:
                if attempt < max_retries - 1:
                    st.warning(f"Attempt {attempt+1} failed. Retrying...")
                    time.sleep(2)
                else:
                    st.error(f"❌ Error: {str(e)}")
                    st.stop()

        # SAVE TO HISTORY
        st.session_state.history.append({
            "product": product,
            "ad_copy": ad_copy,
            "image_prompt": image_prompt
        })

    # DISPLAY RESULTS
    st.markdown("---")
    st.markdown("## 🚀 Generated Ad Copy")
    st.info(ad_copy)

    st.markdown("## 🎨 AI Image Prompt")
    st.success(image_prompt)

    # SHARING LINKS
    encoded_text = urllib.parse.quote(ad_copy)
    st.markdown(f"### 🔗 [Share on Facebook](https://www.facebook.com/sharer/sharer.php?u={affiliate_link}&quote={encoded_text})")

# -----------------------------
# HISTORY
# -----------------------------
if st.session_state.history:
    st.markdown("---")
    st.markdown("## ⏱️ History")
    for item in reversed(st.session_state.history):
        with st.expander(f"Product: {item['product']}"):
            st.write(item['ad_copy'])
            st.caption(f"Image Prompt: {item['image_prompt']}")
