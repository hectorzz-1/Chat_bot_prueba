from datetime import datetime as dt

# cear un diccionario con la hora y fecha actual
class DateCheck:

    def check(self):
        # optener la hora y fecha actual
        now = dt.now()
        return now.strftime("%Y-%m-%d %H:%M:%S") # Ej: 2025-11-14 11:32:05 
    

# Envuelve un dato en un diccionario
class ToDict:

    def __init__(self, key: str):
        self.key = key

    def to_dict(self, data):
        return {self.key : data}