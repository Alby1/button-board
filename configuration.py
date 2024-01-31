import json

class Configuration():
    def read_file(self, filename):
        combinations = {}
        plugins = {}
        with open(filename, 'r') as f:
            read = json.loads(f.read())
            try:
                combinations = read['combinations']
                plugins = read['plugins']
            except:
                return None, None
        
        return combinations, plugins
            