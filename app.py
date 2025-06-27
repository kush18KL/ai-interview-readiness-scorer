import streamlit as st
import requests
import pdfplumber
import docx
from fpdf import FPDF
import re

# 🔐 Load Hugging Face API Key
with open("huggingface_key.txt", "r") as f:
    hf_token = f.read().strip()

# 📄 File Text Extractor
def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return "❌ Unsupported file format."

# 🤖 Hugging Face Inference API
def query_huggingface(prompt):
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return "⚠️ Unexpected response format."
    else:
        return f"❌ API Error: {response.status_code} - {response.text}"

# 📊 Simple keyword-based match score
def calculate_match_score(resume_text, jd_text):
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b\w+\b', jd_text.lower()))
    overlap = resume_words.intersection(jd_words)
    score = int((len(overlap) / len(jd_words)) * 100)
    return min(score, 100)

# 🧾 Generate downloadable PDF
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest="S").encode("latin1")

# 🌐 Streamlit App
st.set_page_config(page_title="AI Interview Coach", layout="centered")
st.title("🧠 AI Interview Readiness Scorer")
st.markdown("Upload your resume and job description to get interview questions and feedback!")

resume_file = st.file_uploader("📄 Upload Resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])
jd_file = st.file_uploader("📃 Upload Job Description (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

if st.button("✨ Generate Interview Questions") and resume_file and jd_file:
    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    # Score match
    match_score = calculate_match_score(resume_text, jd_text)
    st.subheader("📊 Resume–JD Match Score")
    st.progress(match_score / 100)
    st.markdown(f"**Match Score: {match_score}%**")

    # Prompt for Hugging Face
    prompt = f"""
    You are an AI interview coach.

    Given the following resume and job description, generate:
    1. 5 technical interview questions based on the job requirements.
    2. 3 behavioral questions based on the resume.
    3. Suggestions on what the candidate should prepare more based on the gap.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {jd_text}
    """

    with st.spinner("🤖 Generating interview questions..."):
        result = query_huggingface(prompt)

    st.subheader("🎤 Interview Questions and Feedback")
    st.markdown(result)

    # ⬇️ PDF Download
    pdf_bytes = generate_pdf(f"Match Score: {match_score}%\n\n{result}")
    st.download_button(
        label="📥 Download as PDF",
        data=pdf_bytes,
        file_name="interview_feedback.pdf",
        mime="application/pdf"
    )
