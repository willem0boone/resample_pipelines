import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature


source_dir = ("//fs/SHARED/onderzoek/6. Marine Observation Center/Projects"
              "/MarcoBolo/WP5_T5.1.2/maps/")

source_files = [os.path.join(source_dir, file) for file in os.listdir(source_dir)]


def plot(ds):
    # Extract the 'HS' data variable
    HS = ds['HS']

    # Get spatial extent
    lon = ds['longitude']
    lat = ds['latitude']
    for t in range(HS.shape[0]):  # Loop over the time dimension
        fig, ax = plt.subplots(figsize=(10, 6),
                               subplot_kw={'projection': ccrs.PlateCarree()})
        ax.set_extent([lon.min(), lon.max(), lat.min(), lat.max()],
                      crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAND, facecolor='lightgray')

        # Plot HS data
        im = ax.pcolormesh(lon, lat, HS[t, :, :], shading='auto',
                           transform=ccrs.PlateCarree())
        cbar = plt.colorbar(im, ax=ax, orientation='vertical',
                            label='HS Value')

        ax.set_title(f'Time Step {t + 1} - {str(ds.time[t].values)}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        plt.show()

        if t >= 2:
            break

