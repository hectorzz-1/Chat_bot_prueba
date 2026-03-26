# Imports librerias externas
from dotenv import load_dotenv

# Imports librerias internas
# Agente de IA agent/
from agent.connection import ConnectBrain
from agent.config_IA import (
    LoadSettingsAgent, SaveSettingsAgent, UpDateSettingDict,
    )
from agent.agent_setter import NameSetter, BehaviorSetter

# Configuraciones Config/
from config.config import BASE_DIR
from config.json_init import JsonAddConfig

if __name__ == "__main__":

    # Cargamos claves
    load_dotenv(BASE_DIR / ".env")

    # Nos conectamos con la api
    brain = ConnectBrain(env_key="API_KEY_OPENAI").get_client()

    # Cargar los agentes
    JSON_CONFIG= BASE_DIR / "config" / "agents.json"
    chat_config= LoadSettingsAgent(file=JSON_CONFIG).load()

    # Si el usuario no tiene nigún agente disponible
    if not chat_config: 
        print("No tiene ningún agente creado. Creemos uno")
        # Inicializamos un nuevo agente
        agent_using = JsonAddConfig(file=JSON_CONFIG).Add_config()

        # Le damos un nombre
        name_agent = input("Nombre: ")
        # Lo guardamos en un diccionario
        name_agent = NameSetter().set(data=name_agent)
        # Lo actualizamos en el diccionario
        # agent_using es una [{}] ponemos agent_using[0]
        # para que agent_using sea solo un {}
        agent_using = UpDateSettingDict(config_agent=agent_using[0], attribute=name_agent).update()

        # Le damos un comportamiento
        behavior_agent = input("Dale un comportamiento: ")
        # Lo guardamos en un diccionario
        behavior_agent = BehaviorSetter().set(data=behavior_agent)
        # Lo actualizamos en el diccionario
        agent_using = UpDateSettingDict(config_agent=agent_using, attribute=behavior_agent).update()

        # Ahora volvemos a cargar el json
        agents_container = LoadSettingsAgent(file=JSON_CONFIG).load()
        # Actualizamos en el json
        SaveSettingsAgent(file=JSON_CONFIG, config_list=agents_container, agent_update= agent_using).save()

    