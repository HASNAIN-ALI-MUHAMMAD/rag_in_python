import asyncio
from src.db.postgres import PostgresDB
from src.llm.gemini import LLMGemini


async def main():
    llm = LLMGemini()
    db = PostgresDB()
    await db.connect()

    pr = input("enter your prompt: ")
    response = llm.generate_text(pr)
    print("LLM Response:", response)


if __name__ == "__main__":
    asyncio.run(main())