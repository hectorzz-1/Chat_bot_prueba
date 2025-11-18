# Estarán las clases con las que se configurará el chat y sus respuestas

# Librerias
import json, os
from abc import ABC, abstractmethod

# Clase hija de los parametros de configuración
class Setter(ABC):
    
    @abstractmethod
    def set(self, data) -> dict:
        pass
    

# clase padre de la clase
# JsonSettingsRepository
class ISettingsRepository(ABC):
    @abstractmethod
    def load(self) -> dict:
        pass

    @abstractmethod
    def save(self, data: dict):
        pass


# Obtener la temperatura
class TemperaturaSetter(Setter):

    def set(self,data: float):
        return {"temperature" : data}
    

# Obtener la cantidad de tokens que se podrán usar
class MaxTokensSetter(Setter):

    def set(self,data : int):
        return {"max_tokens" : data}
    

# Obtener la penalidad por repetir siempre el tema
class PresencePenaltySetter(Setter):

    def set(self,data : float):
        return {"presence_penalty" : data}
    

# Obtener la penalidad por repetir palabras
class FrequencyPenaltySetter(Setter):

    def set(self,data : float):
        return {"frequency_penalty" : data}
    

# Obtener la modelo de IA
class ModelSetter(Setter):

    def set(self,data : str):
        return {"model" : data}
    

# Obtener el nombre
class NameSetter(Setter):

    def set(self,data : str):
        return {"name" : data}
    

# colocar un comportamiento
class BehaviorSetter(Setter):

    def set(self,data : str):
        return {"memory": [{
            "role": "system",
            "content": data
        }]}
    
# Colocará una instruccion en el comportamiento del agente
# esta siempre irá antes del comportamiento que el usuario
# le haya dado.
# entre la instruccion y el comportamiento habrá un ; para poder
# manejar mejor cual es cual en un futuro.
class InstructionSetter:

    def set(self,agent: dict, inst : str = ""):
        behavior = agent["memory"][0]["content"]
        agent["memory"][0]["content"] = inst+ " ; "+behavior
        return agent



# Clase hija de ISettingsRepository
# Tiene 2 funciones load y save
# La utilidad es guardar y cargar archivos
class JsonSettingsRepository(ISettingsRepository):
    def __init__(self, file: str):
        self.file = file

    # Carga archivos y 
    # si no exiten retorna False
    # se pudo cargar normal retorna el json
    def load(self) -> dict:
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return False
        return False
    
    # Guarda actualiza los datos de un archivo
    # se le tiene que pasar el argumento data(Los datos a actualizar)
    def save(self, data: list):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)


class SaveSettingChat:
    def __init__(self, repository: ISettingsRepository, chat: str):
        self.repository = repository
        self.chat = chat
        self.settings = {}

    # 
    def add(self, setter: Setter, value):
        self.settings.update(setter.set(value))

    # Retorna las configuraciones
    def get_settings(self):
        return self.settings

    # Esta funcion guarda las configuraciones
    # si el file no existia o estaba vacio retorna False
    def save(self):
        data = self.repository.load()
        if data == False:
            return False

        # Buscar el índice del chat en la lista
        for i, chat in enumerate(data):
            if chat.get("name") == self.chat:
                data[i].update(self.settings)
                break

        # Guardar la lista completa
        self.repository.save(data)
        return True



if __name__ == "__main__":
    
    name = "new chat"
    jsr = JsonSettingsRepository("config.json")
    ffj = SaveSettingChat(jsr, name)

    setter = BehaviorSetter()
    setter_dos = FrequencyPenaltySetter()
    name = NameSetter()

    ffj.add(setter=name,value="hola")

    print(ffj.save())