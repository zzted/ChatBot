class DataFile:
    def __init__(self):
        self.text = None

    def read(self, file_path: str):
        f = open(file_path, 'r')
        file_content = f.read()
        self.text = file_content.splitlines()

