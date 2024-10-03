import os
import gdown
from datetime import datetime
from extraction import Extrac     
from flask import Flask, jsonify, request

app = Flask(__name__)

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
                print(filename)
                pdf_path = os.path.join(pdf_folder, filename)
                text = Extrac.extract_text_from_pdf(pdf_path)
                emails, phones = Extrac.extract_email_and_phone(text)
                print(text)
                print(emails)
                print(phones)
                results.append({
                    "filename": filename,
                    "emails": emails,
                    "phones": phones
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