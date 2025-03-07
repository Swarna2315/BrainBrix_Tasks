import gradio as gr
from utils.pdf_utils import extract_text_from_pdf
from utils.chat_utils import ask_groq

# Store extracted text globally (per session)
pdf_text = ""

def upload_pdf(file):
    """Handles PDF upload and text extraction."""
    global pdf_text
    if file is None:
        return "No file uploaded. Please upload a PDF."
    
    pdf_text = extract_text_from_pdf(file.name)
    return "PDF uploaded successfully! You can now ask questions."

def chat_with_pdf(question):
    """Handles user queries and returns AI-generated responses."""
    global pdf_text
    if not pdf_text:
        return "Please upload a PDF first."
    
    return ask_groq(question, pdf_text)

# Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📄 Chat with your PDF using Groq AI")
    
    with gr.Row():
        file_input = gr.File(label="Upload your PDF", type="filepath")
        upload_button = gr.Button("Upload")
    
    status_text = gr.Textbox(label="Status", interactive=False)
    
    chat_input = gr.Textbox(label="Ask a question")
    chat_output = gr.Textbox(label="AI Response", interactive=False)
    submit_button = gr.Button("Get Answer")

    # Event Listeners
    upload_button.click(upload_pdf, inputs=[file_input], outputs=[status_text])
    submit_button.click(chat_with_pdf, inputs=[chat_input], outputs=[chat_output])

# Launch the app
if __name__ == "__main__":
    demo.launch()
