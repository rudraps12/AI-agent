"""
Run the Email Triage app locally in VS Code or from a terminal.

- API docs: http://127.0.0.1:7860/docs
- Gradio UI: http://127.0.0.1:7860/ui
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=7860,
        reload=True,
    )
