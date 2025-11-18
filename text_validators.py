# En este fichero se almacenarán la validación de datos del fichero 
# --> text_providers.py.

# Librerias Externas
from abc import ABC, abstractmethod
import re

class TextValidator(ABC):

    @abstractmethod
    def validator(self):
        pass


# Validará que la variable no esté vacia
# Si está vacia retornará --> False
# Si Tiene al menos un caracter valido retornará --> True 
class TextValidatorIfEmpty(TextValidator):

    def __init__(self):
        self.info = {
                         "check" : False,
                         "error" : "Por favor introduzca un texto",
                         "name" : "TextValidatorIfEmpty"
                     }

    def validator(self, text: str):
        if text:
            return True
        else:
            return False


# Validará si el texto tiene caracteres Usables
# Incluye letras (a-z, A-Z), números (0-9), espacios, puntuación básica y acentos
# si todo está correcto retornará --> True
# si algo falla retornará --> False
class TextValidatorValid(TextValidator):

    def __init__(self):
        self.info = {
                         "check" : False,
                         "error" : "Por favor solo coloque caracteres comunes como letras, espacios y puntuacion solamente",
                         "name" : "TextValidatorValid"
                      }
    
    def validator(self, text: str):
        # Incluye letras (a-z, A-Z), números (0-9), espacios, puntuación básica y acentos
        # si todo está correcto retornará --> True
        # si algo falla retornará --> False
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,;:!?'\-()]+", text))
    

# Validará si el texto solo contiene espacios " "
# si es el caso retornará --> False
# si todo es correcto retornará --> True
class TextValidatorEspace(TextValidator):

    def __init__(self):
        self.info = {
                         "check" : False,
                         "error" : "Por favor introduzca un texto",
                         "name" : "TextValidatorEspace"
                      }


    def validator(self, text: str):
        for i in text:
            if i != " ":
                return True
        
        return False
    

# Validará que la cadena de texto tenga tenga como maximo 500 carácteres
# si tiene -= que 500 retornará True
# si no tiene -= 500 retornará False
class TextValidatorLong(TextValidator):
    def __init__(self):
        self.info = {
                         "check" : False,
                         "error" : "Por favor no coloque mas de 500 caracteres",
                         "name" : "TextValidatorLong"
                      }

    
    def validator(self, text: str):
        if len(text) - 501:
            return True
        else:
            return False
        

# Esta clase obtiene como parametros instancias que hereden
# de TextValidator dependiendo de las instancias validará una cosa u otra
# retornara una lista con diccionarios con las clave check, error, name  
class Validator:

    def __init__(self, *validators: TextValidator):
        self.instancias_list = list(validators)
        self.validatorslist = []
        

    def validate(self, text):
        for i in self.instancias_list:
            try:   
                # Validadr
                check = i.validator(str(text))
                
                # Modificando el diccionario
                # con la respuesta de si es valido o no 
                i.info["check"] = check
            except:
                pass

            # actualizar la lista de diccionarios que retornará
            self.validatorslist.append(i.info)          

        return self.validatorslist
