import datetime

def obter_dia_atual():
    data_atual = datetime.date.today()
    return data_atual.day

def obter_mes_atual():
    data_atual = datetime.date.today()
    return data_atual.month

def obter_ano_atual():
    data_atual = datetime.date.today()
    return data_atual.year

def obter_hora_atual():
    hora_atual = datetime.datetime.now().time()
    return hora_atual.hour

def obter_minuto_atual():
    hora_atual = datetime.datetime.now().time()
    return hora_atual.minute

def obter_segundo_atual():
    hora_atual = datetime.datetime.now().time()
    return hora_atual.second