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
        print("you doesn't have any agents created. Let's create one")
        # Inicializamos un nuevo agente
        agent_using = JsonAddConfig(file=JSON_CONFIG).Add_config()

        # Le damos un nombre
        name_agent = input("Give him a name: ")
        # Lo guardamos en un diccionario
        name_agent = NameSetter().set(data=name_agent)
        # Lo actualizamos en el diccionario
        # agent_using es una [{}] ponemos agent_using[0]
        # para que agent_using sea solo un {}
        agent_using = UpDateSettingDict(config_agent=agent_using[0], attribute=name_agent).update()

        # Le damos un comportamiento
        behavior_agent = input("Give him a behavior: ")
        # Lo guardamos en un diccionario
        behavior_agent = BehaviorSetter().set(data=behavior_agent)
        # Lo actualizamos en el diccionario
        agent_using = UpDateSettingDict(config_agent=agent_using, attribute=behavior_agent).update()

        # Ahora volvemos a cargar el json
        chat_config = LoadSettingsAgent(file=JSON_CONFIG).load()
        # Actualizamos en el json
        SaveSettingsAgent(file=JSON_CONFIG, config_list=chat_config, agent_update= agent_using).save()

    # Si el usuario tiene agentes para usar
    if chat_config:
        # Lista donde estaran los agente que se pueden usar
        AGENTS_USED = []
        # Mostrar los diferentes agentes disponibles en pantalla
        for agent in chat_config:
            print(agent["name"])
            # Guardamos los nombres e ids en una lista
            AGENTS_USED.append({"name":agent["name"], "id" : agent["id_chat"]})
        # Damos la opción de crear uno nuevo
        print("create")

        # Seleccionar un agente
        agent_name = input("Choose the one you want to use: ") 

        # Si el usuario quiere crear un nuevo chat bot
        if agent_name == "create":
            # creamos un nuevo agente
            agent_using = JsonAddConfig(file=JSON_CONFIG).Add_config()

            # Le damos un nombre
            name_agent = input("Give him a name: ")
            # Lo guardamos en un diccionario
            name_agent = NameSetter().set(data=name_agent)
            # Lo actualizamos en el diccionario
            agent_using = UpDateSettingDict(config_agent=agent_using, attribute=name_agent).update()

            # Le damos un comportamiento
            behavior_agent = input("Give him a behavior: ")
            # Lo guardamos en un diccionario
            behavior_agent = BehaviorSetter().set(data=behavior_agent)
            # Lo actualizamos en el diccionario
            agent_using = UpDateSettingDict(config_agent=agent_using, attribute=behavior_agent).update()

            # Ahora volvemos a cargar el json
            agents_container = LoadSettingsAgent(file=JSON_CONFIG).load()
            # Actualizamos en el json
            SaveSettingsAgent(file=JSON_CONFIG, config_list=agents_container, agent_update= agent_using).save()
        
        # Informar si puso un agente inexistente
        elif agent_name not in [agent["name"] for agent in AGENTS_USED]:
            raise ValueError(f"Error: The {agent_name} agent does not exist. Please choose a valid one")

        # Si el usuario puso un agente correcto
        elif agent_name in [agent["name"] for agent in AGENTS_USED]:
            # Obtener el id
            agent_id = next(
                (agent["id"] for agent in AGENTS_USED if agent["name"] == agent_name)
            )
            # Definir el agente que usará el usuario
            agent_using = next(
                (agent for agent in chat_config if agent["id_chat"] == agent_id)
            )

    