import requests
import json
import os

CONFIG_URL = "https://gist.githubusercontent.com/JesusMFVivero/77003ea5e3df702410234a8c991cbbc5/raw/tons-config.json"
TOKEN_FILE = "tons_token.json"

class APIClient:
    def __init__(self):
        self.BASE_URL = self.get_server_url()
        self.token = None
    
    @staticmethod
    def get_server_url():
        try:
            r = requests.get(CONFIG_URL, timeout=5)
            cfg = r.json()
            ip = cfg["ip"]
            port = cfg["port"]
            return f"http://{ip}:{port}"
        except Exception as e:
            print(f"Error getting config: {e}")
            return "http://127.0.0.1:5000"
    
    def save_token(self, token):
        with open(TOKEN_FILE, 'w') as f:
            json.dump({"token": token}, f)
        self.token = token
    
    def load_token(self):
        try:
            if os.path.exists(TOKEN_FILE):
                with open(TOKEN_FILE, 'r') as f:
                    data = json.load(f)
                    self.token = data.get("token")
                    return True
        except:
            pass
        return False
    
    def clear_token(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.token = None
