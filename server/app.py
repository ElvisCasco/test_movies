from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data_loader import load_csvs
from .routers import movies, ratings, recommendation  # add recommendation
from .database import engine, Base

app = FastAPI(title="MovieLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(movies.router, prefix="/api/rest/v1/movies", tags=["movies"])
app.include_router(ratings.router, prefix="/api/rest/v1/ratings", tags=["ratings"])
app.include_router(recommendation.router, prefix="/api/rest/v1", tags=["recommendation"])  # new router

@app.on_event("startup")
def startup_load_data():
    # create DB tables if needed, then load CSVs
    Base.metadata.create_all(bind=engine)
    app.state.data = load_csvs()

@app.get("/")
def root():
    return {"message": "MovieLens API"}