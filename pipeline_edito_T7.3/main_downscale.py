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
         "step": 0.1,
         "invert": True
         },
        {"dimension": "longitude",
         "range": (-10, 40),
         "step": 0.1
         },
    ]

    # -------------------------------------------------------------------------
    # downscale datasets on the fly
    datasets = pd.read_csv("datasets.csv")

    for i, item in enumerate(datasets.itertuples()):
        print(f"working on dataset {i+1} out of  {len(datasets)}: {item}")

        print(item.url)

        ds = xr.open_dataset(item.url, engine='zarr')
        ds_downscaled = down_scale_on_the_fly(
            ds=ds,
            resampler=resampler
        )

        my_store.write_zarr(
            dataset=ds_downscaled,
            name=f"EDITO_DUC2/{item.dataset}.zarr"
        )

    # -------------------------------------------------------------------------
    # downscale big dataset in batches
    print("working on bathymetry")

    url = ("https://s3.waw3-1.cloudferro.com/emodnet/bathymetry/bathymetry_"
           "2022.zarr")
    var = ["elevation"]

    dest_zarr = "EDITO_DUC2/bathymetry.zarr"
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
        **params)

    # -------------------------------------------------------------------------
    print("start plotting")
    # verify datasets by plotting them
    if not os.path.isdir("plots"):
        os.makedirs("plots")

    for item in datasets.itertuples():
        print(item)
        my_s3_ds = my_store.extract_zarr(
            name=f"EDITO_DUC2/{item.dataset}.zarr")

        for time_index in range(len(my_s3_ds.time)):
            data_slice = my_s3_ds.isel(time=time_index)
            time_value = my_s3_ds.time.values[time_index]
            time_value = pd.Timestamp(time_value).year
            plot_dataset(data_slice,
                      var=item.var,
                      name=f"plots/{item.var}_{time_value}.png")

    # plot bathymetry
    my_s3_ds = my_store.extract_zarr(name=f"EDITO_DUC2/bathymetry.zarr")
    plot_dataset(my_s3_ds,
                 var="elevation",
                 name=f"plots/elevation.png")

    # -------------------------------------------------------------------------
    # plot_logs logs
    plot_logs()
