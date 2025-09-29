# Aqui se encontrarán configuraciones que se aplicarán al chat

# Librerias
import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field


# Clase padre de JsonInitConfig
class JsonInit(ABC):

    # Convierte todos los atributos de las clases hijas en diccionarios
    # excluyendo los metadata={"exclude": True}
    # Key = nombre de la varible
    # Value = valor de la variable
    def set_content(self):
        data = asdict(self)

        # Quita cualquier campo marcado como exclude
        return {k: v for k, v in data.items() if not self.__dataclass_fields__[k].metadata.get("exclude", False)}
    
    # Comprueba si el file o no existe o está vacío
    def empty_validate(self, file):
        if os.path.exists(file):
            with open(file, "r") as json_file:
                try:
                    json.load(json_file)
                except json.JSONDecodeError:
                    return None

        else:
            return None

    @abstractmethod
    def init_default(self):
        pass


# Inicializar json de configuracion
# si esta vacia y fue inicializado correctamente = True
# si el diccionario no estaba vacío = False
@dataclass
class JsonInitConfig(JsonInit) :
    temperature: float = 1.0
    max_tokens: int = 350
    presece_penalty: float = 0.4
    frequency_penalty: float = 0.4
    file: str = field(default="config.json", metadata={"exclude": True})


    # Incializa el json con valores por defecto
    def init_default(self):

        # Comprueba si el file o no existe o está vacío
        data = self.empty_validate(self.file)

        # Si el file está vacío le pone los datos por defecto
        if not data:
            with open(self.file, "w") as json_file:
                json.dump(self.set_content(), json_file, indent=4)
            return True
        else:
            return False


# Inicializar json de Memoria corta
# si esta vacia y fue inicializado correctamente = True
# si el diccionario no estaba vacío = False
@dataclass
class JsonInitShortMemory(JsonInit):
    role: str ="system"
    content: str ="Un asistente amigable que busca ayudar al resto"
    file: str = field(default="memory.json", metadata={"exclude": True})

    def init_default(self):

        # Comprueba si el file o no existe o está vacío
        data = self.empty_validate(self.file)

        # Si el file está vacío le pone los datos por defecto
        if not data:
            with open(self.file, "w") as json_file:
                json.dump(self.set_content(), json_file, indent=4)
            return True
        else:
            return False
        

dd = JsonInitShortMemory()
print(dd.init_default())