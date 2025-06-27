import streamlit as st
import os
from db import init_db, save_upload, save_metadata, save_validation
from agent import run_agent, run_compliance_checks

# --- Custom CSS for modern, clean look ---
custom_css = """
<style>
body, .stApp {
    background-color: #f8fafc;
    color: #23272f !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}
[data-testid="stAppViewContainer"] > .main {
    background-color: #f8fafc;
    color: #23272f !important;
}
html, body, .stApp, .block-container, p, span, div, label, input, textarea {
    color: #23272f !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 50%, #80deea 100%);
    padding: 2rem 1rem;
}
[data-testid="stSidebar"] .block-container {
    background: transparent;
    box-shadow: none;
    padding: 0;
}
.sidebar-header {
    text-align: center;
    margin-bottom: 2rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}
.sidebar-section {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
.sidebar-title {
    color: #0097a7;
    font-weight: 700;
    font-size: 1.1em;
    margin-bottom: 0.5rem;
}
.sidebar-text {
    color: #23272f;
    font-size: 0.9em;
    line-height: 1.4;
}
.feature-list {
    color: #23272f;
    font-size: 0.85em;
    line-height: 1.5;
}
.feature-list li {
    margin-bottom: 0.3rem;
}
/* File uploader text styling */
section[data-testid="stFileUploaderDropzone"] p, 
section[data-testid="stFileUploaderDropzone"] div,
section[data-testid="stFileUploaderDropzone"] span {
    color: #23272f !important;
}
/* Analyze button text styling */
button[kind="primary"] {
    background: linear-gradient(90deg, #00bcd4 0%, #26c6da 100%);
    color: #f5f5dc !important;
    border-radius: 10px;
    border: none;
    font-weight: bold;
    font-size: 1.1em;
    padding: 0.6em 1.2em;
}
section[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(90deg, #e0f7fa 0%, #f5f5dc 100%);
    border: 2px dashed #00bcd4;
    border-radius: 16px;
    box-shadow: 0 2px 12px 0 rgba(44, 62, 80, 0.07);
}
.block-container {
    background: #fff;
    border-radius: 22px;
    box-shadow: 0 6px 32px 0 rgba(44, 62, 80, 0.09);
    padding: 2.5rem 2.5rem 1.5rem 2.5rem;
}
.upload-section {
    background: linear-gradient(90deg, #e0f7fa 0%, #f5f5dc 100%);
    border-radius: 18px;
    padding: 2em 1.5em 1.5em 1.5em;
    margin-bottom: 2em;
    box-shadow: 0 2px 12px 0 rgba(44, 62, 80, 0.07);
}
.summary-card, .ocr-card {
    background: #f8f8f5;
    border-radius: 14px;
    padding: 1.2em 1em 1em 1em;
    margin-bottom: 1.2em;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 8px 0 rgba(44, 62, 80, 0.04);
}
.compliance-card {
    background: #e0f7fa;
    border-radius: 14px;
    padding: 1.2em 1em 1em 1em;
    margin-bottom: 1.2em;
    border: 1px solid #b2ebf2;
    box-shadow: 0 2px 8px 0 rgba(44, 62, 80, 0.04);
}
.st-emotion-cache-1c7y2kd {
    padding-bottom: 0px !important;
}
h1, h2, h3, h4 {
    color: #0097a7;
    font-weight: 700;
}
.stAlert-success {
    background-color: #e0f2f1;
    color: #00796b;
}
.stAlert-error {
    background-color: #fff3e0;
    color: #d84315;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Enhanced Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" width="60" style="margin-bottom: 0.5rem;">
        <h2 style='color:#0097a7; margin: 0;'>InsureGenie</h2>
        <p style='color:#0097a7; margin: 0; font-size: 0.9em;'>AI Document Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">🚀 Features</div>
        <ul class="feature-list">
            <li>📄 OCR Text Extraction</li>
            <li>🧠 AI Summarization</li>
            <li>✅ Compliance Checking</li>
            <li>🔍 Document Validation</li>
            <li>📊 Database Storage</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">📋 Supported Formats</div>
        <div class="sidebar-text">
            • PDF Documents<br>
            • JPG Images<br>
            • PNG Images<br>
            • JPEG Images
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Main Title ---
st.markdown("""
<h1 style='margin-bottom:0.2em;'>📄 InsureGenie</h1>
<p style='color:#0097a7;font-size:1.2em;margin-top:0;'>Your AI-powered Insurance Document Compliance Assistant</p>
""", unsafe_allow_html=True)

init_db()

# --- Upload Section ---
st.markdown("""
<div class='upload-section'>
<h3>📤 Upload your insurance document</h3>
<p style='color:#23272f;'>Supported: <b>PDF, JPG, PNG</b>. We'll extract, summarize, and check compliance for you!</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload insurance document (JPG, PNG, PDF)",
    type=["jpg", "jpeg", "png", "pdf"],
    accept_multiple_files=False,
    label_visibility="visible"
)

ocr_text = summary = None
compliance_results = []
validation = None
extracted = None

if uploaded_file:
    if uploaded_file.type.startswith("image/"):
        st.image(uploaded_file, caption="Uploaded Document", use_container_width=True)
    elif uploaded_file.type == "application/pdf":
        st.info("PDF uploaded. All pages will be processed.")
    analyze = st.button("✨ Analyze Document", use_container_width=True)
    if analyze:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        doc_id = save_upload(filename)
        with st.spinner("Running OCR, summarization, and compliance checks..."):
            ocr_text, extracted, validation = run_agent(file_bytes, filename)
            summary = extracted.get("summary", "No summary available.")
            compliance_results = run_compliance_checks(ocr_text)
        save_metadata(doc_id, extracted)
        save_validation(doc_id, validation["status"], validation["errors"])
        # --- OCR & Summary Section ---
        with st.expander("📝 View OCR Text", expanded=False):
            st.markdown(f"<div class='ocr-card'><pre style='font-size:1em; color:#23272f;'>{ocr_text}</pre></div>", unsafe_allow_html=True)
        with st.expander("📝 View Summary", expanded=True):
            st.markdown(f"<div class='summary-card'>{summary}</div>", unsafe_allow_html=True)
        # --- Compliance Checklist ---
        st.markdown("<div class='compliance-card'><h3>✅ Compliance Checklist</h3>", unsafe_allow_html=True)
        for check in compliance_results:
            icon = "✅" if check['status'] == "✅" else "❌"
            st.markdown(f"<span style='font-size:1.1em;'>{icon} <b>{check['check']}</b>: <span style='color:#23272f;'>{check['details']}</span></span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        # --- Validation Section ---
        st.markdown("<div class='compliance-card'><h3>🔎 Validation Result</h3>", unsafe_allow_html=True)
        if validation["status"] == "✅":
            st.success("All fields valid!", icon="✅")
        else:
            st.error("Validation errors:", icon="❌")
            for err in validation["errors"]:
                st.write(f"- {err}")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='color:#b0bec5;font-size:1.1em;margin-top:2em;'>
    <i>Upload a document to get started.</i>
    </div>
    """, unsafe_allow_html=True)
