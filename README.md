# 🧾 InsureGenie – AI-Powered Insurance Compliance Agent

**InsureGenie** is an AI-powered tool that reads, summarizes, and checks compliance of insurance-related documents (PDFs, images, scans). It uses OCR, LLMs, and rule-based validation to make insurance paperwork understandable and automatable.

<div align="center">
  🔍 Built for document clarity & compliance.
</div>

---

## 📌 Key Features

✅ Extracts text using OCR from scanned images or PDFs  
✅ Summarizes complex insurance documents in human-friendly language  
✅ Performs compliance checks (like exclusions, policy number, date fields, etc.)  
✅ Validates structured fields like dates, amounts, document types  
✅ Clean UI built with Streamlit  
✅ Export/download summary  
✅ Hosted for live testing  

---

## 🚀 Live Demo

👉 [Click here to try the app live](https://your-app-url.streamlit.app)  
*(Replace with your actual Streamlit link)*

---

## 🏗️ Tech Stack

| Layer        | Tech Used                     |
|--------------|-------------------------------|
| UI & Frontend | `Streamlit`, HTML/CSS         |
| Backend Logic | `Python`, `OpenCV`, `Tesseract` |
| OCR Engine   | `pytesseract`, `pdfplumber`    |
| LLM API      | `Groq` (Mixtral-8x7B via OpenAI format) |
| Database     | `SQLite` (for metadata/logs)   |

---

## 🛠️ Setup Instructions

> 🖥️ Works best in a Python virtual environment

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/Insurance-compliance-AI-agent.git
cd Insurance-compliance-AI-agent
