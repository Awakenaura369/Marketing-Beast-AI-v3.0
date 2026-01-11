# ==============================
# 🦁 Marketing Beast AI v4.0 PRO (Fixed & Final)
# Specialized for Fiverr Professionals
# ==============================

import streamlit as st
from groq import Groq
import os
import urllib.parse
import time
from fpdf import FPDF

# -----------------------------
# 📄 PDF GENERATION (FIXED FOR EMOJIS)
# -----------------------------
def create_pdf(ad_copy, image_prompt, product_name, platform):
    pdf = FPDF()
    pdf.add_page()
    
    # تحويل النص لـ Latin-1 وتعويض الرموز اللي مكتقراش باش ميتوقعش Error
    # هاد العملية ضرورية باش الـ PDF يقبل يخرج وخا فيه Emojis
    safe_ad_copy = ad_copy.encode('latin-1', 'replace').decode('latin-1')
    safe_image_prompt = image_prompt.encode('latin-1', 'replace').decode('latin-1')

    # Header
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 10, txt="MARKETING BEAST AI - AD STRATEGY", ln=True, align='C')
    pdf.ln(10)
    
    # Info
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 10, txt=f"Product: {product_name}", ln=True)
    pdf.cell(0, 10, txt=f"Platform: {platform}", ln=True)
    pdf.ln(5)
    
    # Content
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, txt="🚀 Generated Ad Copy:", ln=True)
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 8, txt=safe_ad_copy)
    pdf.ln(10)
    
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, txt="🎨 AI Visual Strategy:", ln=True)
    pdf.set_font("helvetica", 'I', 11)
    pdf.multi_cell(0, 8, txt=safe_image_prompt)
    
    return pdf.output()

# -----------------------------
# ⚙️ CONFIG & API SETUP
# -----------------------------
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# قراءة المفتاح من السيكريتس ديال ستريمليت
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# 🏰 UI DESIGN
# -----------------------------
st.title("🦁 Marketing Beast AI v4.0 PRO")
st.markdown("### Powering Your Fiverr Success with AI")
st.divider()

col1, col2 = st.columns(2, gap="medium")

with col1:
    niche = st.text_input("🎯 Niche", "Digital Marketing")
    product = st.text_input("💎 Product Name", "My Awesome Service")
    platform = st.selectbox("📢 Platform", ["Facebook Ads", "Instagram Ads", "TikTok Ads", "Email"])
    tone = st.select_slider("🎭 Tone", options=["Minimal", "Emotional", "Luxury", "Aggressive"])

with col2:
    pain_point = st.text_area("💔 Customer Pain Point")
    benefits = st.text_area("🌟 Main Benefits (comma separated)")
    link = st.text_input("🔗 Link")

# -----------------------------
# 🔥 GENERATION LOGIC
# -----------------------------
if st.button("🔥 Generate Full Strategy"):
    with st.spinner("🧠 Analyzing and Writing..."):
        try:
            # الموديل 70B هو الأقوى والأفضل للـ Copywriting
            model_id = "llama-3.3-70b-versatile"
            
            # 1. Generate Copy
            res_copy = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": f"Write a high-converting {platform} ad copy for {product}. Tone: {tone}. Pain: {pain_point}. Benefits: {benefits}. CTA: {link}"}],
                temperature=0.7
            )
            ad_text = res_copy.choices[0].message.content

            # 2. Generate Image Prompt
            res_img = client.chat.completions.create(
                model=model_id,
                messages=[{"role": "user", "content": f"Create a professional AI image prompt for {product} on {platform}. Style: {tone}"}],
                temperature=0.6
            )
            img_prompt = res_img.choices[0].message.content

            # Display
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🚀 Ad Copy")
                st.write(ad_text)
            with c2:
                st.subheader("🎨 Image Prompt")
                st.write(img_prompt)
                
                # PDF Download
                pdf_bytes = create_pdf(ad_text, img_prompt, product, platform)
                st.download_button(
                    label="📥 Download Professional PDF",
                    data=pdf_bytes,
                    file_name=f"Beast_Strategy_{product}.pdf",
                    mime="application/pdf"
                )
            
            st.session_state.history.append({"p": product, "c": ad_text})

        except Exception as e:
            st.error(f"Error occurred: {e}")

# -----------------------------
# ⏱️ HISTORY
# -----------------------------
if st.session_state.history:
    with st.expander("View History"):
        for h in reversed(st.session_state.history):
            st.write(f"**{h['p']}**")
