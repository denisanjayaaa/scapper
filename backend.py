from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio
from scraper import scrape_all_async
from ai_parser import parse_with_ai

app = FastAPI(title="Marketplace Price Aggregator API")

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: list

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    query = request.query
    raw_results = await scrape_all_async(query)

    final_results = []
    # In a real app we might run these concurrently.
    for platform, text_data in raw_results.items():
        if text_data:
            parsed_items = parse_with_ai(text_data, platform, query)
            if parsed_items:
                final_results.extend(parsed_items)

    return SearchResponse(results=final_results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
