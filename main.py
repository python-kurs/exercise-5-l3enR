# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

input_dir  = Path("data")
output_dir = Path("solution")

# 1. Go to http://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
#    and download the 0.25 deg. file for daily mean temperature.
#    Save the file into the data directory but don't commit it to github!!! [2P]

# 2. Read the file using xarray. Get to know your data. What's in the file?
#    Calculate monthly means for the reference periode 1981-2010 for Europe (Extent: Lon_min:-13, Lon_max: 25, Lat_min: 30, Lat_max: 72). [2P]

data_dir = input_dir / "tg_ens_mean_0.25deg_reg_v19.0e.nc"
data = xr.open_dataset(data_dir)

ref_dat = data.sel(latitude = slice(30,72), longitude = slice(-13,25), time = slice("1981-01-01","2010-12-31"))

monMean = ref_dat["tg"].groupby("time.month").mean("time")

# 3. Calculate monthly anomalies from the reference period for the year 2018 (use the same extent as in #2).
#    Make a quick plot of the anomalies for the region. [2P]

anomaly = data.sel(latitude = slice(30,72), longitude = slice(-13,25), time = "2018")
anomaly = anomaly["tg"].groupby("time.month").mean("time")

#anomaly = 2018 - monMean
anomaly = anomaly - monMean
anomaly.plot(x = "longitude", col = "month", col_wrap = 3)

# 4. Calculate the mean anomaly for the year 2018 for Europe (over all pixels of the extent from #2) 
#    Compare this overall mean anomaly to the anomaly of the pixel which contains Marburg. 
#    Is the anomaly of Marburg lower or higher than the one for Europe? [2P] 

from utils import mean_anomaly

mean_ano_18 = mean_anomaly(x = data, lat_min = 30, lat_max = 72, lon_min = -13, lon_max = 25, year = 2018)

#Marburg = 50.85/8.77
#umschließendes Pixel: (50.75 - 51 / 8.75 - 9)
mr_anomaly = mean_anomaly(x = data, lat_min = 50.75, lat_max = 51, lon_min = 8.75, lon_max = 9, year = 2018)

# 5. Write the monthly anomalies from task 3 to a netcdf file with name "europe_anom_2018.nc" to the solution directory.
#    Write the monthly anomalies for Marburg to a csv file with name "marburg_anom_2018.csv" to the solution directory. [2P]
anomaly.to_netcdf("solution/europe_anom_2018.nc")

mr_anomaly = mr_anomaly.to_dataframe()
mr_anomaly.to_csv("solution/marburg_anom_2018.csv")
