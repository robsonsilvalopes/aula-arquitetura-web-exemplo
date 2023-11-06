import connexion
from flask import jsonify, abort, request
from rq.job import Job
from redis_artifacts import redis_conn, redis_queue
from rq import Queue

import numpy as np
import os
import logging


# TODO: passar estas variáveis e códigos de inicialização para o main
# The time (in seconds) a finished job waits at the queue before being disposed

from distutils.command.config import config


import os

# import configuration


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def get_result(job_id):
    logging.info('<controller>  --------------Call rote /get_result ----------------')
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        return {"job_id": job_id, "job_status": 'error'}, 404

    if not job.result: # If not have results, return empty values
        return {'job_id': job.id, 'result': ''}, 404

    return {
            'job_id (Parameter)': job.id,
            'operacao': job.result['operacao'],
            'resultado': job.result['resultado']
        }

def check_status(job_id):
    logging.info('<controller>  --------------Call rote /check_status ----------------')
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        return {"job_id": job_id, "job_status": 'It was not possible to get job'}, 404
    
    return {
        'job_id': job.id, 
        'job_status': job.get_status(),
        }

def executa():
    logging.info('<controller>  --------------Call rote /executa ----------------')
    
    params = {
        'operando1' : request.form['operando1'],
        'operando2' : request.form['operando2'],
        'operador' : request.form['operador']        
    }
    
    q = Queue('math',connection=redis_conn)
    job = q.enqueue('main.operacao', kwargs=params)
   
    return {
        'job_id':job.id,
    }
    
