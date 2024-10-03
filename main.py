import os
import re
import gdown
import pdf2image
import pytesseract
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

def extract_text_from_pdf(pdf_path):
    try:
        pages = pdf2image.convert_from_path(pdf_path, 500)
        text_data = ''
        for page in pages:
            text = pytesseract.image_to_string(page)
            text_data += text + '\n'
        return text_data
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ''

def extract_email_and_phone(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+\s*[a-zA-Z0-9._%+-]*\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*(?:[a-zA-Z]{2,}|ac\.id|co\.id|go\.id|org\.id|net\.id|sch\.id|mil\.id|info|biz|xyz|me|online|tech|store|site|cloud)'
    phone_pattern = r'\b(?:\+?62|62|08)\d{2,3}[-\s]?\d{3,4}[-\s]?\d{3,4}\b'
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    cleaned_emails = [re.sub(r'\s*@\s*', '@', email) for email in emails]
    return cleaned_emails, phones

@app.route("/", methods=['GET'])
def main():
    return { "statusCode": 200, "message": "Hello World!"}

@app.route("/ocr", methods=['GET'])
def ocr():
    name = request.args.get('name', 'default_name')
    folder_id = request.args.get('folderId', 'default_folder_id')
    date = datetime.now().strftime("%d-%m-%Y")
    pdf_folder = f'./gdrive/{name}/{date}'
    os.makedirs(pdf_folder, exist_ok=True)
    try:
        gdown.download_folder(id=folder_id, output=pdf_folder, quiet=False)
        results = []
        for filename in os.listdir(pdf_folder):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(pdf_folder, filename)
                text = extract_text_from_pdf(pdf_path)
                emails, phones = extract_email_and_phone(text)
                results.append({
                    "text": text,
                    "filename": filename,
                    "emails": emails[0] if emails else None, 
                    "phones": phones[0] if phones else None
                })
        return jsonify({
            "statusCode": 200,
            "message": "OCR processing completed.",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "statusCode": 500,
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))