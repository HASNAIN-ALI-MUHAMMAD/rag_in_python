import asyncio
from src.db.postgres import PostgresDB
from src.llm.gemini import LLMGemini
from src.db.vmongo import VMongo
from filehandling.file_reader import FIleReader

async def main():
    # llm = LLMGemini()
    # mgdb = VMongo("python_dbf","files","pydbf_index1")
    # mgdb.close()


    ## postgres example
    # db = PostgresDB()
    # await db.connect()

    ## Example usage of LLMGemini
    # pr = input("enter your prompt: ")
    # embeddings = llm.embed_text(pr)/
    # print("Embeddings:", embeddings)
    # response = llm.generate_text(pr)
    # print("LLM Response:", response)

    fr = FIleReader()
    f = input("Enter filename to read: ")
    f_d = fr.read(f)
    print(f"file: {f_d}")


if __name__ == "__main__":
    asyncio.run(main())