from ddgs import DDGS
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/images")
def image_search(q: str):
    results = DDGS().images(q, max_results=6)
    return {"results": [r["image"] for r in results]}

handler = Mangum(app)