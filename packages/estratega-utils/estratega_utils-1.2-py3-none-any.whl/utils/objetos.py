from typing import Any
from devtools import debug
from pydantic import BaseModel, create_model
from pydantic.dataclasses import dataclass
from enum import Enum


class Obj:
    '''
        Esta clase permite pasarle un diccionario como parámetro para tratarlo como 
        un objeto y acceder a sus elementos con la notación de punto, además de 
        utilizarlo dentro de un contexto con "with".
    '''

    def __init__(self, d):
        self.d = d

    def __enter__(self):
        Campos = {k: (type(v), ...) for k, v in self.d.items()}
        DiccionarioComoObjeto = create_model(
            'DiccionarioComoObjeto', **Campos)  # type:ignore
        self.o = DiccionarioComoObjeto(**self.d)
        return self.o

    def __exit__(self, exc_type, exc_value, traceback):
        ...
