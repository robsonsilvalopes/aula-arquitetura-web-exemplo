# from distutils.command.config import config

from flask import request
import urllib.request
import re
import json
import logging


    
def operacao(operando1,operando2,operador):
    texto = '';

    operando1 = int(operando1)
    operando2 = int(operando2)

    if (operador == '+'):
        texto = str(operando1) + " + " + str(operando2)
        resultado = operando1 + operando2
    elif (operador == '*'):
        texto = str(operando1) + " * " + str(operando2)
        resultado = operando1 * operando2
    elif (operador == '-'):
        texto = str(operando1) + " - " + str(operando2)
        resultado = operando1 - operando2

    # time.sleep(20)

    return {
        'operacao' : texto,
        'resultado' : resultado
    }
    
    return True
