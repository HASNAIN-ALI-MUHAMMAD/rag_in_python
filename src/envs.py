import os
from dotenv import load_dotenv

class Env:
    _loaded = False

    @classmethod 
    def load(cls):
        if not cls._loaded:
            load_dotenv()
            cls._loaded = True
    
    @classmethod
    def get(cls,key:str,default=None):
        cls.load()
        return os.getenv(key,default)
    

