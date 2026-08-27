import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from database import VoteDatabase, DEFAULT_DB_PATH, DEFAULT_JSON_PATH

app = FastAPI(title="Tumpak Sewu Guide API")

# Initialize DB
db = VoteDatabase(db_path=DEFAULT_DB_PATH, json_path=DEFAULT_JSON_PATH)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")
templates.env.cache = None

class VoteRequest(BaseModel):
    voter_name: str
    category: str
    choice: Optional[str] = None
    choice_id: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Bypass starlette TemplateResponse due to Jinja2 cache bug on Py 3.14
    template = templates.env.get_template("index.html")
    content = template.render()
    return HTMLResponse(
        content=content,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    )

@app.get("/api/health")
async def health_check():
    total_votes = 0
    if db:
        summary = db.get_all_votes_summary()
        total_votes = len(summary.get("raw_votes", []))
    return {
        "status": "ok",
        "health": "healthy",
        "persistence": "sqlite+json",
        "database": "connected",
        "total_votes_recorded": total_votes
    }

@app.get("/api/votes")
async def get_votes():
    try:
        summary = db.get_all_votes_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/vote")
async def post_vote(vote: VoteRequest):
    choice = vote.choice or vote.choice_id
    if not vote.voter_name.strip():
        raise HTTPException(status_code=400, detail="voter_name must be a non-empty string")
    if vote.category not in ("route", "destination"):
        raise HTTPException(status_code=400, detail="category must be 'route' or 'destination'")
    if not choice or not choice.strip():
        raise HTTPException(status_code=400, detail="choice must be a non-empty string")
    
    try:
        vote_record = db.record_vote(vote.voter_name, vote.category, choice)
        summary = db.get_all_votes_summary()
        return {
            "success": True,
            "message": f"Vote recorded successfully",
            "vote": vote_record,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/votes/reset")
async def reset_votes():
    try:
        db.reset_all_votes()
        summary = db.get_all_votes_summary()
        return {
            "success": True,
            "message": "All votes cleared successfully",
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
