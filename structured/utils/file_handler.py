# io/file_handler.py
class FileHandler:
    @staticmethod
    def read_text(filepath):
        with open(filepath, 'r') as f:
            return f.read()
            
    @staticmethod 
    def write_text(filepath, content):
        with open(filepath, 'w') as f:
            f.write(content)

    @staticmethod
    def write_binary(filepath, bytes_data):
        with open(filepath, 'wb') as f:
            f.write(bytes_data)

    @staticmethod
    def read_binary(filepath):
        with open(filepath, 'rb') as f:
            return f.read()
