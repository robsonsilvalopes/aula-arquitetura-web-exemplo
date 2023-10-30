from sentinelsat import SentinelAPI, geojson_to_wkt, make_path_filter
from rasterio.warp import transform_geom
from shapely.geometry import Polygon
from rasterio.mask import mask
from dotenv import load_dotenv
from datetime import datetime
from rasterio import plot
import numpy as np
import rasterio
import pyproj
import json
import glob
import os

from calculate_veg_index import VegetativeIndexProcessor


def calculate_ndvi(**params):
    
    # # Instanciando a classe VegetativeIndexProcessor passando as credenciais
    processor = VegetativeIndexProcessor('robsonsilvalopes', 'CUzixj!fg4')

    # # Definindo o arquivo que contém as coordenadas
    processor.set_file(params['file_gj'])

    # # Definindo as datas de início e fim, respectivamente
    processor.set_date(params['dt_inicio'], params['dt_fim'])

    # # Definindo a porcentagem máxima de núvens
    processor.set_cloud(params['cobertura'])

    # # Cálculo do NDVI e salvando em um arquivo tiff
    ndvi = processor.calculate_ndvi()
    processor.save(ndvi, params['file_gj']+"ndvi")

    # # Cálculo do MSAVI e salvando em um arquivo tiff
    # msavi = processor.calculate_msavi()
    # processor.save(msavi, "msavi")

    # # Exibindo na tela usando a função 'plot'
    # processor.plot(ndvi)
    # processor.plot(msavi)

    return {
        'resultado' : 'ok'
    }