import asyncio
from src.db.postgres import PostgresDB
from src.llm.gemini import LLMGemini
from src.db.vmongo import VMongoFiles
from src.db.vmongo import VMongoConvos

from src.help_main import MainHelp
from src.envs import Env


async def main():
    # db =PostgresDB()
    # db_conn = await db.connect()
    # mn = MainHelp()
    # llm = LLMGemini()
    # mgdb = VMongoFiles()
    mgdb2 = VMongoConvos()
    # mgdb2._drop_index(Env.get("SEARCH_INDEX_NAME_CONVOS"))
    mgdb2.close()
    # res =  mgdb.search_vector(llm.embed_text("What is the significance of this paper."),".pdf","/home/hasnain/D/docs/pdfs/McCulloch.and.Pitts.pdf")
    # for r in res:
    #     print(f"{r["metadata"]["path"]} || {r["metadata"]["chunk_index"]} || {r["metadata"]["chunk_size"]} || {r["score"]}")

    # await db.create_table_files(db_conn)
    # await db.insert_table_files(db_conn,"test","test","test",["23","232"])
    # files = await db.select_table_files(db_conn)
    # print("Fetched files.")
    # for f in files:
    #     print(dict(f))
    # await db.create_table_convos(db_conn)


    # file_chunks=  mn.file_search_chunking()
    # if file_chunks:
    #     ids = mn.vector_upload(file_chunks)
    
    # if file_chunks is not None:
    #     mn.postgres_update(file_chunks["metadata"],ids)




if __name__ == "__main__":
    asyncio.run(main())