import unicodedata


def remover_acentos(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def limpiar_string(input_str):
    str = input_str.replace(" ", "").lower()
    nfkd_form = unicodedata.normalize('NFKD', str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
