from fastapi import FastAPI, Request
from extractor import extract_hubcloud

app = FastAPI()

@app.get("/api/extract")
async def extract(request: Request):
    link = request.query_params.get("link")
    if not link:
        return {"error": "Missing 'link' parameter"}
    
    try:
        data = extract_hubcloud(link)
        return data
    except requests.exceptions.HTTPError as e:
        return {"error": f"{e.response.status_code} {e.response.reason}: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
