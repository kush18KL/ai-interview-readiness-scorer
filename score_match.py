from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Read the extracted text
with open("resume_text.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

with open("job_text.txt", "r", encoding="utf-8") as f:
    job_text = f.read()

# Combine into a corpus
corpus = [resume_text, job_text]

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(corpus)

# Calculate cosine similarity
similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
percentage_score = round(similarity * 100, 2)

# Show the result
print(f"\n🎯 Resume-JD Match Score: {percentage_score}%")

# Optional: Highlight missing keywords
resume_words = set(resume_text.lower().split())
job_words = set(job_text.lower().split())

missing_keywords = job_words - resume_words
top_missing = sorted(list(missing_keywords))[:20]  # show 20 only

print("\n📌 Some important words in JD that are missing from your resume:")
for word in top_missing:
    print("-", word)
