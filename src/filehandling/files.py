import os
from docx import Document
from pypdf import PdfReader

class FIleReader:

    def read(self,filename:str)->str:
        PLAIN_EXTS = ['txt','md','log','py','js','html','css','java',"env"]
        ext = self.extract_ext(filename)
        file_path = os.path.join(os.getcwd(),filename)

        print(f"File to read: {filename} with extension: {ext} and path: {file_path}")
        if ext in PLAIN_EXTS:
            return self.read_plain(file_path)
        elif ext == 'pdf':
            return self.read_pdf(file_path)
        elif ext == 'docx':
            return self.read_docx(file_path)
        else:
            print(f"Error:Unsupported file extension: {ext}")
            # raise ValueError(f"Unsupported file extension: {ext}")
    
    def extract_ext(self,filename:str)->str:
        return filename.split('.')[-1].lower()

    def read_plain(self,file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading plain text file:\n{e}")
            return None

    def read_pdf(self,file_path: str) -> str:
        try: 
            reader = PdfReader(file_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
        except Exception as e:
            print(f"Error reading PDF file.\n{e}")
            return None

    def read_docx(self,file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = ''
            for para in doc.paragraphs:
                text += para.text + '\n'
            return text
        except Exception as e:
            print(f"Error reading DOCX file.\n{e}")
            return None