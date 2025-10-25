#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)

from server.app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
#from src.api.v1.recommendation import router as recommendation_router

#app = FastAPI()

#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["*"],
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

#app.include_router(recommendation_router, prefix="/api/rest/v1", tags=["recommendation"])