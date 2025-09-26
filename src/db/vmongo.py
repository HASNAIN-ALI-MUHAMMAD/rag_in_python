import time
from pymongo.mongo_client import MongoClient as mc
from pymongo.server_api import ServerApi
from pymongo.operations import SearchIndexModel
from src.envs import Env

class VMongoFiles:

    def __init__(self, db_name: str = Env.get("DB_MON_NAME"),coll_name:str = Env.get("COLL_NAME_FILES"),search_index_name:str=Env.get("SEARCH_INDEX_NAME_FILES")):
        uri = Env.get("MONGO_URI",default="blah_blah") 
        self.client = mc(uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.coll = self._create_collection(coll_name)
        self._create_search_index(search_index_name)
    
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
                    "type":"filter",
                    "path":"metadata.path",
                },
                {   
                    "type":"filter",
                    "path":"metadata.filename",
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
        tries=0
        isready = None
        while tries<5:
            indices = list(self.coll.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                isready = True
                break
            time.sleep(5)
            tries+=1
        if isready:
            print(result + " is ready for querying.")
        else:
            print(f"Error while creating index.\n{result}")
    def _create_collection(self,coll_name: str):
        if coll_name in self.db.list_collection_names():
            return self.db[coll_name]
        return self.db.create_collection(coll_name)

    def post_vector(self,vector_data: list[dict]):
        try:
            vcs = self.coll.insert_many(vector_data)        
            return vcs.inserted_ids
        except Exception as e:
            print(f"Error while uploading vectors.\n {e}")

    def search_vector(self,query:list,filename:str,path:str)->list:
        try:
            pipeline = [
                {
                    "$vectorSearch":{
                        "index":Env.get("SEARCH_INDEX_NAME"),
                        "path":"vectors",
                        "queryVector":query,
                        "numCandidates":200,
                        "limit":10,
                        "filter":{"metadata.path":path,"metadata.filename":filename}
                    }
                },
                {
                    "$project":{
                        "_id":0,
                        "text":1,
                        "metadata":1,
                        "score":{"$meta":"vectorSearchScore"}
                    }
                }
            ]
            results = list(self.coll.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Error while searching.\n{e}")
            return
            
    def delete_entry(self,filename:str,path:str):
        try:
            self.coll.delete_many({"filename":filename,"path":path})
            print("Deletion was successful.")
        except Exception as e:
            print(f"Error while deleting.\n{e}")

    def _drop_index(self,index):
        try:
            self.coll.drop_search_index(index)
            print("Dropping index...")
            time.sleep(20)
            print("Index dropped!")
            return
        except Exception as e:
            print(f"Error:{e}")
            return


    def close(self):
        self.client.close()
    
    

class VMongoConvos(VMongoFiles):
    def __init__(self, db_name = Env.get("DB_MON_NAME"), coll_name = Env.get("COLL_NAME_CONVOS"), search_index_name = Env.get("SEARCH_INDEX_NAME_CONVOS")):
        super().__init__(db_name, coll_name, search_index_name)

    def _create_search_index(self, index_name = "vector_index"):
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
                    "type":"filter",
                    "path":"filename",
                },
                {   
                    "type":"filter",
                    "path":"path",
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
        tries=0
        isready = False
        while tries<5:
            indices = list(self.coll.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                isready = True
                break
            time.sleep(7)
            tries+=1
        if isready==True:
            print(result + " is ready for querying.")
        elif not isready:
            print(f"Error while creating index: {result}")

