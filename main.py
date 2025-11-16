from fastapi import FastAPI
from pydantic import BaseModel
from utils.google_search import google_search
from utils.similarity import calculate_similarity, split_into_chunks
import uvicorn

app = FastAPI(
    title="AI Plagiarism Checker API",
    version="1.0",
    description="Backend API for AI Plagiarism Detection"
)

class CheckRequest(BaseModel):
    text: str

@app.post("/api/check")
async def check_plagiarism(req: CheckRequest):
    text = req.text.strip()

    if len(text) < 20:
        return {"error": "Text too short"}

    chunks = split_into_chunks(text)
    matched_sources = []
    matched_count = 0

    for chunk in chunks:
        results = await google_search(chunk)

        for result in results:
            snippet = result["snippet"]
            similarity = calculate_similarity(chunk, snippet)

            if similarity > 20:
                matched_sources.append({
                    "title": result["title"],
                    "link": result["link"],
                    "snippet": snippet,
                    "similarity": similarity,
                    "matched_text": chunk[:150]
                })
                matched_count += 1

    plagiarism_percent = round((matched_count / len(chunks)) * 100)

    return {
        "percentage": plagiarism_percent,
        "total_chunks": len(chunks),
        "matched_chunks": matched_count,
        "sources": sorted(matched_sources, key=lambda x: -x["similarity"])[:10]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
