from src.filehandling.file_searcher import FIleSearcher
from src.filehandling.file_reader import FIleReader
from src.filehandling.splitter import TextSplitter
from src.db.vmongo import VMongoFiles

class MainHelp:
    def __init__(self):
        self.fs = FIleSearcher()
        self.fr = FIleReader()
        self.ts = TextSplitter()

    def file_search_chunking(self) -> list:

        print("Instructions: Provide the filepath(complete) or filename(Could be COMPLETE or *.{ext} or {name}.*).")
        filename = input("Enter the filename/path: ")
        print("Instructions: Provide the search directory in the '/home/{user}/**' dir. Default shall be '/home/{user}")
        search_dir = input("Enter the directory: ")


        ## files for the given filename and dir
        files = self.fs.search_files(filename,search_dir)

        if len(files) == 0:
            print("No files found. Exiting.")
            return
        elif len(files) == 1:
            print(f"One file found: {files[0].get('path')}")
            file_selection = '1'
        else:
            print(f"Found {len(files)} files.")
            for i,f in enumerate(files):
                print(f"{i+1}. {f.get('path')}")

            file_selection = input("Select a file by number to read (or 'q' to quit): ")
            if file_selection.lower() == 'q':
                print("Exiting.")
                return
            elif int(file_selection) not in range(1,len(files)+1):
                print("Invalid selection. Exiting.")
                return
        
        selected_file = files[int(file_selection)-1]
        print(f"Selected file: {selected_file.get('path')}")

        print("Reading file...")
        file_content = self.fr.read(selected_file.get("path"),selected_file.get("ext"))
        print(f"File content read. Length: {len(file_content.split('\n'))} lines.")

        ## chunking
        file_metadata = {
            "filename":filename,
            "path":selected_file.get("path"),
            "type":selected_file.get("ext")
        }
        file_chunks:list = self.ts.create_chunks(file_content,file_metadata)
        print(f"File chunking completed. Total chunks created: {len(file_chunks)}") 
        
        return file_chunks
    
    def vector_upload(self,file_chunks:list):
        vm = VMongoFiles()
        print("Uploading file chunks to the database...")
        upload_ids:list = vm.post_vector(file_chunks)
        vm.close()
        print("File chunks uploaded to the database.")
        return upload_ids

    def postgres_update(self,file_data:dict,ids:list):
        return