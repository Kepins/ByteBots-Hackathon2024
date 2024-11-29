import pickle
from functools import lru_cache
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile

import numpy as np
from pydantic import BaseModel


@lru_cache
def load_model():
    with open("decisiontree.bin", "rb") as f:
        return pickle.loads(f.read())

def model_predict(x):
    model = load_model()
    return model.predict(x)


from fastapi import FastAPI

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PerdictInput(BaseModel):
    age: int
    sex: Literal["M", "F"]
    on_thyroxine: bool
    query_on_thyroxine: bool
    on_antithyroid_meds: bool
    sick: bool
    pregnant: bool
    thyroid_surgery: bool
    I131_treatment: bool
    query_hypothyroid: bool
    query_hyperthyroid: bool
    lithium: bool
    goitre: bool
    tumor: bool
    hypopituitary: bool
    psych: bool
    TSH: float
    T3: float
    TT4: float
    T4U: float
    FTI: float

    def to_x(self):
        return np.array([
            self.age,
            1 if self.sex == "M" else 0,
            int(self.on_thyroxine),
            int(self.query_on_thyroxine),
            int(self.on_antithyroid_meds),
            int(self.sick),
            int(self.pregnant),
            int(self.thyroid_surgery),
            int(self.I131_treatment),
            int(self.query_hypothyroid),
            int(self.query_hyperthyroid),
            int(self.lithium),
            int(self.goitre),
            int(self.tumor),
            int(self.hypopituitary),
            int(self.psych),
            self.TSH,
            self.T3,
            self.TT4,
            self.T4U,
            self.FTI,
        ]).reshape(1, -1)


class PredictOutput(BaseModel):
    prediction: Literal["Negative", "Hyperthyroid", "Hypothyroid"]

    @staticmethod
    def from_y(output: int) -> "PredictOutput":
        match output:
            case 0:
                return PredictOutput(prediction="Negative")
            case 1:
                return PredictOutput(prediction="Hyperthyroid")
            case 2:
                return PredictOutput(prediction="Hypothyroid")
        raise ValueError(f"Wrong output: {output}")


class PredictImageOutput(BaseModel):
    prediction: int

    @staticmethod
    def from_y(output: float) -> "PredictImageOutput":
        prediction = max(min(int(output), 5), 1)
        return PredictImageOutput(prediction=prediction)


@app.post("/predict", name="predict")
def predict(data: PerdictInput) -> PredictOutput:
    return PredictOutput.from_y(model_predict(data.to_x()))


@app.post("/predict-image", name="predict-image")
def predict_image(file: UploadFile) -> PredictImageOutput:
    return PredictImageOutput.from_y(3.55)  # TODO
