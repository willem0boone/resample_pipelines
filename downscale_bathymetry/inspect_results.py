import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

my_zarr = "https://minio.lab.dive.edito.eu/oidc-willemboone/downscaled/bathymetry_res_0dot05.zarr"

ds = xr.open_zarr(my_zarr)
print(ds)

# Extract elevation data
elevation = ds['elevation']
print(elevation)

# Create a plot
plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
elevation.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='terrain', cbar_kwargs={'label': 'Elevation (m)'})

# Add geographic features
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')
ax.add_feature(cfeature.OCEAN)

# Add title and labels
plt.title('Elevation Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()
