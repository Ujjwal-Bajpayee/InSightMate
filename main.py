from fastapi import FastAPI, Query
from recommend import recommend_articles, recommend_jobs
from utils import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="InSightMate API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "InSightMate API is running!"}

@app.get("/recommend")
def get_recommendations(prompt: str, page: int = Query(1, gt=0)):
    try:
        logger.info(f"Fetching recommendations for: {prompt} (Page {page})")
        try:
            articles = recommend_articles(prompt, page)
        except Exception as e:
            logger.error(f"Error in recommend_articles: {e}")
            articles = [{"type": "news", "title": "Error fetching articles", "url": "", "why": str(e)}]

        try:
            jobs = recommend_jobs(prompt, page)
        except Exception as e:
            logger.error(f"Error in recommend_jobs: {e}")
            jobs = [{"type": "job", "title": "Error fetching jobs", "url": "", "why": str(e)}]

        return {"recommendations": {"articles": articles, "jobs": jobs}}

    except Exception as e:
        logger.error(f"Unhandled error in /recommend: {e}")
        return {"error": str(e)}
