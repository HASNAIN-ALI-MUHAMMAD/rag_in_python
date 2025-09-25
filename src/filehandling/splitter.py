import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.llm.gemini import LLMGemini



class TextSplitter:
    def __init__(self,chunk_size=2500,chunk_overlap=500):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def split_text(self,text:str)->list[str]:
        return self.splitter.split_text(text)
    
    def create_embeddings(self,text:str):
        llm = LLMGemini()
        embd = llm.embed_text(text)
        time.sleep(0.2)
        return embd

    def create_chunks(self,text:str,file_metadata:dict)->list[dict]:
        texts = self.split_text(text)
        arr = []
        for i,t in enumerate(texts):
            obj = {
                "text": t,
                "vectors": self.create_embeddings(t),
                "metadata": {
                    "filename": file_metadata.get("filename","unknown"),
                    "path": file_metadata.get("path","unknown"),
                    "type": file_metadata.get("type","unknown"),
                    "chunk_size": len(t),
                    "chunk_index": i+1
                }
            }
            arr.append(obj)
        return arr




###### sample usage and testing..
# if __name__ == "__main__":
#     ts = TextSplitter()
#     text = "This is a sample text. " * 200  # Sample text for demonstration
#     chunks = ts.split_text(text)
#     for i, chunk in enumerate(chunks):
#         print(f"Chunk {i+1}:\n{chunk}\n and length: {len(chunk)}\n")
#     print(f"Total chunks created: {len(chunks)}")
#     print("Text splitting completed.")
