from flask import Flask, render_template
from scraper import fetch_bulk_articles_from_main_page

app = Flask(__name__)

# Replace these with real, working news article URLs!
sample_urls = [
    "https://timesofindia.indiatimes.com/india/morning-newswrap-iran-strikes-back-at-israel-ahmedabad-plane-crash-toll-mounts-to-274-and-more/articleshow/121842028.cms",
    # Add more working news URLs here
]

@app.route("/")
def index():
    articles = fetch_bulk_articles_from_main_page("https://timesofindia.indiatimes.com/")
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)