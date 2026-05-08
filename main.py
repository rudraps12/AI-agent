import gradio as gr

from app.api.logic import app as fastapi_app
from app.api.ui import demo

# FastAPI API with the Gradio application mounted at /ui.
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=7860)
