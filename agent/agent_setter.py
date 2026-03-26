from abc import ABC, abstractmethod

# Clase hija de los parametros de configuración
class Setter(ABC):
    
    @abstractmethod
    def set(self, data) -> dict:
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