# Aqui se encontrarán configuraciones que se aplicarán al chat

# Librerias
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, field


# Clase padre de JsonInitConfig
class JsonInit(ABC):

    # Convierte todos los atributos de las clases hijas en diccionarios
    # excluyendo los metadata={"exclude": True}
    # Key = nombre de la varible
    # Value = valor de la variable
    def set_content(self) -> dict:
        # Convierte atributos de dataclass a diccionario excluyendo los marcados con exclude=True
        result = {}
        for f in fields(self):
            if not f.metadata.get("exclude", False):
                result[f.name] = getattr(self, f.name)
        return result

    # Comprueba si el file o no existe o está vacío
    def empty_validate(self, file : str) -> dict | None:
        if not os.path.exists(file):
            return None
        try:
            with open(file, "r") as json_file:
                data = json.load(json_file)
                return data if data else None
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    # Incializa el json con valores por defecto
    def init_default(self) -> bool:
        # Inicializa el archivo con valores por defecto si está vacío o no existe
        data = self.empty_validate(self.file)
        if not data:
            with open(self.file, "w") as json_file:
                json.dump([self.set_content()], json_file, indent=4)
            return True
        return False
    
    def crear_default(self, config_list: list) -> bool:
        # validar que el agente no exista
        pass 

    @abstractmethod
    def initialize(self):
        pass


# Inicializar json de configuracion
# si esta vacia y fue inicializado correctamente = True
# si el diccionario no estaba vacío = False
@dataclass
class JsonInitConfig(JsonInit) :
    temperature: float = 1.0
    max_tokens: int = 350
    presence_penalty: float = 0.4
    frequency_penalty: float = 0.4
    name : str = "new chat"
    file: str = field(default="config.json", metadata={"exclude": True})

    def initialize(self):
        return self.init_default()

    def crear(self, config_list: list) :
        return self.crear_default(config_list=config_list)
    

# Inicializar json de Memoria corta
# si esta vacia y fue inicializado correctamente = True
# si el diccionario no estaba vacío = False
@dataclass
class JsonInitShortMemory(JsonInit):
    role: str ="system"
    content: str ="Un asistente amigable que busca ayudar al resto"
    file: str = field(default="memory.json", metadata={"exclude": True})

    def initialize(self):
        return self.init_default()


# Clase base
class JsonInit(ABC):

    def set_content(self) -> dict:
        # Convierte atributos de dataclass a diccionario, excluyendo los con metadata exclude=True
        result = {}
        for f in fields(self):
            if not f.metadata.get("exclude", False):
                result[f.name] = getattr(self, f.name)
        return result

    def empty_validate(self, file: str) -> dict | None:
        # Comprueba si el archivo no existe o está vacío
        if not os.path.exists(file):
            return None
        try:
            with open(file, "r") as json_file:
                data = json.load(json_file)
                return data if data else None
        except (json.JSONDecodeError, FileNotFoundError):
            return None

    @abstractmethod
    def initialize(self):
        pass


@dataclass
class JsonInitConfig(JsonInit):
    temperature: float = 1.0
    max_tokens: int = 350
    max_input_tokens: int = 400
    presence_penalty: float = 0.4
    frequency_penalty: float = 0.4
    model: str = "gpt-4o-mini"
    tokens: int = 0
    name: str = "new chat"
    role: str = "system"
    content: str = "Un asistente amigable que busca ayudar al resto"
    file: str = field(default="data.json", metadata={"exclude": True})

    def initialize(self):
        # Inicializa un solo JSON con las configuraciones
        data = self.empty_validate(self.file)

        # Si no existe o está vacío, lo crea con todo el contenido
        if not data:
            structure = [
                {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "max_input_tokens": self.max_input_tokens,
                    "presence_penalty": self.presence_penalty,
                    "frequency_penalty": self.frequency_penalty,
                    "model": self.model,
                    "tokens": self.tokens,
                    "name": self.name,
                    "memory": [{
                        "role": self.role,
                        "content": self.content
                    }]
                }
            ]
            with open(self.file, "w") as json_file:
                json.dump(structure, json_file, indent=4)
            return True

        return False
    
    def crear(self, config_list : list[dict]):
        data = self.empty_validate(self.file)

        # Si no existe o está vacío, lo crea con todo el contenido
        if data:
            structure = {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "max_input_tokens": self.max_input_tokens,
                    "presence_penalty": self.presence_penalty,
                    "frequency_penalty": self.frequency_penalty,
                    "model": self.model,
                    "tokens": self.tokens,
                    "name": self.name,
                    "memory": [{
                        "role": self.role,
                        "content": self.content
                    }]
                }

            config_list.append(structure)

            with open(self.file, "w") as json_file:
                json.dump(config_list, json_file, indent=4)
            return True
        
        return False
    
class JsonCreateConfig(JsonInit):
    pass

"""if __name__ == "__main__":
    g = JsonInitConfig()
    print(g.initialize())"""


if __name__ == "__main__":
   
   sett = [
    {
        "temperature": 1.0,
        "max_tokens": 350,
        "presence_penalty": 0.4,
        "frequency_penalty": 0.4,
        "name": "hector",
        "memory": {
            "rol": "system",
            "content": "es mi amigable"
        }
    }
]
   
   config = JsonInitConfig(file="config.json")

   config_created = config.crear(config_list=sett)

   print("Archivo de configuración creado:", config_created)