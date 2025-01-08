import os.path
import xarray as xr
import pandas as pd

from resampling.plot_logs import plot_logs
from resampling.my_store import store_from_config
from resampling.plot_zarr import plot_dataset
from resampling.down_scale import down_scale_in_batches
from resampling.down_scale import down_scale_on_the_fly

import faulthandler


if __name__ == "__main__":
    faulthandler.enable()

    # initiate store
    my_store = store_from_config(config_file="config.toml")

    # Resampling specifications
    resampler = [
        {"dimension": "latitude",
         "range": (30, 70),
         "step": 0.05,
         "invert": True
         },
        {"dimension": "longitude",
         "range": (-10, 40),
         "step": 0.05
         },
    ]

    # -------------------------------------------------------------------------
    # downscale big dataset in batches
    print("working on bathymetry")

    url = ("https://s3.waw3-1.cloudferro.com/emodnet/bathymetry/bathymetry_"
           "2022.zarr")
    var = ["elevation"]

    dest_zarr = "downscaled/bathymetry_res_0dot05.zarr"
    ds = xr.open_zarr(url)

    params = {"resampler": resampler,
              "workers": 50,
              "batch_size": 500
              }
    down_scale_in_batches(
        my_store=my_store,
        ds=ds,
        dest_zarr=dest_zarr,
        variables=var,
        over_write=False,
        start_batch=900,
        **params)

    # -------------------------------------------------------------------------
    # plot_logs logs
    plot_logs()
