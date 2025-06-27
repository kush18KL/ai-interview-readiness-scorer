import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# === Example usage ===
resume_path = input("Enter path to your RESUME PDF: ").strip()
job_path = input("Enter path to JOB DESCRIPTION PDF or TXT: ").strip()

resume_text = extract_text_from_pdf(resume_path)
job_text = extract_text_from_pdf(job_path)

# Save outputs (optional)
with open("resume_text.txt", "w", encoding="utf-8") as f:
    f.write(resume_text)

with open("job_text.txt", "w", encoding="utf-8") as f:
    f.write(job_text)

print("\n✅ Extracted text from both files and saved as .txt")
