import streamlit as st from groq import Groq import os import requests from bs4 import BeautifulSoup import json

================== UI Setup ==================

st.set_page_config(page_title="Marketing Beast AI v3.3", page_icon="⚡", layout="wide")

st.markdown("""

<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
    background-color: #1e293b !important; color: white !important;
    border: 1px solid #334155 !important; border-radius: 10px !important;
}
.stButton>button {
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    color: white; border: none; padding: 12px 24px; border-radius: 10px;
    font-weight: bold; width: 100%; transition: 0.3s;
}
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(37, 99, 235, 0.4); }
[data-testid="stSidebar"] { background-color: #0f172a; border-right: 1px solid #334155; }
.content-box { background-color: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #3b82f6; margin-top: 20px; }
</style>""", unsafe_allow_html=True)

================== Helper Functions ==================

def get_config(key): if key in st.secrets: return st.secrets[key] return os.environ.get(key)

NICHES = { "Spirituality & Awareness": "Vibrations, manifestation, and emotional healing.", "Make Money Online / Affiliate": "Passive income, financial freedom, and urgency.", "Health & Fitness": "Body transformation, energy, and self-confidence.", "Relationships & Dating": "Attraction, psychological connection, and confidence.", "Tech & AI Tools": "Efficiency, future-proofing, and saving time." }

STYLES = ["Aggressive", "Spiritual", "Storytelling", "Direct"] PLATFORMS = ["Facebook Ad", "Instagram Post", "TikTok Script", "Email Blast"] EMOTIONS = ["Peace", "Power", "Mystery", "Fear"]

--- Generate content with A/B variations ---

def generate_all(niche, style, platform, p_name, p_desc, p_pain, p_link, emotion): api_key = get_config("GROQ_API_KEY") if not api_key: return "⚠️ API Key missing! Please set GROQ_API_KEY." client = Groq(api_key=api_key) niche_focus = NICHES.get(niche, "")

prompt = f"""

You are a Master Marketer expert in {niche_focus}. Generate 3 high-converting {platform} posts in {style} style for '{p_name}' (Benefits: {p_desc}, Pain: {p_pain}, Link: {p_link}). Include 3 CTA variations. Generate 2 alternative versions for A/B testing for each post. Also, generate 1 detailed AI Image prompt for {emotion} emotion representing the niche. Format: ---COPY--- [Post 1 / Post 1B / Post 2 / Post 2B / Post 3 / Post 3B] ---CTA--- [CTA 1 / CTA 2 / CTA 3] ---IMAGE--- [Image Prompt] """

try:
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
except Exception as e:
    return f"⚠️ Error: {str(e)}"

================== Sidebar ==================

with st.sidebar: st.header("🎯 Strategy Center") selected_niche = st.selectbox("Select Niche", list(NICHES.keys())) selected_style = st.selectbox("Select Style", STYLES) selected_platform = st.selectbox("Target Platform", PLATFORMS) selected_emotion = st.selectbox("Image Emotion", EMOTIONS) st.markdown("---")

================== Main Inputs ==================

col1, col2 = st.columns(2) with col1: p_name = st.text_input("💎 Product Name") with col2: p_link = st.text_input("🔗 Affiliate Link")

p_pain = st.text_input("💔 Customer Pain Point") p_desc = st.text_area("🌟 Main Benefits", height=100)

================== Generate Button ==================

if st.button("🚀 UNLEASH THE BEAST"): if all([p_name, p_desc, p_link]): with st.spinner("Generating Marketing Arsenal..."): full_result = generate_all(selected_niche, selected_style, selected_platform, p_name, p_desc, p_pain, p_link, selected_emotion)

parts = full_result.split("---IMAGE---")
        copy_part = parts[0].split("---CTA---")[0].replace("---COPY---", "")
        cta_part = parts[0].split("---CTA---")[1] if "---CTA---" in parts[0] else "No CTA generated."
        image_part = parts[1] if len(parts) > 1 else "No image prompt generated."

        # Save to history (local JSON)
        history_file = "marketing_history.json"
        try:
            try: history = json.load(open(history_file))
            except: history = []
            history.append({"product": p_name, "copy": copy_part, "cta": cta_part, "image": image_part})
            json.dump(history, open(history_file, "w"), indent=2)
        except: pass

        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.markdown("### 🔥 Your Sales Copy (with A/B variations):")
        st.markdown(copy_part)
        st.markdown("---")
        st.markdown("### 🎯 CTA Options:")
        st.info(cta_part)
        st.markdown("---")
        st.markdown("### 🎨 AI Image Generator Prompt:")
        st.info(image_part)
        st.markdown("---")

        # Download output
        st.download_button("💾 Download Output as TXT", data=f"{copy_part}\n{cta_part}\n{image_part}", file_name=f"{p_name}_marketing.txt")

        # Interactive History
        st.markdown("### 🕘 History (Last 10 generations)")
        try:
            history = json.load(open(history_file))[-10:]
            for i, item in enumerate(history[::-1], 1):
                with st.expander(f"{i}. {item['product']}"):
                    st.markdown("**Copy:**")
                    st.markdown(item['copy'])
                    st.markdown("**CTA:**")
                    st.info(item['cta'])
                    st.markdown("**Image Prompt:**")
                    st.info(item['image'])
        except: st.info("No history available yet.")

        st.markdown('</div>', unsafe_allow_html=True)
        st.balloons()
else:
    st.error("Fill all fields first!")
