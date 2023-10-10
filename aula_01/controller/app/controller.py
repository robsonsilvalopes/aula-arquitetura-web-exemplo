import connexion
from flask import jsonify, abort, request

from datetime import timedelta
from datetime import datetime


from distutils.command.config import config
import os
import time



   
def operacao():

    operando1 = int(request.form['operando1'])
    operando2 = int(request.form['operando2'])
    operador = request.form['operador']

    texto = '';

    if (operador == '+'):
        texto = str(operando1) + " + " + str(operando2)
        resultado = operando1 + operando2
    elif (operador == '*'):
        texto = str(operando1) + " * " + str(operando2)
        resultado = operando1 * operando2
    elif (operador == '-'):
        texto = str(operando1) + " - " + str(operando2)
        resultado = operando1 - operando2

    time.sleep(20)

    return {
        'operacao' : texto,
        'resultado' : resultado
    }