import config_IA
import initialize
import text_validators
import valid
import valid_queries
import make_queries
import connection
import actions

# base de datos
from db.initialize_db import DataBaseMCB
from db.tables_db.message_repository import MessageRepository
from db.tables_db.conversation_repository import ConversationRepository
from db.models_db import (MessageSQLMapper, TableMessenge,
                          TableConversation, ConversationSQLMapper)
from db.get_data import generate_uuid, generate_date

import os
from dotenv import load_dotenv
import json

load_dotenv()


config_name = "config.json"
chat_name_df = "new chat"
history_chat = "history.json"
# el limite de tokens que se pueden usar en la conversación
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
    # connection
    api_OAI = os.getenv("API_KEY_OPENAI")
    brain = connection.ConnectBrain(api_OAI)
    # Crear un cliente 
    client = brain.connect()

    # Cargar los agentes
    chat= chat_create.load() 
    
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
        # Elegir un agente
        chat_select = input("Elige el que quieras usar: ") 

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

    # hacer la petición querie
    out = False

    # Definir el id de la convercación
    id_conversation = generate_uuid()

    # inicializar title_init
    # para decirle al agente
    # que aun no hay un título 
    title_init = False

    # creamos la conversación en la base de datos
    with DataBaseMCB() as db:

        # db.models_db.py                                
        # Validamos los datos que vayamos a subir
        valid_data_conversation = TableConversation(
            # id de la conversación
            id= id_conversation,
            # Inicialización de titulo de la conversación
            title= "...",
            # fecha en la que se creó la conversación 
            time_start= generate_date(),
            # Comportamiento que tomará la conversación
            behavior= agent["memory"][0]["content"]
        )
        # Mapeamos los datos en una tupla para amanejarlos
        data_conversation = ConversationSQLMapper()#.to_row(message=valid_data_conversation)

        # db.tables_db.conversation_repository
        # Guarda la conversación en la base de datos
        ConversationRepository(db=db,data=valid_data_conversation).create(data_conversation)

    # Primer saludo de la IA
    request_query = {
        "role" : "assistant",
        "content" : f"\nHola, soy {agent['name']}.\n¿En que te puedo ayudar hoy?."
        }
    print(request_query["content"])

    # Actualizamos la memoria del bot
    agent["memory"].append(request_query)

    with DataBaseMCB() as db:

        # db.models_db.py                                
        # Validamos los datos que vayamos a subir
        valid_data_message = TableMessenge(
            id_conversation=id_conversation, # id de la conversación
            role= request_query["role"], # role del mensaje
            date= generate_date(), # fecha en la que se guardó el mensaje
            content= request_query["content"] # contenido del mensaje
           )
        # Mapeamos los datos en una tupla para amanejarlos
        data_message = MessageSQLMapper.to_row(message=valid_data_message)

        # db.tables_db.messege_repository.py
        # Guarda el mensaje en la base de datos
        MessageRepository(db=db).save(data_message)


    while out != True:
        # Obtenemos la querie del usuario
        user_querie = input("\n")

        # valid_queries.py
        # Objeto que nos ayuda a manejar los tokens
        tokens_control = valid_queries.tokens_querie(model=agent["model"], querie=user_querie)

        # Cuenta los tokens de la querie
        num_tokens = tokens_control.count_tokens() 

        # valid.py
        # validar que no se sobre pase el limite de tokens impuesto para las queries del usuario
        # se le pasa los tokens de la querie y el limite de tokens
        # si no sobre pasa el limite retorna True, si lo hace retorna False
        token_limit = valid.TokensValid(tokens=num_tokens, max_tokens=agent["max_input_tokens"]).is_valid() 
        
        # Si la querie cumple el limite de tokens y
        # el chat no ha usado el limite de tokens entonces.... 
        if token_limit == True and agent["tokens"] < tokens_limit_chat:

            # valid_queries.py
            # obtenemos la querie del usuario en un diccionario
            # {"role" : "user", "content" : "..."}
            querie = valid_queries.HandlingQueries(input_user=user_querie).input_user 

            # sumar los tokens usados al conteo
            # de tokens total de la conversación
            agent["tokens"] += num_tokens 

            # actualizando la memoria con la querie del user
            agent["memory"].append(querie) 
            
            # db.initialize_db.py
            # Abrimos conexión con la base de datos
            # para guardar el mensaje del user
            with DataBaseMCB() as db:

                # db.models_db.py                                
                # Validamos los datos que vayamos a subir
                valid_data_message = TableMessenge(
                    id_conversation=id_conversation, # id de la conversación
                    role= querie["role"], # role del mensaje
                    date= generate_date(), # fecha en la que se guardó el mensaje
                    content= querie["content"] # contenido del mensaje
                )
                # Mapeamos los datos en una tupla para amanejarlos
                data_message = MessageSQLMapper.to_row(message=valid_data_message)

                # db.tables_db.messege_repository.py
                # Guarda el mensaje en la base de datos
                MessageRepository(db=db).save(data_message)

            # make_queries.py
            # Le hacemos la consulta al bot y obtenemos una respuesta
            answer = make_queries.HardQuerie(brain=client,agent=agent).make_querie()

            # valid_queries.py
            # Mapeamos la respuesta del bot en un diccionario
            # {"role" : "assistant", "content" : "..."}
            out_put = valid_queries.HandlingOutPut(out_put=answer).out_put

            # contar los tokens de la respuesta del bot
            num_tokens_out = tokens_control.count_tokens()

            # sumar los tokens usados
            agent["tokens"] += num_tokens 

            agent["memory"].append(out_put) # actualizar la memoria con la respuesta del bot

            # db.initialize_db.py
            # Abrimos conexión con la base de datos
            # para guardar el mensaje del assistant
            with DataBaseMCB() as db:

                # db.models_db.py                                
                # Validamos los datos que vayamos a subir
                valid_data_message = TableMessenge(
                    id_conversation=id_conversation, # id de la conversación
                    role= out_put["role"], # role del mensaje
                    date= generate_date(), # fecha en la que se guardó el mensaje
                    content= out_put["content"] # contenido del mensaje
                )
                # Mapeamos los datos en una tupla para amanejarlos
                data_message = MessageSQLMapper.to_row(message=valid_data_message)

                # db.tables_db.messege_repository.py
                # Guarda el mensaje en la base de datos
                MessageRepository(db=db).save(data_message)

            # imprimir la respuesta por pantalla
            print("\n"+answer) 

            # Creamos un titulo con la query del primer mensaje
            if title_init == False:

                # Abrimos el json en forma de lectura
                with open("title_maker_config.json", "r") as config_tm:      
                    # Guardamos las configuraciones del agente
                    # diseñado para crear un titulo en una variable    
                    title_maker = config_tm.read()

                # Le hacemos una consulta al agente diseñado para crear titulos
                # y optenemos una respues, es dicir el titulo de la conversación
                title_conversation = make_queries.HardQuerie(brain=client,agent=title_maker).make_querie()
                
                # Abrimos conexión 
                # para remplazar el titulo
                with DataBaseMCB() as db:

                    # db.tables_db.conversation_repository
                    # remplaza el titulo generico (...) por el nuevo
                    ConversationRepository(db=db).remplace(id_conversation=id_conversation,col="title",attribute=title_conversation)

                # Le decimos al programa
                # que ya creamos el titulo
                title_init = True

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