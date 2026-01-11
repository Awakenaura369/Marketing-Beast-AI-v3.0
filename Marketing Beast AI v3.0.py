import streamlit as st
from groq import Groq
import os
import urllib.parse
from fpdf import FPDF

# -----------------------------
# 📄 PDF CLASS (FIXED & PRO)
# -----------------------------
class BeastPDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "MARKETING BEAST AI - STRATEGY REPORT", align="C", ln=True)
        self.ln(10)

def create_pdf(ad_copy, image_prompt, product_name, platform):
    pdf = BeastPDF()
    pdf.add_page()
    
    # تنظيف النص من الرموز التي تسبب مشاكل في الترميز
    safe_copy = ad_copy.encode('latin-1', 'replace').decode('latin-1')
    safe_prompt = image_prompt.encode('latin-1', 'replace').decode('latin-1')

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, f"Product: {product_name}", ln=True)
    pdf.cell(0, 10, f"Target Platform: {platform}", ln=True)
    pdf.ln(5)

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
# ⚙️ API SETUP & CONFIG
# -----------------------------
st.set_page_config(page_title="Marketing Beast AI", page_icon="🦁", layout="wide")

# قراءة المفتاح من Secrets
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing in Streamlit Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# 🏰 UI DESIGN
# -----------------------------
st.title("🦁 Marketing Beast AI v4.0 PRO")
st.markdown("### Powering Your Fiverr Success with Groq Speed")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("🎯 Campaign Settings")
    niche = st.text_input("Niche", "Digital Marketing")
    product = st.text_input("Product Name", "The Growth Secret")
    platform = st.selectbox("Platform", ["Facebook Ads", "Instagram Ads", "TikTok Ads", "Email Marketing"])
    tone = st.select_slider("Tone", options=["Minimal", "Emotional", "Luxury", "Inspirational", "Aggressive"])

with col2:
    st.subheader("💡 Product Details")
    pain_point = st.text_area("Customer Pain Point")
    benefits = st.text_area("Key Benefits (comma separated)")
    link = st.text_input("CTA Link")

# -----------------------------
# 🔥 MAIN LOGIC
# -----------------------------
if st.button("🔥 GENERATE BEAST STRATEGY"):
    with st.spinner("🧠 Groq AI is thinking..."):
        try:
            model = "llama-3.3-70b-versatile"
            
            # 1. Generate Content
            ad_res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Write high-converting {platform} ad copy for {product}. Tone: {tone}. Pain: {pain_point}. Benefits: {benefits}. CTA: {link}"}]
            )
            ad_text = ad_res.choices[0].message.content

            img_res = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Create a detailed AI image prompt for {product} on {platform}. Style: {tone}"}]
            )
            img_prompt = img_res.choices[0].message.content

            # 2. Display Results
            st.divider()
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🚀 Professional Ad Copy")
                st.write(ad_text)
                
            with c2:
                st.subheader("🎨 AI Image Prompt")
                st.write(img_prompt)
                
                # Download PDF Button
                pdf_bytes = create_pdf(ad_text, img_prompt, product, platform)
                st.download_button(
                    label="📥 Download Strategy PDF",
                    data=bytes(pdf_bytes),
                    file_name=f"Beast_Report_{product}.pdf",
                    mime="application/pdf"
                )

            # 3. Share & Utility Buttons
            st.divider()
            st.subheader("🔗 Quick Share & Tools")
            share_col1, share_col2, share_col3 = st.columns(3)

            with share_col1:
                wa_text = f"Check this AI Strategy for {product}: {ad_text[:100]}..."
                wa_link = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:10px; cursor:pointer;">Share on WhatsApp</button></a>', unsafe_allow_html=True)

            with share_col2:
                li_link = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote('https://zna3s.streamlit.app')}"
                st.markdown(f'<a href="{li_link}" target="_blank"><button style="width:100%; border-radius:10px; background-color:#0077B5; color:white; border:none; padding:10px; cursor:pointer;">Share on LinkedIn</button></a>', unsafe_allow_html=True)

            with share_col3:
                if st.button("📋 Show Copyable Text"):
                    st.text_area("Select and Copy:", value=ad_text, height=200)
                    st.success("Text is ready to be copied to your clipboard!")

        except Exception as e:
            st.error(f"Error: {e}")

st.sidebar.info("🦁 **Marketing Beast AI** is optimized for Fiverr Sellers. Use the PDF report to impress your clients!")
