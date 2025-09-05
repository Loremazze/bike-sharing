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

# Load dataset
df = pd.read_csv("hour.csv")

# Create connection (edit credentials)
engine = create_engine("postgresql://username:password@localhost:5432/mydatabase")

# Save to PostgreSQL
df.to_sql("bike_sharing", engine, if_exists="replace", index=False)
