import streamlit as st
from groq import Groq
import os
import urllib.parse
from fpdf import FPDF

# -----------------------------
# 📄 PDF CLASS WITH UNICODE SUPPORT
# -----------------------------
class BeastPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "MARKETING BEAST AI - STRATEGY REPORT", align="C", ln=True)
        self.ln(10)

def create_pdf(ad_copy, image_prompt, product_name, platform):
    pdf = BeastPDF()
    pdf.add_page()
    
    # تنظيف النص من الرموز اللي كتدير مشكل في الترميز القديم
    # هاد السطر كيعوض الرموز غير المدعومة بـ '?' باش مكيوقعش Error
    safe_copy = ad_copy.encode('latin-1', 'replace').decode('latin-1')
    safe_prompt = image_prompt.encode('latin-1', 'replace').decode('latin-1')

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, f"Product: {product_name}", ln=True)
    pdf.cell(0, 10, f"Target Platform: {platform}", ln=True)
    pdf.ln(5)

    pdf.set_font("helvetica", "B(14)")
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "🚀 Generated Ad Copy:", ln=True)
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 8, safe_copy)
    pdf.ln(10)

    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "🎨 AI Image Prompt:", ln=True)
    pdf.set_font("helvetica", "I", 11)
    pdf.multi_cell(0, 8, safe_prompt)

    return pdf.output()

# -----------------------------
# ⚙️ API SETUP
# -----------------------------
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# قراءة المفتاح من السيكريتس
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing in Streamlit Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# 🏰 UI DESIGN
# -----------------------------
st.title("🦁 Marketing Beast AI v4.0 PRO")
st.markdown("### Elevate your Fiverr Business with Professional AI Strategies")
st.divider()

col1, col2 = st.columns(2)

with col1:
    niche = st.text_input("🎯 Niche", "Eco-friendly Lifestyle")
    product = st.text_input("💎 Product Name", "The Earth-First Bamboo Hoodie")
    platform = st.selectbox("📢 Platform", ["Facebook Ads", "Instagram Ads", "TikTok Ads", "Email"])
    tone = st.select_slider("🎭 Tone", options=["Minimal", "Emotional", "Luxury", "Inspirational", "Aggressive"])

with col2:
    pain_point = st.text_area("💔 Customer Pain Point", "Feeling guilty about fast fashion impact")
    benefits = st.text_area("🌟 Main Benefits", "100% Organic Bamboo, Soft, Carbon-neutral")
    link = st.text_input("🔗 CTA Link", "https://earthfirst.store")

# -----------------------------
# 🔥 LOGIC
# -----------------------------
if st.button("🔥 Generate Full Strategy"):
    with st.spinner("🧠 Analyzing niche and crafting copy..."):
        try:
            # استعمال أقوى موديل متاح
            model = "llama-3.3-70b-versatile"
            
            # 1. التوليد
            ad_res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Write high-converting {platform} copy for {product}. Tone: {tone}. Pain: {pain_point}. Benefits: {benefits}. CTA: {link}"}]
            )
            ad_text = ad_res.choices[0].message.content

            img_res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Detailed AI image generation prompt for {product} on {platform}. Tone: {tone}"}]
            )
            img_prompt = img_res.choices[0].message.content

            # 2. العرض
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🚀 Ad Copy")
                st.write(ad_text)
            with c2:
                st.subheader("🎨 Image Prompt")
                st.write(img_prompt)
                
                # زر التحميل المصلح
                pdf_output = create_pdf(ad_text, img_prompt, product, platform)
                st.download_button(
                    label="📥 Download Professional PDF",
                    data=bytes(pdf_output),
                    file_name=f"Strategy_{product}.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Error: {e}")
