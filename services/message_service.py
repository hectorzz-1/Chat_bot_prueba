# formatear mensajes al esquema role/content
class HandlingQuery:

    def __init__(self, input_user: str):
        self.query = {"role" : "user", "content" : input_user}


# formatear mensajes al esquema role/content
class HandlingOutPut:

    def __init__(self, out_put: str):
        self.out_put = {"role" : "assistant", "content" : out_put}


# formatear mensajes al esquema role/content
class HandlingSystem:

    def __init__(self, behavior: str):
        self.out_put = {"role" : "system", "content" : behavior}