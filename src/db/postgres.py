import asyncpg
import time
from ..envs import Env


class PostgresDB:
    db_user:str
    db_password:str
    db_name:str
    db_host:str
    db_port:int

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
            self.name = await asyncpg.connect(
            user=self.db_user,
            password=  self.db_password,
            database=self.db_name,
            host = self.db_host,
            port= self.db_port
            )
            print("Database connection established")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise e


