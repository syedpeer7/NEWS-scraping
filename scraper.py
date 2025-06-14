import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {'url': url, 'title': 'Failed to fetch', 'text': f'Error: {e}'}

    soup = BeautifulSoup(response.text, 'html.parser')

    # Title extraction
    title = soup.title.string.strip() if soup.title and soup.title.string else 'No title found'

    # Improved: Try to find the main article container using common classes/ids/HTML5 tags
    article_container = (
        soup.find('div', class_="article-content") or
        soup.find('div', class_="ga-headlines") or
        soup.find('article') or
        soup.find('div', id="content") or
        soup
    )

    # Collect all content: headings, paragraphs, bullet points
    content_parts = []
    for tag in article_container.find_all([ 'span','h1', 'h2', 'h3', 'h4', 'p', 'li']):
        text = tag.get_text(strip=True)
        if text:
            content_parts.append(text)

    article_text = "\n\n".join(content_parts)

    return {
        'url': url,
        'title': title,
        'text': article_text
    }

def fetch_bulk_articles(url_list):
    articles = []
    for url in url_list:
        articles.append(fetch_article(url))
    return articles

def fetch_article_links(main_url):
    try:
        response = requests.get(main_url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching main page: {e}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        # For Times of India, articles typically have '/articleshow/' in URL
        if '/articleshow/' in href:
            full_url = urljoin(main_url, href)
            links.add(full_url)
    return list(links)

def fetch_bulk_articles_from_main_page(main_url, max_articles=10):
    article_links = fetch_article_links(main_url)
    articles = []
    for url in article_links[:max_articles]:  # Limit for demo/test purposes
        articles.append(fetch_article(url))
    return articles