from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """
    Returns 200 OK if the model has finished downloading/loading.
    Returns 503 if the model is still being processed.
    """
    


@app.post("/predict")
def predict():
    pass