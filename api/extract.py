from fastapi import FastAPI, Request
from extractor import extract_hubcloud

app = FastAPI()

@app.get("/api/extract")  # Must match URL
async def extract(request: Request):
    link = request.query_params.get("link")
    if not link:
        return {"error": "Missing 'link' parameter"}
    
    try:
        return extract_hubcloud(link)
    except Exception as e:
        return {"error": str(e)}
