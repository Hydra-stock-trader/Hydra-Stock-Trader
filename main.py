from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.endpoints.endpoints import router
from src.endpoints.sec_endpoints import router as sec_router

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)
app.include_router(sec_router)

@app.get("/")
async def root():
    return {"message": "HYDRA RAHHHHHH"}