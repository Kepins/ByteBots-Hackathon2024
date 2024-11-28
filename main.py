import pickle
from functools import lru_cache
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware

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

class Input(BaseModel):
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

class Output(BaseModel):
    prediction: Literal["Negative", "Hyperthyroid", "Hypothyroid"]

    @staticmethod
    def from_y(output: int):
        match output:
            case 0:
                return Output(prediction="Negative")
            case 1:
                return Output(prediction="Hyperthyroid")
            case 2:
                return Output(prediction="Hypothyroid")
        raise ValueError(f"Wrong output: {output}")


@app.post("/", name="predict")
async def root(data: Input) -> Output:
    return Output.from_y(model_predict(data.to_x()))
