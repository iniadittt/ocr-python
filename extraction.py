import pytesseract
import pdf2image
import re

class Extrac:
    @staticmethod
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

    @staticmethod
    def extract_email_and_phone(text):
        email_pattern = r'[a-zA-Z0-9._%+-]+\s*[a-zA-Z0-9._%+-]*\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*(?:[a-zA-Z]{2,}|ac\.id|co\.id|go\.id|org\.id|net\.id|sch\.id|mil\.id|info|biz|xyz|me|online|tech|store|site|cloud)'
        phone_pattern = r'\b(?:\+?62|62|08)\d{2,3}[-\s]?\d{3,4}[-\s]?\d{3,4}\b'
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        cleaned_emails = [re.sub(r'\s*@\s*', '@', email) for email in emails]
        return cleaned_emails, phones
