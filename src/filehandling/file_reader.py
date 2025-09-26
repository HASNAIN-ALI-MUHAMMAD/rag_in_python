from docx import Document
from pypdf import PdfReader


class FIleReader:

    def read(self,filepath:str,ext:str)->str:
        PLAIN_EXTS = ['txt','md','log','py','js','html','css','java',"env","json","c","c*","js*","ts*"]

        if ext in PLAIN_EXTS:
            return self.read_plain(filepath)
        elif ext == 'pdf':
            return self.read_pdf(filepath)
        elif ext == 'docx':
            return self.read_docx(filepath)
        else:
            print(f"Error:Unsupported file extension: {ext}")
            # raise ValueError(f"Unsupported file extension: {ext}")
    

    ## diff file readers ... fro each extension/type
    def read_plain(self,file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                text = ""
                for l in lines:
                    if l.strip() != "" and l is not None:
                        text += l
                return text
        except Exception as e:
            print(f"Error reading plain text file:\n{e}")
            return e

    def read_pdf(self,file_path: str) -> str:
        try: 
            reader = PdfReader(file_path)
            text = ''
            for page in reader.pages:
                if page.extract_text() is not None and page.extract_text() != "":
                    text += page.extract_text() + '\n'
            return text
        except Exception as e:
            print(f"Error reading PDF file.\n{e}")
            return e

    def read_docx(self,file_path: str) -> str:
        try:
            doc = Document(file_path)
            text = ''
            for para in doc.paragraphs:
                if para.text != "" and para.text is not None:
                    text += para.text + '\n'
            return text
        except Exception as e:
            print(f"Error reading DOCX file.\n{e}")
            return e
        

if __name__ == "__main__":
    exit()