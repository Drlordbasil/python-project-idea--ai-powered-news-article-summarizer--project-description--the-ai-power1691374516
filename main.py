from transformers import pipeline
from bs4 import BeautifulSoup
import requests
Optimized Python script:


class NewsArticleSummarizer:
    def __init__(self):
        self.nlp = pipeline("summarization")
        self.sentiment_analysis_model = "textattack/bert-base-uncased-imdb"

    def fetch_articles(self, source_url):
        """
        Fetches news articles from the given source URL using web scraping.
        """
        response = requests.get(source_url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("article")

        news_articles = [
            {
                "title": article.find("h2").text.strip(),
                "author": article.find("span", class_="author").text.strip(),
                "date": article.find("time")["datetime"],
                "content": article.find("div", class_="content").text.strip()
            }
            for article in articles
        ]

        return news_articles

    def summarize_article(self, article):
        """
        Generates a summary of the article using NLP techniques.
        """
        summary = self.nlp(article["content"], max_length=100, min_length=30, do_sample=False)[0][
            "summary_text"]

        return summary

    def filter_by_topic(self, articles, topic):
        """
        Filters articles based on user's preferred topics.
        """
        filtered_articles = [
            article for article in articles if topic.lower() in article["content"].lower()
        ]

        return filtered_articles

    def analyze_sentiment(self, article):
        """
        Determines the sentiment expressed in the article using sentiment analysis.
        """
        sentiment = self.nlp(article["content"], model=self.sentiment_analysis_model)[0][
            "label"]

        return sentiment

    def generate_summary(self, source_url, topic=None, sentiment=None):
        """
        Fetches articles, filters by topic if specified, and generates summaries.
        """
        articles = self.fetch_articles(source_url)

        if topic:
            articles = self.filter_by_topic(articles, topic)

        if sentiment:
            filtered_articles = [
                article for article in articles if self.analyze_sentiment(article) == sentiment
            ]
            articles = filtered_articles

        summaries = [
            {
                "title": article["title"],
                "summary": self.summarize_article(article)
            }
            for article in articles
        ]

        return summaries


def main():
    # Example usage
    summarizer = NewsArticleSummarizer()
    source_url = "https://example.com/news"
    topic = "technology"
    sentiment = "positive"
    summaries = summarizer.generate_summary(source_url, topic, sentiment)

    for summary in summaries:
        print("Title:", summary["title"])
        print("Summary:", summary["summary"])
        print()


if __name__ == "__main__":
    main()
