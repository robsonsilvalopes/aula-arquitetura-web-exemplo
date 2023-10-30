import connexion
from flask import jsonify, abort, request
from rq.job import Job
from redis_artifacts import redis_conn, redis_queue
from rq import Queue

import numpy as np
import os
import logging

from pathlib import Path
from datetime import timedelta
from datetime import datetime

# TODO: passar estas variáveis e códigos de inicialização para o main
# The time (in seconds) a finished job waits at the queue before being disposed

from distutils.command.config import config


import os

# import configuration


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
UPLOAD_FILE_DIR = '/code/app/tmp'
PLANO_FILE_DIR = '/code/app/files'
Path(UPLOAD_FILE_DIR).mkdir(parents=True, exist_ok=True)

# TODO: passar estas variáveis e códigos de inicialização para o main
# The time (in seconds) a finished job waits at the queue before being disposed
RESULT_TTL = 18000 # 5 hours
# The time (in seconds) a job can execute before being killed 
# By default a job has 180 seconds to complete 
JOB_TIMEOUT = 3600

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

def get_ndvi():
    
    logging.info('<controller>  --------------Call rote /get_NDVI----------------')
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        return {"job_id": job_id, "job_status": 'error'}, 404

    if not job.result: # If not have results, return empty values
        return {'job_id': job.id, 'result': ''}, 404

    return {
            'job_id (Parameter)': job.id,
            'resultado': job.result['resultado']
        }

def calculate_ndvi():  
    
    logging.info('<controller>  --------------Call rote /calculate_NDVI ----------------')

   
    # pega a data atual
    now = datetime.now()

    # cria um timestamp
    timestamp = datetime.timestamp(now)

    #remove o ponto
    timestamp = str(timestamp).replace('.','')

    # cria um link diretório para essa consulta
    plano_path = PLANO_FILE_DIR + "/"+ timestamp

    # criar o diretório
    Path(plano_path).mkdir(parents=True, exist_ok=True)

    logging.info('<controller> path created '+plano_path)
    
    # recebe o arquivo enviado 
    file_pk = connexion.request.files['geojson']
    
    # define o nome do arquivo
    fname = f'{plano_path}/geojson'
    logging.info('<controller> salvando GeoJson file')

    file_pk.save(fname)

    params = {
        'dt_inicio' : request.form['dt_inicio'],
        'dt_fim':request.form['dt_fim'],
        'cobertura':request.form['cobertura'],
        'login':request.form['login'],
        'file_gj':plano_path+'/geojson',
        'pwd':bytes(request.form['pwd'],"utf-8"),
        'geojson':plano_path
        }
    q = Queue('geovi',connection=redis_conn)
    job = q.enqueue('main.calculate_ndvi', result_ttl=RESULT_TTL ,kwargs=params, job_timeout=JOB_TIMEOUT)


    return {
        'jobid': job.id
    }