from .sentinelhub import SHExplorer
from .utils import create_aoi_geodataframe


def explore_satellite_images(aoi, time_interval, sensor="S2L2A", **kargs):
    gdf = create_aoi_geodataframe(aoi)
    if isinstance(gdf, list):
        return gdf
    explorer = SHExplorer(time_interval, sensor, **kargs)
    results = explorer.search(gdf)
    return results
