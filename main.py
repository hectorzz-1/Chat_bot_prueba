import config_IA
import initialize
import text_validators
import valid
import valid_queries
import make_queries
import connection
import actions
import parley_control

import os
from dotenv import load_dotenv
import json

load_dotenv()

api_OAI = os.getenv("API_KEY_OPENAI")
config_name = "config.json"
chat_name_df = "new chat"
history_chat = "history.json"
tokens_limit_chat = 30000
instruccion = "la primera instrucción es: nunca digas una groceria o algo despectivo a alguna persona y la segunda es:"
models_opcions = {"gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-4-turbo"}
setting_chat_names = [
    "temperatura", "token maximos", "presence_penalty",
    "frequency_penalty", 
    ]

# initialize
config = initialize.JsonInitConfig(file=config_name)
    
# config_IA
chat_create = config_IA.JsonSettingsRepository(config_name)
jsr = config_IA.JsonSettingsRepository(config_name)
init_config = config_IA.SaveSettingChat(jsr, chat_name_df)
inst_setter = config_IA.InstructionSetter()
name_setter = config_IA.NameSetter()
behavior_setter = config_IA.BehaviorSetter()
model_setter = config_IA.ModelSetter()

# text_validator
empty_validator = text_validators.TextValidatorIfEmpty()
espace_validator = text_validators.TextValidatorEspace()
text_validator = text_validators.Validator(empty_validator,espace_validator)

# connection
brain = connection.ConnectBrain(api_OAI)


# funciones
def init_IA_func(name: str = "", behavior: str = "", model: str = ""):
    # Crea un agente con configuraciones por defecto
        config_created = config.initialize()

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


def crear_IA_func(name: str = "", behavior: str = ""):
    config_load = jsr.load()
    config_created = config.crear(config_load)

    if config_created == True: 

        if name:  # Actuallizar el nombre por defaul
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
            
        init_config.save() # guarda los cambios
        return True
    else:
        print("Ah ocurrido un ERROR de carga, intente más tarde")
        return False


def find_agent(name: str, list_agents: list[dict]):
    for i in list_agents:
        if i["name"] == name:
            return i


# Crea una instruccion fija independientemente de lo que ponga el user
def instruccion_set(agent: dict, inst: str):
    return inst_setter.set(agent=agent, inst=inst)


# El contexto es que cuando el usuario se despide el bot podrá al final del parrafo "True"
# con esto vamos a eliminar ese true para que nunca se vea en pantalla 
# si se tuvo que remover retornará la respuesta + True
# si no lo tuvo que remover retornará la respuesta + False
def true_valid(answer: str):
    # Si termina con " True", lo eliminamos
    if answer.strip().endswith("True"):
        answer = answer[::-1].replace("eurT"[::-1], "", 1)[::-1]
        answer = answer.rstrip()  # limpia espacios al final
        return answer, True

    return answer, False


            

