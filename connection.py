# Se establecerán las conexiones

# Librerias
import os
from openai import OpenAI


# Conectar el cerebro de OpenAI
class ConnectBrain :
    
    def __init__(self, key=os.getenv("API_KEY_OPENAI")):
        self.key = key


    def connect(self):
        return OpenAI(self.key)