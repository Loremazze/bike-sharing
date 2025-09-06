!pip install ucimlrepo
from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sqlalchemy import create_engine

  
# fetch dataset 
bike_sharing = fetch_ucirepo(id=275) 
  
# data (as pandas dataframes) 
X = bike_sharing.data.features 
y = bike_sharing.data.targets 
  
# metadata 
print(bike_sharing.metadata) 
  
# variable information 
print(bike_sharing.variables) 
