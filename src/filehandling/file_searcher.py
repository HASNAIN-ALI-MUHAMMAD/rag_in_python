from pathlib import Path


class FIleSearcher:


    def extract_ext(self,filename:str)->str:
        return filename.split('.')[-1].lower()

    def search_files(self, filename: str ,dir:str = ""):
        if filename.startswith("*"):
            return self.search_globs(filename,dir)
        dir_path = Path("/home",str(self.get_user()),dir)

        matched_files = []
        for path in dir_path.rglob('*'):
            if path.is_file() and path.name == filename and filename.startswith("*") is False:
                matched_files.append({
                    "path" : str(path),
                    "ext":self.extract_ext(path.name),
                    "filename":path.name or filename
                    })
        return matched_files
    
    def search_globs(self, pattern: str ,dir:str = ""):
        dir_path = Path("/home",str(self.get_user()),dir)

        matched_files = []
        for path in dir_path.rglob(pattern):
            if path.is_file():
                matched_files.append({
                    "path" : str(path),
                    "ext":self.extract_ext(path.name),
                    "filename":path.name 
                    })
        return matched_files
    

    def get_user(self,home_dir:str="/home") -> str:
        dirs = Path(f"/{home_dir}").iterdir()
        users = [d.name for d in dirs if d.is_dir()]
        return users[0]
    


## test runs


# if __name__ == "__main__":
#     fs = FIleSearcher()
#     ddir = fs.search_files("test.c","D")
#     print(ddir)