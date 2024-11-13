from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import torch

app = FastAPI()

# https://huggingface.co/SamLowe/roberta-base-go_emotions
# Load Classifier Model
model_name = "SamLowe/roberta-base-go_emotions"
classifier = pipeline(task="text-classification", model=model_name, top_k=None)

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict(request:PredictRequest):
    try:
        # Run Classifier Model
        model_outputs = classifier(request.text)
        #response=model_outputs[0]
        response = {}

        for i in range(len(model_outputs[0])):
            result = model_outputs[0][i]
            response[result['label']] = result['score']

        return { "result": response }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/healthcheck")
async def healthcheck():
    try:
        return { "data": "Im working just fine" }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))