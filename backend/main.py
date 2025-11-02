


# from fastapi import FastAPI
# from pydantic import BaseModel
# from transformers import pipeline
# from sentence_transformers import SentenceTransformer
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import uvicorn
# import requests
# import nltk

# # Download NLTK data (only first run)
# nltk.download('vader_lexicon')

# app = FastAPI()
# from fastapi.middleware.cors import CORSMiddleware

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # or ["http://localhost:3000"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# -------------------- Load Models Once --------------------
# print("Loading models... please wait ⏳")
# summarizer = pipeline("summarization", model="t5-small")  # lightweight & fast
# sentiment_analyzer = SentimentIntensityAnalyzer()
# embedder = SentenceTransformer("all-MiniLM-L6-v2")
# print("✅ Models loaded successfully!")

# # -------------------- Request Schema --------------------
# class QueryRequest(BaseModel):
#     query: str

# # -------------------- Helper Functions --------------------
# def fetch_news(query, limit=5):
#     API_KEY = "3555a74b35c2431b8a2753bfd7c442c9"  # <-- Replace with your NewsAPI key
#     url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&pageSize={limit}&apiKey={API_KEY}"
#     data = requests.get(url).json()

#     articles = []
#     for a in data.get("articles", []):
#         articles.append({
#             "title": a["title"],
#             "content": a["content"],
#             "description": a["description"],
#             "url": a["url"],
#             "source": a["source"]["name"],
#             "image": a.get("urlToImage", "https://via.placeholder.com/400x200?text=No+Image")
#         })
#     return articles


# # -------------------- API Routes --------------------
# @app.get("/")
# def home():
#     return {"message": "AI News Recommendation API is running!"}


# @app.post("/recommend")
# def recommend(req: QueryRequest):
#     query = req.query
#     articles = fetch_news(query)

#     if not articles:
#         return {"articles": []}

#     # Summarize each article
#     for a in articles:
#         text = a["content"] or a["description"]
#         if text:
#             try:
#                 summary = summarizer(text, max_length=70, min_length=30, do_sample=False)[0]["summary_text"]
#             except:
#                 summary = text[:150] + "..."
#         else:
#             summary = "No content available."
#         a["summary"] = summary

#     # Sentiment Analysis
#     for a in articles:
#         score = sentiment_analyzer.polarity_scores(a["summary"])["compound"]
#         if score > 0.05:
#             a["sentiment"] = "Positive"
#         elif score < -0.05:
#             a["sentiment"] = "Negative"
#         else:
#             a["sentiment"] = "Neutral"

#     return {"articles": articles}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import requests
import os

# -----------------------------------------------------
# ✅ 1. Setup App
# -----------------------------------------------------
app = FastAPI(title="AI News Recommendation API", version="1.0")

# -----------------------------------------------------
# ✅ 2. Enable CORS (Allow Frontend Connection)
# -----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development; later use ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# ✅ 3. Load NLP Models Once
# -----------------------------------------------------
nltk.download("vader_lexicon")
summarizer = pipeline("summarization", model="t5-small")
sentiment_analyzer = SentimentIntensityAnalyzer()

# -----------------------------------------------------
# ✅ 4. Setup API Key (Replace with your own from https://newsapi.org)
# -----------------------------------------------------
NEWS_API_KEY = "3555a74b35c2431b8a2753bfd7c442c9"  # 🔴 Replace this with your actual key
NEWS_API_URL = "https://newsapi.org/v2/everything"

# -----------------------------------------------------
# ✅ 5. Request Model (for frontend POST)
# -----------------------------------------------------
class QueryRequest(BaseModel):
    query: str

# -----------------------------------------------------
# ✅ 6. Root Route
# -----------------------------------------------------
@app.get("/")
def root():
    return {"message": "AI News Recommendation API is running!"}

# -----------------------------------------------------
# ✅ 7. Helper Functions
# -----------------------------------------------------
def summarize_text(text):
    try:
        summary = summarizer(text, max_length=60, min_length=25, do_sample=False)
        return summary[0]["summary_text"]
    except Exception:
        return text  # fallback if summarizer fails


def get_sentiment(text):
    score = sentiment_analyzer.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# -----------------------------------------------------
# ✅ 8. Main Recommendation Endpoint
# -----------------------------------------------------
@app.post("/recommend")
def recommend_news(request: QueryRequest):
    query = request.query.strip()
    if not query:
        return {"error": "Query cannot be empty"}

    try:
        # Fetch news from NewsAPI
        response = requests.get(
            NEWS_API_URL,
            params={"q": query, "sortBy": "relevancy", "language": "en", "apiKey": NEWS_API_KEY},
        )
        data = response.json()

        if "articles" not in data or not data["articles"]:
            return {"message": "No news found for this topic."}

        articles = []
        for article in data["articles"][:6]:  # limit to 6 results
            content = article.get("content") or article.get("description") or ""
            summary = summarize_text(content) if content else "No content available."
            sentiment = get_sentiment(content)
            articles.append(
                {
                    "title": article["title"],
                    "summary": summary,
                    "sentiment": sentiment,
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "image": article.get("urlToImage"),
                }
            )

        return {"articles": articles}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------------------------------
# ✅ 9. Run the app (for manual testing)
# -----------------------------------------------------
# Run this only if executing main.py directly (not in production)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

