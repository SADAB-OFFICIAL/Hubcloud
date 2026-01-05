import requests
from bs4 import BeautifulSoup
import hashlib

# Optional proxy for bypassing blocks
PROXY_URL = None  # Example: "https://proxy.vlyx.workers.dev/?url="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/117.0.0.0 Safari/537.36"
}

def tokenized_url(url: str) -> str:
    token = hashlib.sha256(url.encode()).hexdigest()
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}token={token}"

def extract_hubcloud(link: str) -> dict:
    # Use proxy if set
    url = f"{PROXY_URL}{link}" if PROXY_URL else link

    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()  # will raise exception if 403/404

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.text.strip() if soup.title else "Unknown Title"

    streams = []
    for a in soup.select("a[href]"):
        href = a["href"]
        text = a.get_text(strip=True)

        # Filter relevant download links
        if href.startswith("http") and any(x in href for x in ["mkv", "pixeldrain", "hubcdn", "gigabytes"]):
            streams.append({
                "server": text or "Unknown",
                "type": "mkv",
                "link": href,
                "tokenized": tokenized_url(href)
            })

    return {
        "title": title,
        "streams": streams
    }
