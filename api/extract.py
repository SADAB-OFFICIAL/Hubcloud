from fastapi import FastAPI, Request
from extractor import extract_hubcloud

app = FastAPI()

@app.get("/")
async def root(request: Request):
    link = request.query_params.get("link")
    if not link:
        return {"error": "Missing 'link' parameter"}
    
    try:
        data = extract_hubcloud(link)
        return data
    except Exception as e:
        return {"error": str(e)}
