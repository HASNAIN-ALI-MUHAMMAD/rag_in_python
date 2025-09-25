from pathlib import Path


class FIleSearcher:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def search_files(self, query: str):
        matched_files = []
        for file_path in self.directory.rglob('*'):
            if file_path.is_file() and query.lower() in file_path.name.lower():
                matched_files.append(file_path)
        return matched_files
    

    def get_user(home_dir:str="home") -> str:
        dirs = Path(f"/{home_dir}").iterdir()
        users = [d.name for d in dirs if d.is_dir()]
        return users
    

if __name__ == "__main__":
    # fs = FIleSearcher("/D")
    # query = input("Enter search query: ")
    # results = fs.search_files(query)
    # if results:
    #     print("Matched files:")
    #     for file in results:
    #         print(file)
    # else:
    #     print("No files matched the query.")