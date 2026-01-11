import streamlit as st
from groq import Groq
import os
import urllib.parse
from fpdf import FPDF2
import re

# -----------------------------
# 📄 PDF & UTILS
# -----------------------------
class BeastPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "MARKETING BEAST AI - STRATEGY REPORT", align="C", ln=True)
        self.ln(10)

def clean_text_for_pdf(text):
    """ تنظيف النص من أي رموز تعبيرية أو أحرف غير مدعومة في PDF العادي """
    # تعويض الرموز التعبيرية بـ [emoji] أو مسحها لتجنب الـ Error
    return text.encode('ascii', 'ignore').decode('ascii')

def create_pdf(ad_copy, image_prompt, product_name, platform):
    pdf = BeastPDF()
    pdf.add_page()
    
    # تنظيف النصوص
    safe_copy = clean_text_for_pdf(ad_copy)
    safe_prompt = clean_text_for_pdf(image_prompt)

    # معلومات الحملة
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, f"Product: {product_name}", ln=True)
    pdf.cell(0, 10, f"Target Platform: {platform}", ln=True)
    pdf.ln(5)

    # قسم الإعلان
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "Generated Ad Copy:", ln=True)
    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(0, 8, safe_copy)
    pdf.ln(10)

    # قسم وصف الصورة
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, "AI Image Prompt:", ln=True)
    pdf.set_font("helvetica", "I", 11)
    pdf.multi_cell(0, 8, safe_prompt)

    return pdf.output()

# -----------------------------
# ⚙️ APP CONFIG
# -----------------------------
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ API Key Missing in Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# 🏰 UI INTERFACE
# -----------------------------
st.title("🦁 Marketing Beast AI v4.0 PRO")
st.markdown("### Advanced AI Ad Generator for Fiverr Professionals")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    niche = st.text_input("🎯 Niche", placeholder="e.g., Sustainable Fashion")
    product = st.text_input("💎 Product Name", placeholder="e.g., Bamboo Hoodie")
    platform = st.selectbox("📢 Platform", ["Facebook Ads", "Instagram Ads", "TikTok Ads", "Email Marketing"])
    tone = st.select_slider("🎭 Tone", options=["Minimal", "Emotional", "Luxury", "Inspirational", "Aggressive"])

with col2:
    pain_point = st.text_area("💔 Customer Pain Point", placeholder="What keeps them awake at night?")
    benefits = st.text_area("🌟 Main Benefits", placeholder="Bullet points of why this is great")
    link = st.text_input("🔗 CTA Link (Optional)")

# -----------------------------
# 🔥 PROCESS & GENERATE
# -----------------------------
if st.button("🔥 GENERATE PROFESSIONAL STRATEGY"):
    if not pain_point or not product:
        st.warning("Please fill in the Product Name and Pain Point!")
    else:
        with st.spinner("🧠 Beast AI is crafting your content..."):
            try:
                model_id = "llama-3.3-70b-versatile"
                
                # توليد المحتوى
                ad_content = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": f"High-converting {platform} ad for {product}. Tone: {tone}. Pain: {pain_point}. Benefits: {benefits}. CTA: {link}"}]
                ).choices[0].message.content

                img_content = client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": f"Detailed AI image prompt for {product} on {platform}. Style: {tone}"}]
                ).choices[0].message.content

                # العرض
                st.divider()
                res_c1, res_c2 = st.columns(2)
                
                with res_c1:
                    st.success("🚀 Ad Copy")
                    st.write(ad_content)
                
                with res_c2:
                    st.info("🎨 Image Strategy")
                    st.write(img_content)
                    
                    # زر التحميل
                    pdf_data = create_pdf(ad_content, img_content, product, platform)
                    st.download_button(
                        label="📥 Download Delivery PDF",
                        data=bytes(pdf_data),
                        file_name=f"Beast_Strategy_{product}.pdf",
                        mime="application/pdf"
                    )

                # قسم المشاركة والنسخ
                st.divider()
                st.subheader("🔗 Share & Copy Tools")
                s_col1, s_col2, s_col3 = st.columns(3)

                with s_col1:
                    wa_url = f"https://wa.me/?text={urllib.parse.quote('Check this Ad Strategy: ' + ad_content[:200])}"
                    st.markdown(f'<a href="{wa_url}" target="_blank"><div style="text-align:center; background-color:#25D366; color:white; padding:10px; border-radius:10px; cursor:pointer;">Share via WhatsApp</div></a>', unsafe_allow_html=True)

                with s_col2:
                    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote('https://zna3s.streamlit.app')}"
                    st.markdown(f'<a href="{li_url}" target="_blank"><div style="text-align:center; background-color:#0077B5; color:white; padding:10px; border-radius:10px; cursor:pointer;">Share on LinkedIn</div></a>', unsafe_allow_html=True)

                with s_col3:
                    if st.button("📋 Copy Text to Clipboard"):
                        st.text_area("Copy from here:", value=ad_content, height=150)
                        st.info("Select the text above and press Ctrl+C")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.sidebar.markdown("---")
st.sidebar.write("🦁 **Marketing Beast v4.0 PRO**")
st.sidebar.caption("Optimized for High-Speed Groq AI")
