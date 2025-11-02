import React, { useState } from "react";
import "./App.css";  // ✅ correct path
import SearchBar from "./components/SearchBar";  // ✅ correct spelling
import NewsCard from "./components/NewsCard";    // ✅ correct file name


function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchNews = async (query) => {
    setLoading(true);
    const response = await fetch("http://127.0.0.1:8000/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await response.json();
    setArticles(data.articles || []);
    setLoading(false);
  };

  return (
    <div className="app-container">
      <h1>🧠 AI News Recommendation System</h1>
      <SearchBar onSearch={fetchNews} />
      {loading && <p>Loading news...</p>}

      <div className="news-grid">
        {articles.length > 0 ? (
          articles.map((article, index) => (
            <NewsCard key={index} article={article} />
          ))
        ) : (
          <p>💡 Try searching for topics like “AI”, “Space”, or “Technology”.</p>
        )}
      </div>
    </div>
  );
}

export default App;
