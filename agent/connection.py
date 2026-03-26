# Librerias
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv


# Conectar el cerebro de OpenAI
class ConnectBrain :
    
    def __init__(self, env_key: str):
        # obtenemos la clave
        api_key =  os.getenv(env_key)

        # Validamos que si la haya encontrado
        if not api_key:
            raise ValueError(f"{env_key} not found")
        
        # Variable privada con la instancia de la api
        self._client = OpenAI(api_key=api_key)

    # Retornamos la instancia de la api
    def get_client(self):
        return self._client

    
if __name__ == "__main__":
    c = ConnectBrain()
    print(c.get_client())