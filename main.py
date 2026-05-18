# Imports librerias externas
from dotenv import load_dotenv

# Imports librerias internas
# Agente de IA agent/
from agent.connection import ConnectBrain
from agent.config_IA import (
    LoadSettingsAgent, SaveSettingsAgent, UpDateSettingDict,
    )
from agent.agent_setter import NameSetter, BehaviorSetter
from agent.query_executor import QueryExecutor

# Configuraciones Config/
from config.config import BASE_DIR
from config.json_init import JsonAddConfig

# Base de datos db/
from db.initialize_db import DataBaseMCB
from db.tables_db.message_repository import MessageRepository
from db.tables_db.conversation_repository import ConversationRepository
from db.models_db import (MessageSQLMapper, TableMessenge,
                          TableConversation, ConversationSQLMapper)
from db.get_data import generate_uuid, generate_date

# Servicios services/
from services.tokens_service import TokensQuery
from services.message_service import HandlingQuery, HandlingOutPut
from services.table_service import table_by_dict

tokens_limit_chat = 3000

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

    # Preguntar que acción quiere hacer el usuario
    ACTIONS_ALLOWED = ["view history", "chat"]
    
    print("\nWhat do you want to do?\n")
    for action in ACTIONS_ALLOWED:
        print(f"{action}\n") 

    agent_action = input("")

    # Si el usuario quiere ver el historial del agente
    if agent_action == "view history":
        with DataBaseMCB() as db:
            datos = ConversationRepository(db=db, data=[]).get_conversations()

            new_dates = []
            INDEX_ALLOWED = []
            for index, date in enumerate(datos, start=1) :
                new_date = {
                    "position": index,
                    "id_db" : date[0],
                    "title": date[1],
                    "date" : date[2].strftime("%Y-%m-%d %I:%M:%S %p"),
                }
                
                INDEX_ALLOWED.append(index)
                new_dates.append(new_date)

            # Creamos una tabla con los tados y la imprimimos en pantalla
            table_by_dict(data=new_dates, table_name="Historial de conversación", exclude=["id_db"])

            # Le preguntamos la conversación que quiere ver
            position_conversation = input("\nchoose one: ")

            # Si el usuario seleccionó un index correcto
            if int(position_conversation) in INDEX_ALLOWED:
                # seleccionamos la conversacion que quiere el usuario
                for conv in new_dates:
                    if conv["position"] == int(position_conversation):
                        conversation_selected = conv
                        break
                    
                # Obtenemos los mensajes de la conversacion
                messages_conversation = (
                    MessageRepository(db=db).
                    get_by_conversation(
                        conversation_id=conversation_selected["id_db"]
                        )
                    )

                # Imprimimos todos los mensajes
                for messege in messages_conversation:
                    print(f"""
                        \n{messege.role}: {messege.content}\n{messege.date}
                        """)
            # Si no selecciona un index correcto
            else:
                raise ValueError("you need put a valid position")

    # Si el usuario quiere hablar con el agente
    elif agent_action == "chat":
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
            agent_name = input("\nChoose one you want to use: ") 

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

        # creamos la conversación en la base de datos
        with DataBaseMCB() as db:
            # Definir el id de la convercación
            id_conversation = generate_uuid()

            # instanceamos el mapper de mensajes
            mapper_message = MessageSQLMapper()
            # Instanseamos el mapeador de conversacion
            mapper_conversation = ConversationSQLMapper()

            # Validamos los datos que vayamos a subir
            valid_data_conversation = TableConversation(
                # id de la conversación
                id= id_conversation,
                # Inicialización de titulo de la conversación
                title= "...",
                # fecha en la que se creó la conversación 
                time_start= generate_date(),
                # Comportamiento que tomará la conversación
                behavior= agent_using["memory"][0]["content"]
            )

            # db.tables_db.conversation_repository
            # Guarda la conversación en la base de datos
            ConversationRepository(db=db,data=valid_data_conversation).create(mapper_conversation)
            db.conn.commit()

            # Primer saludo de la IA
            request_query = {
                "role" : "assistant",
                "content" : f"\nHola, soy {agent_using['name']}.\n¿En que te puedo ayudar hoy?."
            }
            print(request_query["content"])

            """# Actualizamos la memoria del bot
            agent_using["memory"].append(request_query)

            # guardamos el mensaje en la base de datos
            # Validamos los datos que vayamos a subir
            valid_data_message = TableMessenge(
                id_conversation=id_conversation, # id de la conversación
                role= request_query["role"], # role del mensaje
                date= generate_date(), # fecha en la que se guardó el mensaje
                content= request_query["content"] # contenido del mensaje
            )

            # Guarda el mensaje en la base de datos
            MessageRepository(db=db, data=valid_data_message).save(mapper_message)"""

            # Variable que nos permitirá saber si 
            # ya fue creado un titulo para esta conversación
            title_created = False

            while True:
                # Obtenemos la query del usuario
                user_query = input("\n>>> ")

                # Objeto que nos ayuda a manejar los tokens
                tokens_control = TokensQuery(model=agent_using["model"], query=user_query)

                # Cuenta los tokens de la query
                num_tokens_query = tokens_control.count_tokens() 

                # validar que no se sobre pase el limite de tokens impuesto para las query del usuario
                # se le pasa los tokens de la query y el limite de tokens
                # si no sobre pasa el limite retorna True, si lo hace retorna False
                token_limit = num_tokens_query <= agent_using["max_input_tokens"]

                # Si la query cumple el limite de tokens y
                # el chat no ha usado el limite de tokens entonces.... 
                if token_limit == True and agent_using["tokens"] < tokens_limit_chat:

                    # formateamos el mensaje
                    # {"role" : "user", "content" : "..."}
                    user_query = HandlingQuery(input_user=user_query).query

                    # sumar los tokens usados al conteo
                    # de tokens total de la conversación
                    agent_using["tokens"] += num_tokens_query 

                    # actualizando la memoria con la query del user
                    agent_using["memory"].append(user_query) 


                    # Abrimos conexión con la base de datos
                    # para guardar el mensaje del user
                    with DataBaseMCB() as db:

                        # Validamos los datos que vayamos a subir
                        valid_data_message = TableMessenge(
                            id_conversation=id_conversation, # id de la conversación
                            role= user_query["role"], # role del mensaje
                            date= generate_date(), # fecha en la que se guardó el mensaje
                            content= user_query["content"] # contenido del mensaje
                        )

                        # db.tables_db.messege_repository.py
                        # Guarda el mensaje en la base de datos
                        MessageRepository(db=db, data= valid_data_message).save(mapper_message)

                    # Le hacemos la consulta al bot y obtenemos una respuesta
                    answer = QueryExecutor(brain=brain,agent=agent_using).make_query()

                    # formateamos el mensaje
                    # {"role" : "assistant", "content" : "..."}
                    out_put = HandlingOutPut(out_put=answer).out_put

                    # contar los tokens de la respuesta del bot
                    num_tokens_out = tokens_control.count_tokens()

                    # sumar los tokens usados
                    agent_using["tokens"] += num_tokens_out 
                    # actualizar la memoria con la respuesta del bot
                    agent_using["memory"].append(out_put) 

                    # Abrimos conexión con la base de datos
                    # para guardar el mensaje del assistant
                    with DataBaseMCB() as db:            
                        # Validamos los datos que vayamos a subir
                        valid_data_message = TableMessenge(
                            id_conversation=id_conversation, # id de la conversación
                            role= out_put["role"], # role del mensaje
                            date= generate_date(), # fecha en la que se guardó el mensaje
                            content= out_put["content"] # contenido del mensaje
                        )

                        # Guarda el mensaje en la base de datos
                        MessageRepository(db=db, data=valid_data_message).save(mapper_message)

                    # imprimir la respuesta por pantalla
                    print("\n"+answer)

                    # Creamos el titulo
                    if not title_created:
                        # Cargar el creador de titulos
                        JSON_TITLE_MAKER = BASE_DIR / "config" / "title_maker_config.json"
                        title_maker = LoadSettingsAgent(file=JSON_TITLE_MAKER).load()

                        # Añadimos la primera interacción entre el usuario y el bot
                        conversation = HandlingQuery(input_user=(
                            f"usuario: {user_query['content']}. bot: {out_put['content']}."
                        )).query

                        title_maker["memory"].append(conversation)
                        # Obtenemos el titulo con IA
                        title = QueryExecutor(brain=brain,agent=title_maker).make_query()

                        with DataBaseMCB() as db:
                            ConversationRepository(db=db).remplace(
                                conversation_id= str(id_conversation),
                                col= "title",
                                attribute= title
                                )

                        title_created = True

                    # Si el usuario se despide con un unico chao se sale del bucle
                    if user_query["content"].lower() == "chao":
                        break


                # Si la convesación sobrepasa el limite de tokens
                elif not token_limit:
                    print("if you want to keep talking to him that's fine, but pay")
                    # Nos salimos del bucle
                    break
                
                # Si la pregunta sobrepasa el limite de tokens
                if agent_using["tokens"] >= tokens_limit_chat:
                    print("Do you want to ask him such a long question?.")
                    print("Okay, then I want your money.")
                    # Nos salimos del bucle
                    break
    
    # Decir que no eligió una opción valida
    else:
        raise ValueError(f"Error: {agent_action} is not allowed action")
