from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sqlalchemy import create_engine

  
# fetch dataset 
bike_sharing = fetch_ucirepo(id=275) 
  
# data (as pandas dataframes) 
X = bike_sharing.data.features 
y = bike_sharing.data.targets 
  
# metadata 
#print(bike_sharing.metadata) 
  
# variable information 
#print(bike_sharing.variables) 

bike_sharing_dataframe = X.copy()

# Convert to DataFrame
bike_sharing_dataframe = pd.DataFrame(bike_sharing.data, columns=bike_sharing.feature_names)

# If the dataset has targets/labels, you can add them too:
#if bike_sharing.target is not None:
 #   df["target"] = bike_sharing.target

# Show first few rows
print(bike_sharing_dataframe.head())
