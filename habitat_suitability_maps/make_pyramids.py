import os
import re
import xarray as xr
import dask.array as da
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from ndpyramid import pyramid_resample
from resampling.make_global import expand_to_global_coverage
import resampling
from resampling.object_store import ObjectStore

print(resampling.__version__)

if __name__ == "__main__":

    source_dir = ("//fs/SHARED/onderzoek/6. Marine Observation Center/Projects"
                  "/MarcoBolo/WP5_T5.1.2/maps/")

    source_files = [os.path.join(source_dir, file) for file in
                    os.listdir(source_dir)]

    my_store = resampling

    for file in source_files:
        # check file
        # ----------
        basename = os.path.splitext(os.path.basename(file))[0]
        parts = re.split("_", basename)
        aphia = parts[1]
        model = parts[2]
        period = "_".join(parts[3:])
        period = re.sub(r'_v\d+_\d+$', '', period)
        print(f"Aphia: {aphia}, Model: {model}, Period: {period}")

        # open dataset
        # ------------
        ds = xr.open_dataset(file)

        # make global
        # -----------
        ds = expand_to_global_coverage(ds, 0.083333, 0.083333)
        ds.rio.write_crs("EPSG:4326", inplace=True)
        ds = ds.drop_vars('crs')

        if not isinstance(ds['HS'].data, da.core.Array):
            # Convert data to a dask array if it's not already chunked
            ds['HS'] = ds['HS'].chunk(
                {'time': 1, 'latitude': 100, 'longitude': 100})
        print(ds)
        HS = ds['HS']

        resampled_pyramid = pyramid_resample(ds,
                                             x="longitude",
                                             y="latitude",
                                             levels=6,
                                             resampling="nearest")

        my_store.write_zarr(resampled_pyramid,
                            name=f"marcobolo/viewer/{name}.zarr")

