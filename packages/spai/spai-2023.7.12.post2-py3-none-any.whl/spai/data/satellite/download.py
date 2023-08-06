from .sentinelhub import SHS2L2ADownloader, SHS2L1CDownloader, SHS1Downloader
from .utils import create_aoi_geodataframe
import shutil
import os
import geopandas as gpd

def download_satellite_image(aoi, date, sensor, storage):
    gdf = create_aoi_geodataframe(aoi)
    if isinstance(gdf, gpd.GeoDataFrame):
        download_dir = "/tmp/sentinelhub"
        if sensor == "S2L2A":
            downloader = SHS2L2ADownloader(download_dir)
        elif sensor == "S2L1C":
            downloader = SHS2L1CDownloader(download_dir)
        elif sensor == "S1":
            downloader = SHS1Downloader(download_dir)
        else:
            raise Exception(f"sensor {sensor} not supported")
        dst_path = downloader.download(gdf, date)
        dst_path = storage.create(dst_path, name=f"{sensor}_{date}.tif")
        shutil.rmtree(download_dir)
        return dst_path
    else:
        return gdf