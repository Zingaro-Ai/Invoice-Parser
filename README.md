```markdown
# Single-Page PDF or Image to parse invoice

This application allows you to:

1. Upload either a single-page PDF or an image invoice.
2. If a PDF is uploaded:
   - Verify that it contains only one page.
   - Convert that page into a PNG image.
3. Convert the final image (original or from PDF) into a Base64 string.
4. Pass the Base64-encoded image to a model for inference.
5. Display the results as JSON.

## Setup

1. Create a `.env` file at the root of your project:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

Access the application in your browser via the provided local URL.
```