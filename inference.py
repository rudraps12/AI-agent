from fastapi import FastAPI
from pydantic import BaseModel

# ✅ import YOUR existing function
from app.api.ui import process_email

app = FastAPI()

# Input schema (required by OpenEnv)
class StepInput(BaseModel):
    input: str


# ✅ REQUIRED endpoint 1
@app.post("/reset")
def reset():
    return {"status": "ok"}


# ✅ REQUIRED endpoint 2
@app.post("/step")
def step(data: StepInput):
    try:
        result = process_email(data.input)

        return {
            "output": result
        }

    except Exception as e:
        return {
            "output": f"Error: {str(e)}"
        }