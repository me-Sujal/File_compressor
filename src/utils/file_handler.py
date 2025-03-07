class FileHandler:
    @staticmethod
    def read_text(filepath):
        with open(filepath, 'r') as f:
            return f.read()
        
    @staticmethod
    def write_text(filepath, data):
        with open(filepath, 'w') as f:
            f.write(data)    
            
    @staticmethod
    def write_binary(filepath, data):
        with open(filepath, 'wb') as f:
            f.write(data)
