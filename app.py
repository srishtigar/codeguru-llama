import requests
import json
import gradio as gr
import datetime

# API setup
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
history = []

# Generate response from API
def generate_response(prompt):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append(f"[{timestamp}] You: {prompt}")
    final_prompt = "\n".join(history)

    data = {
        "model": "codeguru",
        "prompt": final_prompt,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        data = response.json()
        answer = data['response']
        history.append(f"[{timestamp}] CodeGuru: {answer}")
        return answer
    else:
        return f"⚠️ Error: {response.text}"

# Reset conversation
def clear_history():
    history.clear()
    return "🔄 Chat cleared. Ready for a fresh start."

# Interface
with gr.Blocks(title="CodeGuru - Review Assistant") as interface:
    gr.HTML("""
        <style>
            body, html {
                background-color: #0c0c0c !important;
                color: #ffffff !important;
                font-family: 'Fira Code', 'JetBrains Mono', monospace;
            }
            .gradio-container {
                background-color: #0c0c0c !important;
            }
            textarea, input {
                background-color: #1a1a1a !important;
                color: #f2f2f2 !important;
                border: 1px solid #444 !important;
            }
            .gr-button {
                background-color: #2a2a2a !important;
                color: #ffffff !important;
                border: 1px solid #666 !important;
            }
            .gr-button:hover {
                background-color: #444 !important;
                color: #00ffe7 !important;
            }
        </style>
    """)

    # Fixed visible heading and subheading using gr.HTML
    gr.HTML("""
        <div style="text-align:center; font-size:28px; color:white; font-weight:bold; margin-bottom:4px;">
            📁 CodeGuru – Advanced Code Review Assistant
        </div>
        <div style="text-align:center; font-size:15px; color:#cccccc; font-style:italic; margin-bottom:20px;">
            Built for developers, researchers, and NGOs – Secure. Local. Reliable.
        </div>
    """)

    # Text inputs/outputs
    with gr.Column():
        input_box = gr.Textbox(
            label="Your Prompt",
            placeholder="→ Ask something (Python, SQL, APIs...)",
            lines=4
        )

        output_box = gr.Textbox(
            label="CodeGuru's Response",
            lines=10
        )

        with gr.Row():
            submit_btn = gr.Button("Run")
            clear_btn = gr.Button("Reset")

    # Event handlers
    submit_btn.click(fn=generate_response, inputs=input_box, outputs=output_box)
    clear_btn.click(fn=clear_history, inputs=[], outputs=output_box)

# Run app
interface.launch()