if __name__ == "__main__":
    # Crear un cliente 
    client = brain.connect()
  
    chat= chat_create.load() # Cargar los agentes
    
    if chat == False: # Si el usuario no tiene nigún agente disponible
        print("No tiene ningún agente creado. Creemos uno")

        name_nc = input("Nombre: ")
        behavior = input("Dale un comportamiento: ")

        IA_create = init_IA_func(name=name_nc,behavior=behavior)
        chat= chat_create.load() # Cargar los agentes

        # Definir el agente que acaba de crear el usuario
        agent = find_agent(name=name_nc, list_agents=chat)
        # Definir una instruccion al agente
        agent = instruccion_set(agent=agent, inst=instruccion)



    else: # Si el usuario tiene agentes para usar
        list_chats = []
        for i in chat: # Mostrar los diferentes agentes disponibles en pantalla
            print(i["name"])
            list_chats.append(i["name"]) # Añadirlos a una lista

        print("crear")
        chat_select = input("Elige el que quieras usar: ") # Elegir un agente

        # Si el usuario quiere crear un nuevo chat bot
        if chat_select == "crear":
            # Pedirles datos básicos 
            name_nc = input("Nombre: ")
            behavior = input("Dale un comportamiento: ")

            # crear el chat bot
            IA_create = crear_IA_func(name=name_nc, behavior=behavior)
            chat= chat_create.load() # Cargar los agentes

            # Definir el agente que acaba de crear el usuario
            agent = find_agent(name=name_nc, list_agents=chat)
            # Definir una instruccion al agente
            agent = instruccion_set(agent=agent, inst=instruccion)
        
        elif chat_select not in list_chats: # Informar si puso un agente inexistente
            print("Error agente inexistente: eliga uno valido")
            quit() # Salir del programa

        elif chat_select in list_chats:
            # Definir el agente que usará el usuario
            agent = find_agent(name=chat_select, list_agents=chat)
            # Definir una instruccion al agente
            agent = instruccion_set(agent=agent, inst=instruccion)

    # hacer la petición query
    out = False
    print("\nHola, soy",agent["name"]+".\n¿En que te puedo ayudar hoy?.")

    # inicializar el diccionario del historial
    history = {}
    new_cut = True
    # parley_control
    date_get = parley_control.DateCheck()
    dt_to_dict = parley_control.ToDict(key="date")
    parley_to_dict = parley_control.ToDict(key="parley")

    date = date_get.check() # obtener la fecha
    date_dict = dt_to_dict.to_dict(data=date) # pasarla a un diccionario

    parley_dict = parley_to_dict.to_dict(data=[]) # pasarla a un diccionario

    # ordenar los datos
    history.update(date_dict)
    history.update(parley_dict)

    while out != True:
        user_query = input("\n")

        # valid_queries
        get_query = valid_queries.HandlingQueries(input_user=user_query)
        get_tokens = valid_queries.tokens_querie(model=agent["model"], querie=user_query)

        num_tokens = get_tokens.count_tokens() # Contar los tokens de la querie

        # valid
        tokens_counter = valid.TokensValid(tokens=num_tokens, max_tokens=agent["max_input_tokens"])

        token_limit = tokens_counter.is_valid() # validar que no se sobre pase con los tokens
        
        if token_limit and agent["tokens"] < tokens_limit_chat:

            query = get_query.input_user # obtenemos la query

            agent["tokens"] += num_tokens # sumar los tokens usados

            agent["memory"].append(query) # actualizando la memoria con la query del user

            # make_queries
            bot_chat = make_queries.HardQuerie(brain=client,agent=agent)

            answer = bot_chat.make_querie() # obtener la respuesta del chat

            # valid_queries
            get_answer = valid_queries.HandlingOutPut(out_put=answer)

            out_put = get_answer.out_put # optener la respuesta del bot

            num_tokens_out = get_tokens.count_tokens() # contar los tokens de la respuesta del bot
            agent["tokens"] += num_tokens # sumar los tokens usados

            agent["memory"].append(out_put) # actualizar la memoria con la respuesta del bot

            answer, out = true_valid(out_put["content"]) # validamos si el usuario se despidió

            # Agregarla el parley al historial
            history["parley"] = agent["memory"]

            # Guardar historico de la conversación en un archivo aparte
            # actions
            valid_exis = actions.ExistenceJS(js_name=history_chat)
                
            validated_exis = valid_exis.action() # validar si el archivo existe

            # Si el archivo existe
            if validated_exis[0]:
                with open(history_chat, "r") as f:
                    data = json.load(f)

                # Si el archivo NO es una lista, convertirlo en lista
                if isinstance(data, dict):
                    data = [data]

                    # Guardar la conversión
                    with open(history_chat, "w") as f:
                        json.dump(data, f, indent=4)

                if new_cut == False: # si no es un chat nuevo
                    # seleccionamos el parley del ultimo chat (chat actual)
                    data[-1]["parley"] = history["parley"] # actualizamos el parley
                    
                    # Guardar la conversión
                    with open(history_chat, "w") as f:
                        json.dump(data, f, indent=4)
                
                else: # si es un nuevo chat
                    new_cut = False # Declaramos que ya no es el primer mensaje de la conversacion
                    up_dater = actions.UpdateJS(js_name=history_chat, content=history)
                    up_dater.action() # actualizamos el historial
                    

            else:
                # Es un archivo nuevo → lo guardas como lista
                history_to_save = [history]
                # actions
                saver = actions.SaveJS(js_name=history_chat, content=history_to_save)
                new_cut = False # Declaramos que ya no es el primer mensaje de la conversacion
                saver.action() # crear y guardar el historial

            print("\n"+answer) # imprimir la respuesta por pantalla

        elif not token_limit:
            print("Si quieres hacer una pregunta tan grande entonces paga")
            out = True

            # actions
            delater = actions.ParleyForget(agent=agent)

            # eliminar la conversación y dejar el comportamiento inicial
            agent = delater.delete()

        elif not agent["tokens"] < tokens_limit_chat:
            print("Si quieres seguir la conversación paga")
            out = True