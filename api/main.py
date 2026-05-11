from ddgs import DDGS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from urllib.parse import urlparse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_site_name(url: str):
    domain = urlparse(url).netloc  # e.g. 'www.onmanorama.com'
    domain = domain.replace("www.", "")  # remove www
    name = domain.split(".")[0]  # 'onmanorama'
    return name.capitalize()


@app.get("/images")
def image_search(q: str):
    results = DDGS().images(q, max_results=6)
    return {"results": [r["image"] for r in results]}


@app.get("/search")
def web_search(q: str, max_results: int = 10):
    results = DDGS().text(q, max_results=max_results)
    return {
        "results": [
            {
                "title": r["title"],
                "url": r["href"],
                "snippet": r["body"],
                "site": get_site_name(r["href"]),
                "favicon": f"https://www.google.com/s2/favicons?domain={r['href']}&sz=32",
            }
            for r in results
        ]
    }


handler = Mangum(app)

