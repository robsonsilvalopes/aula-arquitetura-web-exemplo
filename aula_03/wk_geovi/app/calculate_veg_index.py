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

load_dotenv()


class VegetativeIndexProcessor:
    file = None
    src_crs = None
    kwargs = None
    red_transform = None
    start_date = None
    end_date = None
    cloud = None

    def __init__(self, username, password):
        print("-> Configuração da API Sentinel")
        
        self.api = SentinelAPI(username, password, "https://apihub.copernicus.eu/apihub")

    def set_date(self, start_date, end_date):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")

    def set_file(self, file):
        self.file = file

    def set_cloud(self, value):
        self.cloud = int(value)

    def crop_area(self):
        with open(self.file) as file:
            data = json.load(file)

        # Captura as coordenadas
        coords = data["features"][0]["geometry"]["coordinates"][0]

        # Converte para o padrão polygon
        polygon = Polygon(coords)

        footprint = geojson_to_wkt(polygon.__geo_interface__)

        products = self.api.query(
            footprint,
            date=(self.start_date, self.end_date),
            platformname="Sentinel-2",
            processinglevel="Level-2A",
            cloudcoverpercentage=(0, self.cloud),
        )

        products_gdf = self.api.to_geodataframe(products)
        products_gdf = products_gdf.sort_values(
            ["cloudcoverpercentage"], ascending=[True]
        )

        products_gdf = products_gdf.head(1)
        product_id = products_gdf.index.values[0]

        path_filter_band_04 = make_path_filter(f"*_B04_10m.jp2")
        path_filter_band_08 = make_path_filter(f"*_B08_10m.jp2")

        print("-> Download das bandas")
        self.api.download(product_id, nodefilter=path_filter_band_04)
        self.api.download(product_id, nodefilter=path_filter_band_08)

        band_04_file = glob.glob("**/*_B04_10m.jp2", recursive=True)
        band_08_file = glob.glob("**/*_B08_10m.jp2", recursive=True)

        # Extrair as coordenadas do anel externo do polígono
        exterior_coords = polygon.exterior.coords

        # Define o sistema de referência espacial da imagem raster
        with rasterio.open(band_04_file[0]) as src:
            dst_crs = src.crs

        # Define o sistema de referência espacial das coordenadas do polígono (WGS84)
        self.src_crs = pyproj.CRS.from_epsg(4326)

        # Transforma as coordenadas do polígono para o mesmo SRS da imagem raster
        transformed_coords = transform_geom(
            self.src_crs, dst_crs, {"type": "Polygon",
                                    "coordinates": [exterior_coords]}
        )

        print("-> Cortando a imagem")
        with rasterio.open(band_04_file[0]) as red:
            with rasterio.open(band_08_file[0]) as nir:
                self.kwargs = red.meta.copy()

                red_crop, self.red_transform = mask(
                    red,
                    [transformed_coords],
                    invert=False,
                    crop=True,
                    nodata=0,
                    filled=True,
                )
                nir_crop, _ = mask(
                    nir,
                    [transformed_coords],
                    invert=False,
                    crop=True,
                    nodata=0,
                    filled=True,
                )

                # Pequena constante para evitar divisões por zero
                epsilon = 1e-6

                return red_crop, nir_crop, epsilon

    def plot(self, index):
        print("-> Exibindo imagem")
        plot.show(index)

    def save(self, index, name):
        print(f'-> Salvando imagem "{name}.tiff"')
        self.kwargs.update(
            {"driver": "GTiff", "count": 1, "compress": "lzw", "crs": "EPSG:4326"}
        )

        _, height, width = index.shape

        # Salvar a matriz em um arquivo tiff
        with rasterio.open(
            f"{name}.tiff",
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=1,
            dtype=np.float32,
            crs=self.src_crs,
            transform=self.red_transform,
            nodata=None,
        ) as dst:
            dst.write(index)

        print("-> Salvamento concluído")

    def calculate_ndvi(self):
        red, nir, epsilon = self.crop_area()

        ndvi = (nir - red) / (nir + red + epsilon)

        return ndvi

    def calculate_msavi(self):
        red, nir, _ = self.crop_area()

        msavi = (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2

        return msavi
