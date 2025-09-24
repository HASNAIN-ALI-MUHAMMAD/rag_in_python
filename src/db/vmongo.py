import time
from pymongo.mongo_client import MongoClient as mc
from pymongo.server_api import ServerApi
from pymongo.operations import SearchIndexModel
from src.envs import Env

class VMongo:
    def __init__(self, db_name: str,coll_name:str,searhch_index_name:str="vector_index"):
        uri = Env.get("MONGO_URI",default="blah_blah") 
        self.client = mc(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.coll = self._create_collection(coll_name)
        self._create_search_index(searhch_index_name)
    
    def _create_search_index(self,index_name:str="vector_index",):
        ifIndex = self.coll.list_search_indexes().to_list()
        if len(ifIndex) != 0:
            if (ifIndex[0].get("name")==index_name) and ifIndex[0].get("queryable") is True:
                print(f"Search index {index_name} already exists and is ready for querying.")
                return
        index_model = SearchIndexModel(
            definition={
            "fields":[
                {
                    "type": "vector",
                    "path": "vectors",
                    "numDimensions": 1536,
                    "similarity": "dotProduct",
                    "quantization": "scalar"
                },
                {
                    "type" :"filter",
                    "path" :"path"
                },
                {
                    "type":"filter",
                    "path" : "filename"
                }
            ]
            },
            name=index_name,
            type="vectorSearch"
        )

        result = self.coll.create_search_index(index_model)
        print("New search index named " + result + " is building.")
        print("Polling to check if the index is ready. This may take up to a minute.")
        predicate=None
        if predicate is None:
            predicate = lambda index: index.get("queryable") is True
        while True:
            indices = list(self.coll.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(2)
        print(result + " is ready for querying.")


    def _create_collection(self,coll_name: str):
        if coll_name in self.db.list_collection_names():
            return self.db[coll_name]
        return self.db.create_collection(coll_name)

    def post_vector(self,vector_data: dict):
        self.coll.insert_many([vector_data])        
        return

    def close(self):
        self.client.close()
    
    