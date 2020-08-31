import os
import requests
import json

class MUPU:
    def __init__(self):
        self.game_path = "all-over-the-universe/"
        self.check_game_folder()
        if self.check_newer_version() == "true":
            print("Found newer version updating now")
            self.update_files(self.get_file_dict())
            self.update_version_file(self.get_newest_version())
            print("Update successfull starting game")
            self.start_game()
        else:
            print("Already on newest version starting game")
            self.start_game()
    
    def start_game(self):
        os.system(os.path.abspath(os.getcwd())+"/"+self.game_path+"AllOverTheUniverse.exe")
    
    def get_newest_version(self):
        r = requests.get("http://152.89.239.144:8080/api/get_newest_version/")
        return r.text

    def update_version_file(self, new_version):
        with open("version.txt", "w") as f:
            f.write(new_version)

    def update_files(self, file_dict):
        for key, value in file_dict.items():
            print("Writing file: "+key)
            r = requests.get("http://152.89.239.144/"+value)
            self.create_folders(os.path.dirname(self.game_path+key))
            open(self.game_path+key, "wb").write(r.content)
    
    def create_folders(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def check_game_folder(self):
        if os.path.exists(self.game_path):
            return
        os.mkdir(self.game_path)

    def get_file_dict(self):
        r = requests.get("http://152.89.239.144:8080/api/compare/", params={"version": self.get_version()})
        return json.loads(r.text)
        
    def check_newer_version(self):
        r = requests.get('http://152.89.239.144:8080/api/newer_version_availible/', params={"version": self.get_version()})
        return r.text

    def get_version(self):
        if os.path.exists("version.txt"):
            with open("version.txt", "r") as f:
                return float(f.read())
        else:
            return 0

if __name__ == "__main__":
    mupu = MUPU()