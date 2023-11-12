
from flask import Flask, render_template, request
from difflib import SequenceMatcher
import openai
import os
import PyPDF2
import json
from datetime import date
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = "your_api_key"


# Define a function to read a PDF file and extract its text
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for i in range(len(reader.pages)):
            # Get the i-th page and extract its text
            page = reader.pages[i]
            page_text = page.extract_text()

            # Add the extracted text to the final result
            text += page_text
        return text

# Define a function to generate a title for a given PDF file
def generate_title_from_pdf(pdf_path, question=None):
    # Extract the text from the PDF file
    text = extract_text_from_pdf(pdf_path)

  
    prompt = f"Text: {text}\n\nAnswer the following question: {question}\n\n"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text.strip()

    print("Generated Answer:", answer)

    return answer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file from the request
        file = request.files['file']

        # Save the file to the local file system
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Generate the title for the file
        question = request.form.get('question')
        answer = generate_title_from_pdf(file_path, question)
        
       
        return render_template('result.html', answer=answer)
    
    else:
        # Render the upload form page
        return render_template('index.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)
