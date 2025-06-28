import streamlit as st
import os
import tempfile
import base64
from utils.convertapi_utils import (
    convert_docx_to_pdf_and_download,
    convert_pdf_to_docx_and_download,
    compress_pdf_with_convertapi
)

# ================================
# 🎨 Custom CSS for Styling
# ================================
st.set_page_config(page_title="SmartDoc AI", layout="centered", page_icon="📄")

st.markdown("""
    <style>
    .landing-container {
        text-align: center;
        padding: 2em;
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        border-radius: 20px;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 2em;
    }
    .landing-title {
        font-size: 3em;
        font-weight: bold;
        background: -webkit-linear-gradient(left, #f857a6, #ff5858);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
        animation: fadeIn 1s ease-in-out;
    }
    .landing-subtext {
        font-size: 1.3em;
        color: #222;
        margin-bottom: 2em;
    }
    .stButton > button {
        background: linear-gradient(to right, #36d1dc, #5b86e5);
        color: white;
        padding: 0.7em 1.5em;
        border: none;
        border-radius: 8px;
        font-size: 1.1em;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background: linear-gradient(to right, #5b86e5, #36d1dc);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(91,134,229,0.4);
        cursor: pointer;
    }
    @keyframes fadeIn {
        0% {opacity: 0; transform: translateY(-10px);}
        100% {opacity: 1; transform: translateY(0);}
    }
    </style>
""", unsafe_allow_html=True)

# ================================
# 🔊 Success Sound Function
# ================================
def play_success_sound():
    try:
        file_path = "static/success.mp3"
        if os.path.exists(file_path):
            with open(file_path, "rb") as sound_file:
                b64 = base64.b64encode(sound_file.read()).decode()
                md = f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                """
                st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.warning("Sound error: " + str(e))

# ================================
# 🏠 Landing Section
# ================================
st.markdown("""
<div class="landing-container">
    <h1 class="landing-title">SmartDoc AI 📄</h1>
    <p class="landing-subtext">Convert, Translate, Style, and Compress your Documents with AI ✨</p>
</div>
""", unsafe_allow_html=True)

# ================================
# 🔐 ConvertAPI Token
# ================================
CONVERTAPI_BEARER_TOKEN = "hngs4CnuwWDhA8NUsmaoGLSjp2L3ELW2"

if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = []

# ================================
# 📄 Word to PDF
# ================================
st.header("📄 Word to PDF Converter")

uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")
    if st.button("Convert to PDF"):
        with st.spinner("🔄 Converting..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            os.makedirs("downloads", exist_ok=True)
            success, result = convert_docx_to_pdf_and_download(
                filepath=tmp_path,
                output_folder="downloads",
                bearer_token=CONVERTAPI_BEARER_TOKEN
            )
            if success:
                st.success("✅ Converted successfully!")
                st.balloons()
                play_success_sound()
                st.download_button("⬇️ Download PDF", open(result, "rb"), file_name=os.path.basename(result))
                st.session_state.conversion_history.append(f"{uploaded_file.name} ➡️ PDF")
            else:
                st.error(f"❌ Conversion failed: {result}")

# ================================
# 🔄 PDF to Word
# ================================
st.header("📄 PDF to Word Converter")

uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"], key="pdf_upload")
if uploaded_pdf:
    st.success(f"Uploaded: {uploaded_pdf.name}")
    if st.button("Convert to Word"):
        with st.spinner("🔄 Converting PDF to DOCX..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.read())
                tmp_path = tmp_file.name
            os.makedirs("downloads", exist_ok=True)
            success, result = convert_pdf_to_docx_and_download(
                filepath=tmp_path,
                output_folder="downloads",
                bearer_token=CONVERTAPI_BEARER_TOKEN
            )
            if success:
                st.success("✅ Converted successfully!")
                st.balloons()
                play_success_sound()
                st.download_button("⬇️ Download Word File", open(result, "rb"), file_name=os.path.basename(result))
                st.session_state.conversion_history.append(f"{uploaded_pdf.name} ➡️ DOCX")
            else:
                st.error(f"❌ Conversion failed: {result}")

# ================================
# 🌐 Translate & Style DOCX
# ================================
st.header("🌐 Translate & Style Word Document")

uploaded_docx = st.file_uploader("Upload a DOCX file", type=["docx"], key="translate_docx")
if uploaded_docx:
    st.success(f"Uploaded: {uploaded_docx.name}")
    lang = st.text_input("🌍 Target Language (e.g., hi, fr, es)", value="hi")
    font_name = st.text_input("🔤 Font Name", value="Arial")
    font_size = st.slider("🔠 Font Size", min_value=8, max_value=36, value=12)

    if st.button("🛠️ Translate & Style"):
        with st.spinner("Processing..."):
            from docx import Document
            from utils.editor import translate_paragraphs, style_paragraphs, save_document
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_input:
                tmp_input.write(uploaded_docx.read())
                input_path = tmp_input.name
            doc = Document(input_path)
            doc = translate_paragraphs(doc, target_lang=lang)
            doc = style_paragraphs(doc, font_name=font_name, font_size=font_size)
            os.makedirs("downloads", exist_ok=True)
            output_path = os.path.join("downloads", "translated_styled_" + uploaded_docx.name)
            save_document(doc, output_path)
            st.success("✅ Translation and styling completed!")
            st.balloons()
            play_success_sound()
            st.download_button("⬇️ Download Edited DOCX", open(output_path, "rb"), file_name=os.path.basename(output_path))
            st.session_state.conversion_history.append(f"{uploaded_docx.name} ➡️ Translated & Styled")

# ================================
# 🗜️ PDF Compression
# ================================
st.header("📉 Compress PDF File")

uploaded_pdf_to_compress = st.file_uploader("Upload a PDF to compress", type=["pdf"], key="compress_pdf")
if uploaded_pdf_to_compress:
    st.success(f"Uploaded: {uploaded_pdf_to_compress.name}")
    selected_quality = st.selectbox("Select Compression Quality", ["low", "medium", "high"])
    if st.button("Compress PDF"):
        with st.spinner("🔄 Compressing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf_to_compress.read())
                tmp_path = tmp_file.name
            os.makedirs("downloads", exist_ok=True)
            success, result = compress_pdf_with_convertapi(
                filepath=tmp_path,
                output_folder="downloads",
                bearer_token=CONVERTAPI_BEARER_TOKEN,
                quality=selected_quality
            )
            if success:
                st.success("✅ Compression successful!")
                st.balloons()
                play_success_sound()
                st.download_button("⬇️ Download Compressed PDF", open(result, "rb"), file_name=os.path.basename(result))
                st.session_state.conversion_history.append(f"{uploaded_pdf_to_compress.name} ➡️ Compressed ({selected_quality})")
            else:
                st.error(f"❌ Compression failed: {result}")

# ================================
# 🕘 Conversion History
# ================================
st.markdown("---")
st.subheader("🕘 Conversion History")

if st.session_state.conversion_history:
    for record in reversed(st.session_state.conversion_history):
        st.markdown(f"- {record}")
else:
    st.info("No file history yet.")

if st.button("🧹 Clear History"):
    st.session_state.conversion_history.clear()
    st.success("History cleared!")
    st.snow()
    play_success_sound()

# ================================
# 👩‍💻 Footer
# ================================
st.markdown("---")
st.caption("Made with ❤️ by **Salwa Kazmi** using Python & Streamlit · © 2025 SmartDoc AI")
