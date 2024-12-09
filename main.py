import gradio as gr
import base64
import os
import json
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import tempfile
from invoice_parser import extract_invoice_elements

def run_model(base64_str):
    invoice_results = extract_invoice_elements(base64_str)
    return invoice_results.dict()


def process_file(uploaded_file):
    if uploaded_file is None:
        return "No file uploaded."

    # Check the file extension
    _, ext = os.path.splitext(uploaded_file.name.lower())
    allowed_image_ext = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]

    if ext == ".pdf":
        # Check if the PDF has only one page
        try:
            reader = PdfReader(uploaded_file.name)
            num_pages = len(reader.pages)
            if num_pages > 1:
                return "Error: PDF contains more than one page."
        except Exception as e:
            return f"Error reading PDF: {e}"

        # Convert the single-page PDF to an image (PNG)
        try:
            # Convert PDF to images (list of PIL Images)
            images = convert_from_path(uploaded_file.name)
            if len(images) != 1:
                return "Error: PDF must have exactly one page."
            img = images[0]

            # Save PIL image to a temporary PNG file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img_file:
                img_path = tmp_img_file.name
                img.save(img_path, "PNG")

            # Read the PNG file and convert to base64
            with open(img_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode('utf-8')

            # Remove the temporary file
            os.remove(img_path)

            # Pass the base64 image to the model
            model_output = run_model(encoded)
            return json.dumps(model_output, indent=2)
        except Exception as e:
            return f"Error converting PDF to image: {e}"

    elif ext in allowed_image_ext:
        # It's already an image, just convert to base64
        with open(uploaded_file.name, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode('utf-8')

        # Pass the base64 image to the model
        model_output = run_model(encoded)
        return json.dumps(model_output, indent=2)
    else:
        return "Unsupported file format. Please upload a PDF or supported image."


# Build the interface
with gr.Blocks() as demo:
    gr.Markdown("# Upload Single-Page PDF or Image and Run Model")
    file_input = gr.File(label="Upload PDF or Image")
    output = gr.Textbox(label="JSON Results")
    submit_btn = gr.Button("Parse Invoice")

    submit_btn.click(process_file, inputs=file_input, outputs=output)

if __name__ == "__main__":
    demo.launch()
