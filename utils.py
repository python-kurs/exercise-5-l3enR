# utility functions

# Use this file for all functions you create and might want to reuse later.
# Import them in the `main.py` script

def mean_anomaly(x, lat_min, lat_max, lon_min, lon_max, year):
    """
    Calculates the mean anomaly from the monthly anomaly values.
    
    The single monthly anomalies were calculated and used in a mean function.
    
    Parameters
    ----------
    x       : xarray Dataset
              The original dataset
    lat_min : number
              The minimum latitude extent 
    lat_max : number
              The maximum latitude extent 
    lon_min : number
              The minimum longitude extent 
    lon_max : number
              The maximum longitude extent 
    year    : number
              The requested year        
            
    Returns
    -------
    xarray Dataset
    
    """
    #create a month vector
    import numpy as np
    month = np.arange(1,13)
    
    #create 12 arrays for the 12 month and groupby month
    arrayDict = {}
    
    for i in month:
        if i < 10:
            temp = x.sel(latitude = slice(lat_min,lat_max), longitude = slice(lon_min, lon_max), time = str(year)+"-0"+str(i))
            arrayDict["mon"+str(i)] = temp["tg"].groupby("time.month").mean("time")
        else:
            temp = x.sel(latitude = slice(lat_min,lat_max), longitude = slice(lon_min, lon_max), time = str(year)+"-"+str(i))
            arrayDict["mon"+str(i)] = temp["tg"].groupby("time.month").mean("time")
        
    #sum up the monthly anomalies
    for i in month:
        if i == 1:
            annualSum = arrayDict["mon"+str(i)]
        else:
            annualSum = sum(annualSum, arrayDict["mon"+str(i)]) #use the sum() function because the "+" produce errors 
    
    #divide the result by the number of month    
    anomaly_total = annualSum / 12
    
    return anomaly_total