import os
from docx import Document
from pypdf import PdfReader
from file_searcher import FIleSearcher


class FIleReader:

    def read(self,filepath:str,ext:str)->str:
        PLAIN_EXTS = ['txt','md','log','py','js','html','css','java',"env"]
        # file_path = os.path.join("/home/hasnain/D/code/python/rag_pj",filename)

        print(f"File to read: {filepath}")
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
                return file.read()
        except Exception as e:
            print(f"Error reading plain text file:\n{e}")
            return e

    def read_pdf(self,file_path: str) -> str:
        try: 
            reader = PdfReader(file_path)
            text = ''
            for page in reader.pages:
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
                if para.text != "":
                    text += para.text + '\n'
            return text
        except Exception as e:
            print(f"Error reading DOCX file.\n{e}")
            return e
        

if __name__ == "__main__":
    fs =FIleSearcher()
    filename = input("Enter filename to search: ")
    dir = input("Enter directory to search in (or leave blank for '/home/{user}/*'): ")
    print(f"Searching files...\nFilename: {filename} ||     Dir: {dir}\n")
    files= fs.search_files(filename,dir)
    print(f"Found {len(files)} files.")
    print(files)

    if len(files) == 0:
        exit(0)
    filepath = files[0].get("path")
    fr = FIleReader()
    pdf  = fr.read(filepath,files[0].get("ext"))
    print(pdf.split("\n")[0:100])