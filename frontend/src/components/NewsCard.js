import React from "react";

function NewsCard({ article }) {
  const { title, summary, sentiment, image, url, source } = article;
  const emoji =
    sentiment === "Positive" ? "😊" : sentiment === "Negative" ? "😞" : "😐";

  return (
    <div className="news-card">
      <img src={image} alt="news" />
      <div className="news-info">
        <h3>{title}</h3>
        <p className="summary">{summary}</p>
        <p className="sentiment">
          <b>💬 Sentiment:</b> {emoji} {sentiment}
        </p>
        <p className="source">🗞 {source}</p>
        <a href={url} target="_blank" rel="noreferrer">
          Read More →
        </a>
      </div>
    </div>
  );
}

export default NewsCard;
