from abc import ABC, abstractmethod
import json
import os

# clase que elimina el historico de la 
# conversación y solo deja el comportamiento
class ParleyForget:

    def __init__(self,agent: dict):
        self.agent = agent

    def delete(self):
        bahevior = self.agent["memory"][0]
        # cuando tiene una instruccion el separador es un ;.
        # con esto nos quedaremos con el comportamiento base sin 
        # ninguna instruccion solo lo que puso el user
        cut = bahevior["content"].split(";")
        bahevior["content"] = cut[-1]

        self.agent["memory"] = [bahevior]
        return self.agent
    

class Action(ABC):
    
    @abstractmethod
    def action(self):
        pass


# Guardará un archivo en un json
# si el json no existe lo creará
# y si existe lo sobre escribirá
class SaveJS(Action):

    def __init__(self, content, js_name: str):
        self.content = content
        self.js_name = js_name

    def action(self):
        try:
            with open(self.js_name, "w") as js_file:
                json.dump(self.content, js_file, indent=4)
        except Exception as e:
            return "Error: " + str(e)
        
        return True
    

# Elmina el contenido de un json
class DeleteJS(Action):

    def __init__(self, js_name: str):
        self.js_name = js_name

    def action(self):
        if not os.path.exists(self.js_name):
            return "El archivo no existe"

        try:
            os.remove(self.js_name)
            return "Archivo eliminado correctamente"
        except Exception as e:
            return f"Error al eliminar el archivo: {e}"
    

# Actualiza una lista o diccionario del json con el contenido dado
# si falla algo retornará el error
# si no sale nada mal retornará True
class UpdateJS(Action):

    def __init__(self, js_name: str, content):
        self.content = content
        self.js_name = js_name

    def action(self):
        # Leer el Json
        try:
            with open(self.js_name, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return "Error: El archivo no existe"
        except json.JSONDecodeError:
            return "Error: El archivo JSON está corrupto o vacío"

        if isinstance(data, dict): # Comprobar si es un diccionario
            if not isinstance(self.content, dict):
                return "Error: No puedes actualizar un diccionario con algo que no es un diccionario"
            
            data.update(self.content)

        elif isinstance(data, list): # comprobar si es una lista
            data.append(self.content) 

        else:
            return "Error: El JSON debe ser una lista o un diccionario"

        # Guardar el JSON actualizado
        try:
            with open(self.js_name, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            return f"Error al guardar el archivo: {e}"
        

# comprueba si un archivo existe y no es un directorio
# y tiene la opcion de tambien comprobar si el archivo
# tiene la opcion esperada. 
# Si todo sale bien retornará una lista con un True.
# Si algo falla retornará una lista con el error dado y un False.
class ExistenceJS(Action):

    def __init__(self, js_name: str, extension: str = None):
        self.js_name = js_name
        self.extension = extension

    def action(self):
        # Comprueba si la ruta existe 
        if not os.path.exists(self.js_name):
            return [False, f"Error: La ruta '{self.js_name}' no existe."]

        # Comprueba si es un archivo real y no un directorio 
        if not os.path.isfile(self.js_name):
            return [False, f"Error: '{self.js_name}' no es un archivo, es un directorio."]

        # comprueba si tiene la extensión esperada
        if self.extension is not None:
            if not self.js_name.lower().endswith(self.extension.lower()):
                return [False, f"Error: El archivo no tiene la extensión '{self.extension}'."]

        return [True]