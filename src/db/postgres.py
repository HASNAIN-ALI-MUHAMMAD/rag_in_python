import asyncpg
import time
from ..envs import Env


class PostgresDB:
    def __init__(self):
        self.db_user = Env.get('DB_USER','postgres')
        self.db_password = Env.get('DB_PASSWORD','password')
        self.db_name = Env.get('DB_NAME','postgres')

        self.db_host = Env.get('DB_HOST','localhost')
        self.db_port = int(Env.get('DB_PORT',5432))
    
    async def connect(self):
        try:
            print("Connecting to the database...")
            time.sleep(1.1)
            db = await asyncpg.connect(
                user=self.db_user,
                password=  self.db_password,
                database=self.db_name,
                host = self.db_host,
                port= self.db_port
            )
            print("Database connection established")
            return db
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise e
        
    async def create_table_files(self,db):
        try: 
            await db.execute("""
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                CREATE TABLE IF NOT EXISTS files(
                    file_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    filename VARCHAR(50) NOT NULL,
                    path VARCHAR(200) NOT NULL,
                    extension VARCHAR(20),
                    record_date TIMESTAMP DEFAULT NOW(),
                    chunk_ids TEXT[] NOT NULL
                )"""
            )
            return True
        except Exception as e:
            print(f"Table not created.\n{e}")
            return False
    
    async def insert_table_files(self,db,filename:str,path:str,ext:str,chunks:list):
        try: 
            await db.execute("""
                INSERT INTO files (filename,path,extension,chunk_ids)
                VALUES ($1,$2,$3,$4)
            """,filename,path,ext,chunks
            )
            return True
        except Exception as e:
            print(f"Error while inserting into *files*.\n{e}")
            return False
        
    async def select_table_files(self,db)->list:
        try: 
            rows = await db.fetch("""
                SELECT * FROM files
            """)
            return rows
        except Exception as e:
            print(f"Error while inserting into *files*.\n{e}")
            return None
        
    async def create_table_convos(self,db):
        try:
            await db.execute("""
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                CREATE TABLE IF NOT EXISTS conversations(
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    query TEXT,
                    response TEXT,
                    retreived_docs JSONB,
                    file_id UUID REFERENCES files(file_id) ON DELETE SET NULL
                );
        """)
            return True
        except Exception as e:
            print(f"Table not created.\n{e}")
            return False
        
    async def insert_table_convos(self,db,query:str,res:str,r_docs:dict):
        try:
            await db.execute("""
                INSERT INTO conversations (query,response,retreived_docs)
                VALUES ($1,$2,$3);
            """,query,res,r_docs)
            return True
        except Exception as e:
            print(f"Error inserting into *convesations*: {e}")
            return False
        
    async def select_table_convos(self,db):
        try:
            rows = await db.execute("""
                SELECT * FROM conversations
            """)
            return True
        except Exception as e:
            return

    async def drop_table(self,db,table:str):
        try:
            await db.execute(f"""
                DROP TABLE IF EXISTS {table};
        """)
            print(f"{table} dropped!")
        except Exception as e:
            print(f"Error: {e}")
