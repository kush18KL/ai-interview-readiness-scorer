# 🧠 AI Interview Readiness Scorer

This is a smart AI-powered tool that analyzes your resume and job description to:
- ✅ Score your resume’s match with the job
- 🧠 Highlight missing keywords
- 🎯 Generate potential interview questions
- 📋 Suggest resume improvements

---

## 📂 Features
- 🔍 Resume vs JD Match Scoring
- 🤖 AI-generated Interview Questions (OpenAI/HuggingFace)
- 📊 Keyword analysis with feedback
- 📝 Built-in resume text extraction
- 🧪 Simple CLI-based interface

---

## 🛠️ Tech Stack
- Python 3.10+
- OpenAI API (or Hugging Face Transformers)
- Pandas, Scikit-learn
- Flask (for future web integration)
- PDF/Text parsing

---

## 📦 How to Run

```bash
# Clone repo
git clone https://github.com/kush18KL/ai-interview-readiness-scorer.git
cd ai-interview-readiness-scorer

# Create a virtual environment
python -m venv env
env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your keys (optional)
echo "your-openai-key" > openai_key.txt
echo "your-huggingface-token" > huggingface_key.txt

# Run the scorer
python app.py
