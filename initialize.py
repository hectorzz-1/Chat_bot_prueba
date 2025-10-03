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
                json.dump(self.set_content(), json_file, indent=4)
            return True
        return False

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
    file: str = field(default="config.json", metadata={"exclude": True})

    def initialize(self):
        return self.init_default()        


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