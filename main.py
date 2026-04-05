import gradio as gr
from app.api.ui import demo
from inference import app as fastapi_app

# Mount FastAPI + Gradio UI together
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")