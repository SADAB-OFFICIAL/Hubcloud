import requests
from bs4 import BeautifulSoup
import hashlib

def tokenized_url(url: str) -> str:
    token = hashlib.sha256(url.encode()).hexdigest()
    joiner = "&" if "?" in url else "?"
    return f"{url}{joiner}token={token}"

def extract_hubcloud(link: str) -> dict:
    r = requests.get(link, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.title.text.strip() if soup.title else "Unknown Title"

    streams = []
    for a in soup.select("a[href]"):
        href = a["href"]
        text = a.get_text(strip=True)

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
