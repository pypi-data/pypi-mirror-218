from pydantic import field_validator
from pydantic.dataclasses import dataclass
from devtools import debug
from enum import Enum
import sys
import os
import re
import pymysql

# from utils.query_builder.mysql import Condition
relative_path = os.getcwd()
sys.path.append(relative_path)
if True:
    from utils.strings import limpiar_string


class Filters(Enum):
    GROUP = 'group'
    ORDER = 'order'


class LogicOperators(Enum):
    IGUAL = '='
    DIFERENTE = '<>'
    MAYOR = '>'
    MENOR = '<'
    MAYORIGUAL = '>='
    MENORIGUAL = '<='
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'


@dataclass
class Condition:
    columna: str
    operador: LogicOperators
    valor: str
    siguiente: LogicOperators | None = None
    negar: bool = False

    # @field_validator('negacion')
    # def validator_negacion(cls, v):
    #     if v not in (LogicOperators.NOT, None):
    #         raise ValueError("Valor inválido")


class QueryBasics:
    def __init__(self,
                 table: str,
                 columns: list[str] | None = None,
                 conditions: list[Condition] | None = None,
                 ) -> None:
        self.columns = [
            limpiar_string(x) for x in columns] if columns is not None else None
        self.table = limpiar_string(table)
        self.conditions = conditions
        self.s_conditions = ''

    def format_columns(self) -> str:
        if self.columns is None:
            return ' * '
        s_columns: str
        s_columns = ", ".join(self.columns)
        return s_columns

    def make_conditions(self) -> str:
        if self.conditions is None:
            return ''
        s_condiciones: str = ' WHERE '
        if self.conditions is None:
            raise ValueError("No se han pasado condiciones.")
        for c in self.conditions:
            s_condicion: str = ''
            if c.negar:
                s_condicion += LogicOperators.NOT.value
            s_condicion += f' {c.columna} {c.operador.value} "{c.valor}" '
            if c.siguiente:
                s_condicion += c.siguiente.value
            s_condiciones += s_condicion

        return s_condiciones

    def make_filters(self, fields: list[str],
                     tipo: str,
                     desc: bool | None = None
                     ) -> str:
        s_filter: str
        s_fields: str = ', '.join(fields)
        if not fields:
            raise ValueError("Debe proporcionar al menos un campo.")
        match tipo:
            case Filters.ORDER.value:
                s_order = ' DESC ' if desc else ' ASC '
                s_filter = ' ORDER BY ' + s_fields + s_order
            case Filters.GROUP.value:
                s_filter = ' GROUP BY ' + s_fields
            case _:
                raise ValueError("No se ha proporcionado un tipo de filtro.")
        return s_filter


class Select(QueryBasics):
    def __init__(self,  table: str,
                 columns: list[str] | None = None,
                 group: list[str] | None = None,
                 order: list[str] | None = None,
                 conditions: list[Condition] | None = None,
                 #  filter_fields: list[str] | None = None,
                 #  filter_type: str | None = None,
                 desc: bool | None = None,
                 ) -> None:
        super().__init__(table, columns, conditions)
        self.order = [
            limpiar_string(x) for x in order] if order is not None else None
        self.group = [
            limpiar_string(x) for x in group] if group is not None else None
        self.desc = desc

    @property
    def string(self):
        s_query: str
        s_columnas = self.format_columns() if self.columns is not None else ' * '

        if self.group is None:
            s_group = ''
        else:
            s_group = self.make_filters(self.group, Filters.GROUP.value)

        if self.order is None:
            s_order = ''
        else:
            s_order = self.make_filters(
                self.order, Filters.ORDER.value, self.desc)

        s_query = f'SELECT {s_columnas} FROM {self.table} {self.make_conditions()} {s_group} {s_order};'

        return re.sub(r'\s{2,}', ' ', s_query)

    def ejecutar(self):
        ...


class Delete(QueryBasics):
    def __init__(self, table: str, conditions: list[Condition] | None = None) -> None:
        super().__init__(table, None, conditions)

    @property
    def string(self):
        s_query: str = f'DELETE FROM {self.table} {self.make_conditions()};'
        return re.sub(r'\s{2,}', ' ', s_query)


class Insert(QueryBasics):
    def __init__(self,
                 table: str,
                 columns: list[str],
                 values: list[list],
                 ) -> None:
        super().__init__(table, columns)
        self.values = values

    def format_values(self) -> str:
        s_values: str
        if self.values is None:
            raise ValueError("Debe ingresar valores para insertar.")
        n_cant_cols = len(self.columns) if self.columns else 0
        if not all(len(x) == n_cant_cols for x in self.values):
            debug(n_cant_cols)
            raise ValueError(
                "Verifique la cantidad de valores proporcionados con la cantidad de columnas.")

        s_values: str = ''
        for value in self.values:
            s_value: str = ' ( '
            s_value += ', '.join(value)
            s_value += ' ), '
            s_values += s_value
        return s_values[:len(s_values)-2]  # quito espacio y última coma

    @property
    def string(self):
        s_query: str
        s_columns: str = self.format_columns()
        s_values: str = self.format_values()
        s_query = f'INSERT INTO {s_columns} VALUES {s_values};'

        return re.sub(r'\s{2,}', ' ', s_query)


class Update(QueryBasics):
    def __init__(self,
                 table: str,
                 column_values: list[list[str]],
                 conditions: list[Condition] | None = None,
                 ) -> None:
        super().__init__(table, None, conditions)
        self.values = column_values
        self.column_values = column_values

    def format_set(self) -> str:
        s_format_set: str = ''
        for c, v in self.column_values:
            s_format_set += f' {c} = "{v}", '
        # quito espacio y última coma
        return s_format_set[:len(s_format_set)-2]

    @property
    def string(self):
        s_query: str = f'UPDATE {self.table} SET {self.format_set()}'
        return re.sub(r'\s{2,}', ' ', s_query)


# * ===========================================================================
# tabla = input('ingrese tabla')

tabla = 'auth_user'
columnas = ['id', 'username']
order = ['nombre']
desc = True
valores = [['Iván', 'Sayavedra'], ['Adrián', 'Ramírez']]
valores2 = [['col1', 'valor1'], ['col2', 'val2']]
# condiciones = ('nombre', 'igual', 'Iván')
condiciones: list[Condition]

condiciones = [
    Condition('nombre', LogicOperators.IGUAL,
              'Iván', LogicOperators.AND),
    Condition('nombre',
              LogicOperators.DIFERENTE, 'Adrián'),
]


query = Update(tabla, valores2, conditions=condiciones).string
# query = Insert(tabla, columnas, valores)

print('')
debug(query)
print('')
# conexion_data = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': 'root01',
#     'db': 'wpruebas',
#     'port': 3306
# }

# conexion = pymysql.connect(**conexion_data)
# cursor = conexion.cursor()


# cursor.execute(query)

# for id, username in cursor.fetchall():
#     print(f'Usuario: {id} {username}')

# conexion.close()
