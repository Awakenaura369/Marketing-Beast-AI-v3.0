import streamlit as st
from groq import Groq
import urllib.parse
from fpdf import FPDF
import re
import json

# -----------------------------
# 🎨 PAGE CONFIG & CUSTOM CSS
# -----------------------------
st.set_page_config(
    page_title="Marketing Beast AI",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --beast-red: #FF2D20;
    --beast-orange: #FF6B00;
    --beast-dark: #0A0A0A;
    --beast-card: #111111;
    --beast-border: #222222;
    --beast-text: #F0F0F0;
    --beast-muted: #888888;
}

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--beast-dark) !important;
    color: var(--beast-text) !important;
}

.stApp { background-color: var(--beast-dark) !important; }

/* HIDE STREAMLIT DEFAULTS */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1400px !important; }

/* HERO HEADER */
.beast-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    background: linear-gradient(135deg, #0A0A0A 0%, #1a0505 50%, #0A0A0A 100%);
    border-bottom: 1px solid var(--beast-border);
    margin-bottom: 2rem;
}
.beast-logo {
    font-family: 'Bebas Neue', cursive;
    font-size: clamp(3rem, 8vw, 6rem);
    letter-spacing: 0.05em;
    background: linear-gradient(90deg, #FF2D20, #FF6B00, #FF2D20);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    margin: 0;
    line-height: 1;
}
@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.beast-tagline {
    color: var(--beast-muted);
    font-size: 0.9rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.version-badge {
    display: inline-block;
    background: linear-gradient(90deg, #FF2D20, #FF6B00);
    color: white;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    padding: 3px 12px;
    border-radius: 20px;
    margin-top: 0.8rem;
    text-transform: uppercase;
}

/* CARDS */
.section-card {
    background: var(--beast-card);
    border: 1px solid var(--beast-border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.3rem;
    letter-spacing: 0.1em;
    color: var(--beast-orange);
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--beast-border);
    padding-bottom: 0.5rem;
}

/* INPUTS */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #1A1A1A !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    color: var(--beast-text) !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--beast-orange) !important;
    box-shadow: 0 0 0 2px rgba(255,107,0,0.2) !important;
}

/* LABELS */
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    color: #CCCCCC !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
}

/* GENERATE BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #FF2D20, #FF6B00) !important;
    color: white !important;
    font-family: 'Bebas Neue', cursive !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.15em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(255,45,32,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255,45,32,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    background: linear-gradient(90deg, #1a6b3a, #25a55a) !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 0.7rem 1rem !important;
    transition: all 0.3s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37,165,90,0.4) !important;
}

/* RESULT BOXES */
.result-box {
    background: #0D1117;
    border: 1px solid var(--beast-border);
    border-left: 3px solid var(--beast-orange);
    border-radius: 8px;
    padding: 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.9rem;
    line-height: 1.7;
    white-space: pre-wrap;
}
.result-label {
    font-family: 'Bebas Neue', cursive;
    font-size: 1rem;
    letter-spacing: 0.1em;
    color: var(--beast-orange);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* METRICS / KPI CARDS */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}
.kpi-card {
    background: #111;
    border: 1px solid #222;
    border-top: 2px solid var(--beast-orange);
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.8rem;
    color: var(--beast-orange);
    line-height: 1;
}
.kpi-label {
    font-size: 0.7rem;
    color: var(--beast-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* SHARE BUTTONS */
.share-btn {
    display: block;
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    color: white !important;
    font-weight: 600;
    font-size: 0.85rem;
    text-decoration: none;
    transition: all 0.3s;
}
.share-btn:hover { transform: translateY(-2px); opacity: 0.9; }
.wa-btn { background: #25D366; }
.li-btn { background: #0077B5; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #111 !important;
    border-radius: 8px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--beast-muted) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #FF2D20, #FF6B00) !important;
    color: white !important;
}

/* SPINNER */
.stSpinner > div { border-top-color: var(--beast-orange) !important; }

/* DIVIDER */
hr { border-color: var(--beast-border) !important; opacity: 0.5 !important; }

/* SUCCESS / INFO / WARNING */
.stSuccess, .stInfo, .stWarning {
    border-radius: 8px !important;
    border: 1px solid !important;
}

/* TONE SLIDER */
.stSlider [data-testid="stTickBar"] { color: var(--beast-muted) !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 📄 PDF CLASS (IMPROVED)
# -----------------------------
class BeastPDF(FPDF):
    def __init__(self, product, platform):
        super().__init__()
        self.product = product
        self.platform = platform

    def header(self):
        # Header bar
        self.set_fill_color(15, 15, 15)
        self.rect(0, 0, 210, 25, 'F')
        self.set_font("helvetica", "B", 14)
        self.set_text_color(255, 107, 0)
        self.set_xy(0, 7)
        self.cell(0, 10, "MARKETING BEAST AI  |  STRATEGY REPORT", align="C")
        self.set_text_color(200, 200, 200)
        self.ln(18)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, self.clean(f"Beast AI v5.0  |  {self.product}  |  {self.platform}  |  Page {self.page_no()}"), align="C")

    def clean(self, text):
        replacements = {
            '\u2014': '-', '\u2013': '-', '\u2018': "'", '\u2019': "'",
            '\u201c': '"', '\u201d': '"', '\u2022': '*', '\u2026': '...',
            '\u00b7': '*', '\u2010': '-', '\u2011': '-', '\u2012': '-',
            '\u2015': '-', '\u00e9': 'e', '\u00e8': 'e', '\u00ea': 'e',
            '\u00e0': 'a', '\u00e2': 'a', '\u00f4': 'o', '\u00fb': 'u',
            '\u00fc': 'u', '\u00e7': 'c', '\u2039': '<', '\u203a': '>',
            '\u00ab': '<<', '\u00bb': '>>', '\u00a9': '(c)', '\u00ae': '(R)',
            '\u2122': '(TM)', '\u20ac': 'EUR', '\u00a3': 'GBP',
            '\u00b0': ' deg', '\u00bd': '1/2', '\u00bc': '1/4', '\u00be': '3/4',
        }
        for char, rep in replacements.items():
            text = text.replace(char, rep)
        return text.encode('latin-1', 'replace').decode('latin-1')

    def section_title(self, title):
        self.set_font("helvetica", "B", 13)
        self.set_text_color(255, 107, 0)
        self.set_fill_color(20, 20, 20)
        self.cell(0, 10, self.clean(f"  {title}"), ln=True, fill=True)
        self.set_text_color(220, 220, 220)
        self.ln(3)

    def body_text(self, text):
        self.set_font("helvetica", size=10)
        self.set_text_color(220, 220, 220)
        self.multi_cell(0, 6, self.clean(text))
        self.ln(5)

    def info_row(self, label, value):
        self.set_font("helvetica", "B", 10)
        self.set_text_color(255, 107, 0)
        self.cell(45, 8, self.clean(label + ":"), ln=False)
        self.set_font("helvetica", size=10)
        self.set_text_color(220, 220, 220)
        self.cell(0, 8, self.clean(value), ln=True)

    def kpi_box(self, label, value):
        self.set_font("helvetica", "B", 9)
        self.set_text_color(150, 150, 150)
        self.cell(45, 6, self.clean(label.upper()), ln=False)
        self.set_font("helvetica", "B", 10)
        self.set_text_color(255, 107, 0)
        self.cell(0, 6, self.clean(value), ln=True)





def create_pdf(ad_copy, image_prompt, product, platform, tone, strategy_data=None):
    pdf = BeastPDF(product, platform)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Campaign Info
    pdf.section_title("CAMPAIGN OVERVIEW")
    pdf.info_row("Product", product)
    pdf.info_row("Platform", platform)
    pdf.info_row("Tone", tone)
    pdf.ln(5)

    # KPIs
    pdf.section_title("TARGET KPIs")
    kpis = [
        ("Target CTR", "> 2.5%"),
        ("Est. ROAS", "3x - 5x"),
        ("Recommended Budget", "$20 - $50/day"),
        ("A/B Test Variants", "3 variations"),
        ("Audience Size", "1M - 5M"),
        ("Frequency Cap", "3x per week"),
    ]
    for label, val in kpis:
        pdf.kpi_box(label, val)
    pdf.ln(5)

    # Ad Copy
    pdf.section_title("GENERATED AD COPY - 3 VARIATIONS")
    pdf.body_text(ad_copy)

    # Strategy (if available)
    if strategy_data:
        pdf.add_page()
        pdf.section_title("FULL STRATEGY")
        pdf.body_text(strategy_data)

    # Image Prompt
    pdf.add_page()
    pdf.section_title("AI IMAGE GENERATION PROMPT")
    pdf.set_font("helvetica", "I", 10)
    pdf.set_text_color(180, 220, 180)
    pdf.multi_cell(0, 6, pdf.clean(image_prompt))

    # Facebook Specs
    pdf.ln(8)
    pdf.section_title("PLATFORM SPECIFICATIONS")
    specs = {
        "Facebook Ads": [("Image Size", "1080 x 1080 or 1200 x 628"), ("Video Length", "15-30 sec"), ("Headline", "Max 40 chars"), ("Body Text", "Max 125 chars"), ("CTA", "Learn More / Shop Now")],
        "Instagram Ads": [("Image Size", "1080 x 1350 (4:5)"), ("Video Length", "Up to 60 sec"), ("Caption", "Max 2200 chars"), ("Hashtags", "5-10 recommended")],
        "TikTok Ads": [("Video Size", "9:16 vertical"), ("Length", "9-15 sec optimal"), ("Text Overlay", "Max 100 chars"), ("Sound", "Required for best performance")],
        "Email Marketing": [("Subject Line", "Max 50 chars"), ("Preview Text", "Max 100 chars"), ("Width", "600px recommended"), ("CTA Button", "Above the fold")],
    }
    platform_specs = specs.get(platform, specs["Facebook Ads"])
    for label, val in platform_specs:
        pdf.kpi_box(label, val)

    return pdf.output()


# -----------------------------
# ⚙️ API SETUP
# -----------------------------
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ API Key Missing in Secrets!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)
MODEL = "llama-3.3-70b-versatile"

# -----------------------------
# 🏰 HERO HEADER
# -----------------------------
st.markdown("""
<div class="beast-header">
    <div class="beast-logo">MARKETING BEAST AI</div>
    <div class="beast-tagline">Professional Ad Strategy Generator</div>
    <div class="version-badge">v5.0 PRO — Fiverr Edition</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 📋 INPUT FORM
# -----------------------------
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ CAMPAIGN SETUP</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        niche = st.text_input("🎯 Niche / Industry", placeholder="e.g., Sustainable Fashion, SaaS, Fitness")
        product = st.text_input("💎 Product / Service Name", placeholder="e.g., Bamboo Hoodie, AI Writing Tool")
        platform = st.selectbox("📢 Target Platform", ["Facebook Ads", "Instagram Ads", "TikTok Ads", "Email Marketing"])
        tone = st.select_slider("🎭 Brand Tone", options=["Minimal", "Emotional", "Luxury", "Inspirational", "Aggressive"])
        target_audience = st.text_input("👥 Target Audience", placeholder="e.g., Women 25-40 interested in eco fashion")

    with col2:
        pain_point = st.text_area("💔 Customer Pain Point", placeholder="What problem keeps them awake at night?", height=100)
        benefits = st.text_area("🌟 Key Benefits", placeholder="- Benefit 1\n- Benefit 2\n- Benefit 3", height=100)
        offer = st.text_input("🎁 Special Offer / Hook", placeholder="e.g., 20% off first order, Free shipping")
        link = st.text_input("🔗 CTA Link (Optional)", placeholder="https://yoursite.com")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# 🔥 GENERATE
# -----------------------------
st.markdown("")
generate_btn = st.button("🔥 GENERATE FULL STRATEGY REPORT", use_container_width=True)

if generate_btn:
    if not product or not pain_point:
        st.warning("⚠️ Please fill in at least: Product Name + Customer Pain Point")
    else:
        with st.spinner("🧠 Beast AI is building your strategy..."):
            try:
                # PROMPT 1: 3 Ad Copy Variations
                ad_prompt = f"""
You are an elite marketing copywriter. Create 3 high-converting ad copy variations for:

Product: {product}
Niche: {niche}
Platform: {platform}
Tone: {tone}
Target Audience: {target_audience}
Pain Point: {pain_point}
Benefits: {benefits}
Special Offer: {offer}
CTA Link: {link if link else 'website'}

For each variation include:
- VARIATION NAME (e.g., Pain-Focused, Benefit-Focused, FOMO)
- HEADLINE (attention-grabbing, max 40 chars for ads)
- BODY TEXT (optimized for {platform})
- CTA BUTTON TEXT

Make each variation distinctly different in approach. Be specific, persuasive, and platform-native.
"""

                # PROMPT 2: Full Strategy
                strategy_prompt = f"""
Create a complete marketing strategy document for:

Product: {product}
Platform: {platform}
Tone: {tone}
Target Audience: {target_audience}
Pain Point: {pain_point}

Include:
1. TARGET AUDIENCE ANALYSIS (demographics, psychographics, behaviors)
2. MESSAGING FRAMEWORK (hook, story, offer, close)
3. A/B TESTING PLAN (what to test, how to measure)
4. KPIs & SUCCESS METRICS (CTR benchmarks, ROAS targets, CPM estimates)
5. RETARGETING STRATEGY (warm vs cold audience approach)
6. BUDGET ALLOCATION RECOMMENDATION
7. COMPETITOR DIFFERENTIATION

Be specific and actionable. This is a professional deliverable.
"""

                # PROMPT 3: Image Prompt
                image_prompt_request = f"""
Create a detailed, professional AI image generation prompt for:

Product: {product}
Platform: {platform}
Style/Tone: {tone}

Include:
- Composition and framing
- Lighting style
- Color palette with hex codes
- Mood and atmosphere
- Style references
- Technical specs for {platform}
- Negative prompts (what to avoid)

Make it ready to paste directly into Midjourney or DALL-E.
"""

                # API Calls
                ad_content = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": ad_prompt}],
                    max_tokens=2000
                ).choices[0].message.content

                strategy_content = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": strategy_prompt}],
                    max_tokens=2500
                ).choices[0].message.content

                img_content = client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": image_prompt_request}],
                    max_tokens=1000
                ).choices[0].message.content

                # -----------------------------
                # 📊 RESULTS DISPLAY
                # -----------------------------
                st.divider()
                st.markdown("## 📊 YOUR STRATEGY REPORT")

                # KPI Cards
                st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-value">3</div><div class="kpi-label">Ad Variations</div></div>
    <div class="kpi-card"><div class="kpi-value">>2.5%</div><div class="kpi-label">Target CTR</div></div>
    <div class="kpi-card"><div class="kpi-value">3-5x</div><div class="kpi-label">Est. ROAS</div></div>
    <div class="kpi-card"><div class="kpi-value">100%</div><div class="kpi-label">AI-Powered</div></div>
</div>
""", unsafe_allow_html=True)

                # Tabs for results
                tab1, tab2, tab3 = st.tabs(["📝 Ad Copy (3 Variations)", "🗺️ Full Strategy", "🎨 Image Prompt"])

                with tab1:
                    st.markdown('<div class="result-label">✍️ 3 HIGH-CONVERTING AD VARIATIONS</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{ad_content}</div>', unsafe_allow_html=True)

                with tab2:
                    st.markdown('<div class="result-label">🗺️ COMPLETE MARKETING STRATEGY</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{strategy_content}</div>', unsafe_allow_html=True)

                with tab3:
                    st.markdown('<div class="result-label">🎨 AI IMAGE GENERATION PROMPT</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{img_content}</div>', unsafe_allow_html=True)

                # -----------------------------
                # 📥 DOWNLOAD + SHARE
                # -----------------------------
                st.divider()
                dl_col, wa_col, li_col = st.columns(3)

                with dl_col:
                    pdf_data = create_pdf(ad_content, img_content, product, platform, tone, strategy_content)
                    st.download_button(
                        label="📥 Download Full PDF Report",
                        data=bytes(pdf_data),
                        file_name=f"Beast_Strategy_{product.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with wa_col:
                    wa_text = f"🦁 Marketing Strategy for {product}\n\n{ad_content[:300]}...\n\nGenerated by Marketing Beast AI"
                    wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
                    st.markdown(f'<a href="{wa_url}" target="_blank" class="share-btn wa-btn">💬 Share on WhatsApp</a>', unsafe_allow_html=True)

                with li_col:
                    li_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote('https://marketingbeast.streamlit.app')}"
                    st.markdown(f'<a href="{li_url}" target="_blank" class="share-btn li-btn">💼 Share on LinkedIn</a>', unsafe_allow_html=True)

                # Copy to clipboard area
                with st.expander("📋 Copy Raw Text"):
                    tab_c1, tab_c2 = st.tabs(["Ad Copy", "Strategy"])
                    with tab_c1:
                        st.text_area("", value=ad_content, height=200, key="copy_ad")
                    with tab_c2:
                        st.text_area("", value=strategy_content, height=200, key="copy_strategy")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your API key and try again.")

# -----------------------------
# 🦁 SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("### 🦁 Marketing Beast v5.0")
    st.markdown("---")
    st.markdown("**What you get:**")
    st.markdown("✅ 3 Ad Copy Variations")
    st.markdown("✅ Full Marketing Strategy")
    st.markdown("✅ AI Image Prompt")
    st.markdown("✅ KPIs & A/B Test Plan")
    st.markdown("✅ Professional PDF Export")
    st.markdown("---")
    st.caption("Powered by Groq + LLaMA 3.3 70B")
    st.caption("Built for Fiverr Professionals")
