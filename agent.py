import os
import json
import re
import requests
from dotenv import load_dotenv
from ocr_tool import ocr_tool

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ GROQ_API_KEY not found in .env")

# ----------------------------
# Prompt Template
# ----------------------------
SUMMARY_PROMPT = """
You are a helpful assistant that summarizes complex insurance policy documents into simple, human-readable language.

Your task is to extract and summarize the following key points in plain English, so that a non-technical person with no insurance background can understand:

1. ✅ **Main coverage benefits**  
   - What is covered in this policy?
   - Who or what is protected?

2. ⚠️ **Exclusions / what is NOT covered**  
   - Clearly list anything that will cause claims to be denied.

3. 📅 **Policy duration and renewal**  
   - How long is the policy valid?
   - Does it auto-renew?

4. 💰 **Payment, fees, penalties**  
   - Any extra charges, hidden fees, or cancellation costs?

5. 📌 **Important conditions**  
   - Any special terms, age limits, paperwork requirements?

---
Use bullet points. Be short, clear, and conversational — avoid legal or technical language.  
Do NOT include a copy of the original text — only your easy-to-read summary.

Refer to this following document:
{raw_text}
"""

# ----------------------------
# Groq-based Summarization Tool
# ----------------------------
def summarize_tool(ocr_text):
    prompt = SUMMARY_PROMPT.format(raw_text=ocr_text[:3000])  # Trim if needed

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        # Use a currently supported Groq model (see https://console.groq.com/docs/models)
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You summarize insurance documents into bullet points for regular people."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        if response.status_code != 200:
            print(f"❌ Groq API error: {response.status_code} {response.text}")
            # Always return a dict for extracted
            return {"summary": f"❌ Groq API error: {response.status_code} {response.text}"}
        content = response.json()["choices"][0]["message"]["content"].strip()
        return {"summary": content}
    except Exception as e:
        print("❌ Groq API error:", e)
        return {"summary": f"❌ Groq API error: {e}"}

# ----------------------------
# Main Agent Interface
# ----------------------------
def run_agent(file_bytes, filename=None):
    print("📄 Running OCR...")
    ocr_text = ocr_tool(file_bytes, filename)

    if not ocr_text or len(ocr_text.strip()) < 20:
        return "", {"summary": "❌ No readable text found in the uploaded file."}, {"status": "❌", "errors": ["No readable text found in the uploaded file."]}

    print("🧠 Summarizing with Groq...")
    extracted = summarize_tool(ocr_text)

    validation = validate_tool(extracted)
    return ocr_text, extracted, validation

def validate_tool(fields):
    errors = []
    if "summary" not in fields or not fields["summary"] or fields["summary"].startswith("❌"):
        errors.append("Summary missing or failed to generate.")
    status = "✅" if not errors else "❌"
    return {"status": status, "errors": errors}

def run_compliance_checks(ocr_text):
    """
    Run compliance checks on OCR text for critical insurance info.
    Returns a list of dicts: {check, status, details}
    """
    checks = []
    # 1. Policy number (alphanumeric, at least 6 chars)
    policy_match = re.search(r'(policy\s*no\.?|policy\s*number)[:\s]*([A-Za-z0-9\-/]{6,})', ocr_text, re.IGNORECASE)
    checks.append({
        'check': 'Policy Number Present',
        'status': '✅' if policy_match else '❌',
        'details': policy_match.group(0) if policy_match else 'Not found'
    })
    # 2. Start and End Dates (DD/MM/YYYY)
    date_matches = re.findall(r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}', ocr_text)
    checks.append({
        'check': 'Start Date Present',
        'status': '✅' if len(date_matches) >= 1 else '❌',
        'details': date_matches[0] if len(date_matches) >= 1 else 'Not found'
    })
    checks.append({
        'check': 'End Date Present',
        'status': '✅' if len(date_matches) >= 2 else '❌',
        'details': date_matches[1] if len(date_matches) >= 2 else 'Not found'
    })
    # 3. Insurer name (common insurers)
    insurers = ["LIC", "HDFC", "Bajaj", "ICICI", "SBI", "Max Life", "Tata", "Aditya Birla", "Kotak", "Reliance"]
    insurer_found = next((name for name in insurers if re.search(rf'\b{name}\b', ocr_text, re.IGNORECASE)), None)
    checks.append({
        'check': 'Insurer Name Present',
        'status': '✅' if insurer_found else '❌',
        'details': insurer_found or 'Not found'
    })
    # 4. Coverage terms (keywords)
    coverage_terms = ["hospitalization", "coverage", "sum insured", "benefit", "treatment", "medical"]
    coverage_found = next((term for term in coverage_terms if re.search(term, ocr_text, re.IGNORECASE)), None)
    checks.append({
        'check': 'Coverage Terms Mentioned',
        'status': '✅' if coverage_found else '❌',
        'details': coverage_found or 'Not found'
    })
    # 5. Exclusions section
    exclusions_found = re.search(r'(exclusions|not covered)', ocr_text, re.IGNORECASE)
    checks.append({
        'check': 'Exclusions Section Present',
        'status': '✅' if exclusions_found else '❌',
        'details': exclusions_found.group(0) if exclusions_found else 'Not found'
    })
    return checks
