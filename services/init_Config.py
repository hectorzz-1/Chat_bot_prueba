from db.initialize_db import DataBaseMCB

from config.json_init import JsonAddConfig
from config import BASE_DIR


class AgentInit:
    def __init__(self, name: str = "", behavior: str = "", model: str = ""):
        pass
    
    def initialize_agent(self):
        pass

def init_IA_func(name: str = "", behavior: str = "", model: str = ""):
    # Crea un agente con configuraciones por defecto
    FILE_CONFIG = BASE_DIR / "config" / "agents.json"
    JsonAddConfig(file=FILE_CONFIG).Add_config()

    if config_created == True: 

        if name:  # Actuallizar el nombre por defaul
            valid_text = text_validator.validate(name) # valida el behavior
            for i in valid_text:

                # si el nombre no es valido se quedará con el que tiene por defecto
                if i["check"] == False:
                    break
                
                # Si todo esta correcto
                else:
                    # Coloca el nombre
                    init_config.add(setter=name_setter, value=name_nc)

        if behavior: # Cambiar el comportamiento por defecto
            valid_text = text_validator.validate(behavior) # valida el behavior
            for i in valid_text:

                # si el behavior no es valido se quedará con el que tiene por defecto
                if i["check"] == False:
                    break
                
                # Si todo esta correcto
                else:
                    # Coloca el comportamiento
                    init_config.add(setter=behavior_setter, value=behavior)

        if model: # Cambiar el modelo por defecto
            # Si existe el modelo se lo configura al agente
            if model in models_opcions:
                init_config.add(setter=model_setter, value=name_nc)
            
        init_config.save() # guarda los cambios
        return True
    else:
        print("Ah ocurrido un ERROR de carga, intente más tarde")
        return False