import uvicorn

# Same app as main.py: FastAPI + Gradio UI at /ui (local use)
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)
    