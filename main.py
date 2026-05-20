# Imports librerias externas
from dotenv import load_dotenv
from uuid import uuid4

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
from db.tables_db.agent_repository import AgentRepository
from db.models_db import (MessageSQLMapper, TableMessenge, TableAgent,
                          TableConversation, ConversationSQLMapper)
from db.get_data import generate_date

# Servicios services/
from services.tokens_service import TokensQuery
from services.message_service import HandlingQuery, HandlingOutPut, HandlingSystem
from services.table_service import table_by_dict

tokens_limit_chat = 3000

if __name__ == "__main__":

    # Cargamos claves
    load_dotenv(BASE_DIR / ".env")

    # Nos conectamos con la api
    brain = ConnectBrain(env_key="API_KEY_OPENAI").get_client()

    # Cargar los agentes
    with DataBaseMCB() as db:
        chat_config = AgentRepository(db=db).get_all()

    # Si el usuario no tiene nigún agente disponible
    if not chat_config: 
        print("you doesn't have any agents created. Let's create one")
        # Inicializamos un nuevo agente
        with DataBaseMCB() as db:
            # Creamos su nuevo id
            agent_id = str(uuid4())
            # Validamos los datos
            data_new_agent = TableAgent(
                id= agent_id,
                name= "...",
                model= "gpt-4o-mini",
                behavior="Un bot amigable y que responde todo tipo de dudas",
                temperature= 1.0,
                presence_penalty= 0.4,
                frequency_penalty= 0.4,
                max_tokens= 1000,
                max_input_tokens= 1000,
            )

            # Creamos el agente
            AgentRepository(db=db).create(data=data_new_agent)
            # Obtenemos el agente
            agent_using = AgentRepository(db=db).get_by_id(agent_id=agent_id)
        
            # Le damos un nombre
            name_agent = input("Give him a name: ")
            # Actualizamos el nombre
            agent_using.name = name_agent

            # Le damos un comportamiento
            behavior_agent = input("Give him a behavior: ")
            # Actualizamos el nombre
            agent_using.behavior = behavior_agent

            # Actualizamos en la base de datos
            AgentRepository(db=db).remplace(
                agent_id=agent_id,column="name", attribute=name_agent
                )
            AgentRepository(db=db).remplace(
                agent_id=agent_id,column="behavior", attribute=behavior_agent
                )

    # Si el usuario tiene agentes para usar
    elif chat_config:
        # Lista donde estaran los agente que se pueden usar
        AGENTS_USED = []
        # Mostrar los diferentes agentes disponibles en pantalla
        for agent in chat_config:
            print(agent.name)
            # Guardamos los nombres e ids en una lista
            AGENTS_USED.append({"name":agent.name, "id" : agent.id})
        # Damos la opción de crear uno nuevo
        print("create")

        # Seleccionar un agente
        agent_name = input("\nChoose one you want to use: ") 

        # Si el usuario quiere crear un nuevo chat bot
        if agent_name.lower() == "create":
            # Creamos su nuevo id
            agent_id = str(uuid4())
            # Validamos los datos
            data_new_agent = TableAgent(
                id= agent_id,
                name= "...",
                model= "gpt-4o-mini",
                behavior="Un bot amigable y que responde todo tipo de dudas",
                temperature= 1.0,
                presence_penalty= 0.4,
                frequency_penalty= 0.4,
                max_tokens= 1000,
                max_input_tokens= 1000,
            )

            with DataBaseMCB() as db:
                # Creamos el agente
                AgentRepository(db=db).create(data=data_new_agent)
                # Obtenemos el agente
                agent_using = AgentRepository(db=db).get_by_id(agent_id=agent_id)

                # Le damos un nombre
                name_agent = input("Give him a name: ")
                # Actualizamos el nombre
                agent_using.name = name_agent

                # Le damos un comportamiento
                behavior_agent = input("Give him a behavior: ")
                # Actualizamos el nombre
                agent_using.behavior = behavior_agent

                # Actualizamos en la base de datos
                AgentRepository(db=db).remplace(
                    agent_id=agent_id,column="name", attribute=name_agent
                    )
                AgentRepository(db=db).remplace(
                    agent_id=agent_id,column="behavior", attribute=behavior_agent
                    )

        # Informar si puso un agente inexistente
        elif agent_name not in [agent["name"] for agent in AGENTS_USED]:
            raise ValueError(f"Error: The {agent_name} agent does not exist. Please choose a valid one")

        # Si el usuario puso un agente correcto
        elif agent_name in [agent["name"] for agent in AGENTS_USED]:
            # Obtener el id
            with DataBaseMCB() as db:
                agent_using = AgentRepository(db=db).get_by_name(agent_name=agent_name)
    
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
        # creamos la conversación en la base de datos
        with DataBaseMCB() as db:
            # Definir el id de la convercación
            id_conversation = str(uuid4())

            # Validamos los datos que vayamos a subir
            valid_data_conversation = TableConversation(
                # id de la conversación
                id= id_conversation,
                # Inicialización de titulo de la conversación
                title= "...",
                # fecha en la que se creó la conversación 
                time_start= generate_date(),
                # Comportamiento que tomará la conversación
                id_agent= agent_using.id,
                # tokens que usó el chat
                tokens= 0,
            )

            # db.tables_db.conversation_repository
            # Guarda la conversación en la base de datos
            ConversationRepository(db=db).create(data=valid_data_conversation)
            current_conversation = ConversationRepository(
                db=db
                ).get_by_id(conversation_id=id_conversation)

            # mostrar saludo de la IA
            print(f"\nHola, soy {agent_using.name}.\n¿En que te puedo ayudar hoy?.")

            # Variable que nos permitirá saber si 
            # ya fue creado un titulo para esta conversación
            title_created = False

            # Inicializamos donde se guardará la conversación
            # y añadimos el comportamiento
            messages_conversation = [HandlingSystem(behavior=agent_using.behavior).out_put]

            while True:
                # Obtenemos la query del usuario
                user_query = input("\n>>> ")

                # Cuenta los tokens de la query
                num_tokens_query = TokensQuery(
                    model=agent_using.model, query=user_query
                    ).count_tokens() 

                # validar que no se sobre pase el limite de tokens impuesto para las query del usuario
                # se le pasa los tokens de la query y el limite de tokens
                # si no sobre pasa el limite retorna True, si lo hace retorna False
                token_limit = num_tokens_query <= agent_using.max_input_tokens

                # Si la query cumple el limite de tokens y
                # el chat no ha usado el limite de tokens entonces.... 
                if token_limit == True and current_conversation.tokens < tokens_limit_chat:

                    # formateamos el mensaje
                    # {"role" : "user", "content" : "..."}
                    user_query = HandlingQuery(input_user=user_query).query

                    # sumar los tokens usados al conteo
                    # de tokens total de la conversación
                    ConversationRepository(
                        db=db
                        ).remplace(
                            conversation_id=id_conversation, col="tokens",
                            attribute= num_tokens_query
                            )

                    # actualizando la memoria con la query del user
                    messages_conversation.append(user_query) 
                    
                    # Validamos los datos que vayamos a subir
                    valid_data_message = TableMessenge(
                        id_conversation=id_conversation, # id de la conversación
                        role= user_query["role"], # role del mensaje
                        date= generate_date(), # fecha en la que se guardó el mensaje
                        content= user_query["content"] # contenido del mensaje
                    )

                    # Guarda el mensaje en la base de datos
                    MessageRepository(db=db).save(data= valid_data_message)

                    # Le hacemos la consulta al bot y obtenemos una respuesta
                    answer = QueryExecutor(
                        brain=brain,agent=agent_using
                        ).make_query(conversation=messages_conversation)

                    # formateamos el mensaje
                    # {"role" : "assistant", "content" : "..."}
                    out_put = HandlingOutPut(out_put=answer).out_put

                    # contar los tokens de la respuesta del bot
                    num_tokens_out = TokensQuery(
                    model=agent_using.model, query=out_put["content"]
                    ).count_tokens()

                    # sumar los tokens usados
                    ConversationRepository(db=db).remplace(
                            conversation_id=id_conversation, col="tokens",
                            attribute= num_tokens_out
                            )
                    # actualizar la memoria con la respuesta del bot
                    messages_conversation.append(out_put)
        
                    # Validamos los datos que vayamos a subir
                    valid_data_message = TableMessenge(
                        id_conversation=id_conversation, # id de la conversación
                        role= out_put["role"], # role del mensaje
                        date= generate_date(), # fecha en la que se guardó el mensaje
                        content= out_put["content"] # contenido del mensaje
                    )

                    # Guarda el mensaje en la base de datos
                    MessageRepository(db=db).save(data=valid_data_message)

                    # imprimir la respuesta por pantalla
                    print("\n"+answer)
                    db.conn.commit()

                    # Creamos el titulo
                    if not title_created:
                        # Cargar el creador de titulos
                        JSON_TITLE_MAKER = BASE_DIR / "config" / "title_maker_config.json"
                        title_maker = LoadSettingsAgent(file=JSON_TITLE_MAKER).load()
                        # Lo convertimos a un objeto
                        title_maker = TableAgent(
                            id=str(uuid4()),
                            name= title_maker["name"],
                            model= title_maker["model"],
                            behavior= title_maker["memory"][0]["content"],
                            temperature= title_maker["temperature"],
                            presence_penalty= title_maker["presence_penalty"],
                            frequency_penalty= title_maker["frequency_penalty"],
                            max_tokens= title_maker["max_tokens"],
                            max_input_tokens= title_maker["max_input_tokens"],
                        )

                        # formateamos la primera interacion 
                        # y el comportamiento del bot en una lista
                        first_interaction = [
                            HandlingSystem(title_maker.behavior).out_put,
                            HandlingQuery(input_user=(
                            f"usuario: {user_query['content']}. bot: {out_put['content']}."
                            )).query
                            ]
                        # Obtenemos el titulo con IA
                        title = QueryExecutor(
                            brain=brain,agent=title_maker
                            ).make_query(
                            conversation=first_interaction
                            )

                        ConversationRepository(db=db).remplace(
                            conversation_id= str(id_conversation),
                            col= "title",
                            attribute= title
                            )

                        title_created = True
                        db.conn.commit()

                    # Si el usuario se despide con un unico chao se sale del bucle
                    if user_query["content"].lower() == "chao":
                        break


                # Si la convesación sobrepasa el limite de tokens
                elif not token_limit:
                    print("if you want to keep talking to him that's fine, but pay")
                    # Nos salimos del bucle
                    break
                
                # Si la pregunta sobrepasa el limite de tokens
                if current_conversation.tokens > tokens_limit_chat:
                    print("Do you want to ask him such a long question?.")
                    print("Okay, then I want your money.")
                    # Nos salimos del bucle
                    break
    
    # Decir que no eligió una opción valida
    else:
        raise ValueError(f"Error: {agent_action} is not allowed action")
