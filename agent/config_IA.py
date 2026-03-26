# Estarán las clases con las que se configurará el chat y sus respuestas

# Librerias
import json
from pathlib import Path


class LoadSettingsAgent:
    def __init__(self, file: Path):
        self.file = file
        
    # Carga archivos y 
    # si no exiten retorna un error
    # se pudo cargar normal retorna el json
    def load(self) -> dict:
        try:
            with open(self.file, "r") as f:
                # Retornamos el contenido del json 
                return json.load(f)
            
        # Si el json no existe
        except FileNotFoundError:
            return None
        # Si el json no es valido
        except json.JSONDecodeError:
            return None


# Actualiza las configuraciones y la guarda en el json
class SaveSettingsAgent:
    def __init__(self, file: Path, config_list: list[dict], agent_update: dict):
        self.file = file
        self.config_list = config_list
        self.agent_update = agent_update
    
    # Guarda actualiza los datos de un archivo
    # se le tiene que pasar el argumento data(Los datos a actualizar)
    def save(self):
        try:
            # Recorremos config_list hasta encontrar el indice del chat a actualizar
            for indice, agent_config in enumerate(self.config_list):
                if agent_config["id_chat"] == self.agent_update["id_chat"]:
                    # Actualizamos las configuraciones del agente
                    self.config_list[indice] = self.agent_update
        except KeyError:
            raise KeyError("key does not exist in dict. You most put a valid key")

        try:
            with open(self.file, "w") as f:
                # Actualizamos el json
                json.dump(self.config_list, f, indent=4)
        # Si el json no existe
        except FileNotFoundError:
            raise FileNotFoundError(f"{self.file} does not exist")
        # Si el json no es valido
        except json.JSONDecodeError:
            raise ValueError(f"{self.file} is not valid JSON")


# pide un diccionario y el atributo a cambiar.
# Lo que hace es que Actualiza el diccionario con el id dicho 
# y retorna el diccionario actualizado
class UpDateSettingDict:
    def __init__(self, config_agent: dict, attribute: dict):
        self.config_agent = config_agent
        if len(attribute) != 1:
            raise ValueError(f"atributte is not valid. You can only put dict with a single key.")
        self.attribute = attribute

    def update(self):
        try:
            # Actualiza el diccionario
            self.config_agent.update(self.attribute)
        except KeyError:
            raise KeyError("key does not exist in dict. You most put a valid key")

        # pasar el diccionario actualizada
        return self.config_agent


if __name__ == "__main__":

    list_c = [
  {
    "id_chat": "b15b4846-7c6d-41ed-80c8-01a47370f1a3",
    "temperature": 1.0,
    "max_tokens": 350,
    "max_input_tokens": 400,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.4,
    "model": "gpt-4o-mini",
    "tokens": 0,
    "name": "new chat",
    "memory": [
      {
        "role": "system",
        "content": "Un asistente amigable que busca ayudar al resto"
      }
    ]
  },
  {
    "id_chat": "cca168f0-8fd8-40e8-8683-7f8cb06219a1",
    "temperature": 1.0,
    "max_tokens": 350,
    "max_input_tokens": 400,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.4,
    "model": "gpt-4o-mini",
    "tokens": 0,
    "name": "dggddg",
    "memory": [
      {
        "role": "system",
        "content": "Un asistente amigable que busca ayudar al resto"
      }
    ]
  }
]
    dict_update= {
    "id_chat": "cca168f0-8fd8-40e8-8683-7f8cb06219a1",
    "temperature": 1.0,
    "max_tokens": 350,
    "max_input_tokens": 400,
    "presence_penalty": 0.4,
    "frequency_penalty": 0.4,
    "model": "gpt-4o-mini",
    "tokens": 0,
    "name": "dggddg",
    "memory": [
      {
        "role": "system",
        "content": "Un asistente amigable que busca ayudar al resto"
      }
    ]
  }
    file_path = "/home/hector/Escritorio/proyectos/IA/pruebas/mini_chat_bot/config/agents.json"

    d = UpDateSettingDict(config_agent=dict_update, attribute={"name": "Eduardo"}).update()
    a = SaveSettingsAgent(file=file_path,config_list=list_c,agent_update=d).save()

    print("d:", d)