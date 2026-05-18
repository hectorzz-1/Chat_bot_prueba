from rich import print, box
from rich.table import Table
from rich.console import Console
from typing import Sequence


class TableCreater:

    def __init__(self, table_name: str , columns: Sequence):

        # Validar que table_name sea un string
        if not isinstance(table_name, (str)):
            raise TypeError("table_name must be a string")
        
        # Validar que columns sea una tupla o lista
        if not isinstance(columns, (list, tuple)):
            raise TypeError("columns must be a list or tuple")

        # Convertimos todos los valores a string
        self.columns = [str(value) for value in columns]
        self.table_name = table_name

    def create_table(self) -> Table:
        # Creamos la tabla
        table = Table(title=self.table_name, box=box.ROUNDED)

        # Añadimos las columnas 
        for column in self.columns:
            table.add_column(column, style="white")

        return table


class TableRowAdder:

    def __init__(self, row: Sequence, table: Table):

        # Validar que row sea una tupla o lista
        if not isinstance(row, (list, tuple)):
            raise TypeError("row must be a list or tuple")

        # Validar que table sea una tabla de rich
        if not isinstance(table, Table):
            raise TypeError("table must be an instance of rich.table.Table")

        # Validamos que las columnas y las filas conicidan
        if len(table.columns) != len(row):
            raise ValueError(f"you just sent {len(row)} fields, and the table needs exactly {len(table.columns)} fields")

        # Convertimos todos los valores a string
        self.row = [str(value) for value in row]
        self.table = table

    def add(self) -> None:
        self.table.add_row(*self.row)


class TablePrinter:

    def __init__(self, table):
        # Validar que table sea una tabla de rich
        if not isinstance(table, Table):
            raise TypeError("table must be an instance of rich.table.Table")
        
        self.table = table
        self.console = Console()

    def show(self) -> None:
        self.console.print(self.table)


def table_by_dict(
        data : dict | list[dict],
        table_name : str = "ORDERED LIST",
        exclude : str | list[str] = None
        ) -> None: 
    
    # Normalizamos exclude siempre a una lista
    if exclude is None:
        exclude = []
    elif isinstance(exclude, str):
        exclude = [exclude]
    
    # Obtenemos una listas con las llaves
    dict_keys = []
    # Validamos si es un list[dict] o dict
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):   

        # Filtramos las keys excluidas
        data_filtred = [{
                key: value
                for key, value in obj.items()
                if key not in exclude
            } for obj in data ]

        dict_keys = list(data_filtred[0].keys())

    elif isinstance(data, dict):
        data_filtred = {
            key: value
            for key, value in data.items()
            if key not in exclude
            }
        dict_keys = list(data_filtred.keys())
        data_filtred = [data_filtred] 

    else:
        raise ValueError("you must to enter a dict or list[dict]")
    
    # Creamos la tabla
    table = TableCreater(table_name=table_name, columns= dict_keys).create_table()

    # Añadimos los datos a la tabla
    for i in data_filtred:
        # Añadimos el contenido de cada diccionario
        TableRowAdder(table=table, row= list(i.values())).add()

    TablePrinter(table= table).show()


if __name__ == "__main__":

    columnas = ["nombre", "primer apellido", "segundo apellido"]
    table = TableCreater("nombres", columns= columnas).create_table()

    row_uno = ["Hector", "Loyo", "Mesen"]
    row_dos = ["Adryan", "Loyo", "Mesen"]
    TableRowAdder(table=table, row=row_uno).add()
    TableRowAdder(table=table, row=row_dos).add()

    TablePrinter(table=table).print()