import gradio as gr
from app.api.ui import demo
from inference import app as fastapi_app

# Mount UI at /ui so API can use /docs
app = gr.mount_gradio_app(fastapi_app, demo, path="/ui")