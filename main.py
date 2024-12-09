import gradio as gr
import base64
import os
import json
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import tempfile
from invoice_parser import extract_invoice_elements
from PIL import Image

def run_model(base64_str):
    # Run your model inference
    invoice_results = extract_invoice_elements(base64_str)
    return invoice_results.dict()

def process_file(uploaded_file):
    if uploaded_file is None:
        return None, "No file uploaded."

    _, ext = os.path.splitext(uploaded_file.name.lower())
    allowed_image_ext = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]

    if ext == ".pdf":
        # Ensure single-page PDF
        try:
            reader = PdfReader(uploaded_file.name)
            num_pages = len(reader.pages)
            if num_pages > 1:
                return None, "Error: PDF contains more than one page."
        except Exception as e:
            return None, f"Error reading PDF: {e}"

        # Convert PDF page to image
        try:
            images = convert_from_path(uploaded_file.name)
            if len(images) != 1:
                return None, "Error: PDF must have exactly one page."
            img = images[0]

            # Save to temp PNG
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img_file:
                img_path = tmp_img_file.name
                img.save(img_path, "PNG")

            # Convert to base64
            with open(img_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode('utf-8')

            os.remove(img_path)

            # Run model
            model_output = run_model(encoded)
            return img, json.dumps(model_output, indent=2)
        except Exception as e:
            return None, f"Error converting PDF to image: {e}"

    elif ext in allowed_image_ext:
        # Already an image
        with open(uploaded_file.name, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')

        # Open image for display
        img = Image.open(uploaded_file.name)

        # Run model
        model_output = run_model(encoded)
        return img, json.dumps(model_output, indent=2)
    else:
        return None, "Unsupported file format. Please upload a PDF or supported image."


# Build the interface
with gr.Blocks() as demo:
    gr.Markdown("# Upload Single-Page PDF or Image and Run Model")

    with gr.Row():
        file_input = gr.File(label="Upload PDF or Image")
        submit_btn = gr.Button("Parse Invoice")

    with gr.Row():
        image_output = gr.Image(label="Image Preview", type="pil")
        output = gr.Textbox(label="JSON Results")

    submit_btn.click(process_file, inputs=file_input, outputs=[image_output, output])

if __name__ == "__main__":
    demo.launch()
