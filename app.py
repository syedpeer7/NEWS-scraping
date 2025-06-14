from flask import Flask, render_template
from scraper import fetch_article_links, fetch_article
import threading

app = Flask(__name__)

ARTICLES_CACHE = []
PROCESSING = False

def process_articles(main_url, max_articles=10):
    global ARTICLES_CACHE, PROCESSING
    PROCESSING = True
    ARTICLES_CACHE.clear()
    links = fetch_article_links(main_url)
    for url in links[:max_articles]:
        article = fetch_article(url)
        ARTICLES_CACHE.append(article)
    PROCESSING = False

@app.route("/")
def index():
    global PROCESSING
    if not ARTICLES_CACHE and not PROCESSING:
        # Start processing in the background if not already running
        thread = threading.Thread(target=process_articles, args=("https://timesofindia.indiatimes.com/", 10), daemon=True)
        thread.start()
        PROCESSING = True
    return render_template("index.html", articles=ARTICLES_CACHE, processing=PROCESSING)

if __name__ == "__main__":
    app.run(debug=True)
