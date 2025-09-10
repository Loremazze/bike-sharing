from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sklearn.model_selection import KFold, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, mean_squared_error, r2_score, mean_absolute_error
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

def execute_regression(regression_method,X,y):
    # Pipeline con scaling + modello
    pipe = Pipeline([
        ('scaling', StandardScaler()),
        ('reg', regression_method)
    ])

    # KFold normale (non stratificato!)
    kf = KFold(n_splits=10, shuffle=True, random_state=21)

    # cross-validation con metriche da regressione
    results_validation = cross_validate(
        pipe,
        X,
        y,
        scoring={
            'r2': make_scorer(r2_score),
            'mse': make_scorer(mean_squared_error),
            'mae': make_scorer(mean_absolute_error)
        },
        cv=kf,
        return_estimator=True,
        n_jobs=-1
    )

    # Mostriamo i risultati
    print("Mean R²: ", np.mean(results_validation['test_r2']))
    print("Mean MSE: ", np.mean(results_validation['test_mse']))
    print("Mean MAE: ", np.mean(results_validation['test_mae']))


def train_model(bike_sharing_dataframe):
    bike_sharing_dataframe_copy = bike_sharing_dataframe.copy()

    # Convert dteday into datetime
    dteday_dt = pd.to_datetime(bike_sharing_dataframe['dteday'])

    # Extract year and month from dteday
    dteday_year = dteday_dt.dt.year
    dteday_month = dteday_dt.dt.month

    # Recall: yr is coded as 0=2011, 1=2012
    yr_decoded = bike_sharing_dataframe['yr'] + 2011

    # Check consistency
    year_match = (dteday_year == yr_decoded).all()
    month_match = (dteday_month == bike_sharing_dataframe['mnth']).all()

    print("Year matches yr column:", year_match)
    print("Month matches mnth column:", month_match)

    bike_sharing_dataframe.drop('instant',axis=1,inplace=True)
    bike_sharing_dataframe.drop('dteday',axis=1,inplace=True)

    # Check if there is any null values
    bike_sharing_dataframe.isnull().values.any()

    # Check the relationship with the target feature
    all(bike_sharing_dataframe['registered'] + bike_sharing_dataframe['casual'] == bike_sharing_dataframe['cnt'])

    bike_sharing_dataframe.drop('casual',axis=1,inplace=True)
    bike_sharing_dataframe.drop('registered',axis=1,inplace=True)

    linaerRegression = LinearRegression()
    y = bike_sharing_dataframe['cnt']
    X = bike_sharing_dataframe.drop('cnt',axis=1)
    execute_regression(linaerRegression,X,y)

    bike_sharing_dataframe["hour_sin"] = np.sin(2 * np.pi * bike_sharing_dataframe["hr"]/24)
    bike_sharing_dataframe["hour_cos"] = np.cos(2 * np.pi * bike_sharing_dataframe["hr"]/24)
    # Rimuovere le colonne originali
    bike_sharing_dataframe.drop("hr",axis=1,inplace=True)
    y_processed = bike_sharing_dataframe['cnt']
    X_processed = bike_sharing_dataframe.drop('cnt',axis=1)
    execute_regression(linaerRegression,X_processed,y_processed)

    bike_sharing_dataframe["weekday_sin"] = np.sin(2 * np.pi * bike_sharing_dataframe["weekday"]/7)
    bike_sharing_dataframe["weekday_cos"] = np.cos(2 * np.pi * bike_sharing_dataframe["weekday"]/7)
    # Rimuovere le colonne originali
    bike_sharing_dataframe.drop("weekday",axis=1,inplace=True)
    y_processed = bike_sharing_dataframe['cnt']
    X_processed = bike_sharing_dataframe.drop('cnt',axis=1)

    bike_sharing_dataframe["month_sin"] = np.sin(2 * np.pi * bike_sharing_dataframe["mnth"]/12)
    bike_sharing_dataframe["month_cos"] = np.cos(2 * np.pi * bike_sharing_dataframe["mnth"]/12)
    # Rimuovere le colonne originali
    bike_sharing_dataframe.drop("mnth",axis=1,inplace=True)
    y_processed = bike_sharing_dataframe['cnt']
    X_processed = bike_sharing_dataframe.drop('cnt',axis=1)
    execute_regression(linaerRegression,X_processed,y_processed)

    # Assicurati che tutte le colonne numeriche siano numeriche
    numerical_cols = bike_sharing_dataframe.select_dtypes(include=['int64', 'float64']).columns

    # Heatmap delle correlazioni
    plt.figure(figsize=(12, 10))
    corr_matrix = bike_sharing_dataframe[numerical_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlazioni tra feature numeriche")
    plt.show()

    bike_sharing_dataframe.drop(columns=['weekday_sin','weekday_cos'],axis=1,inplace=True)
    # Creiamo una nuova colonna 'avg_temp' come media di temp e atemp
    bike_sharing_dataframe["avg_temp"] = bike_sharing_dataframe[["temp", "atemp"]].mean(axis=1)
    bike_sharing_dataframe.drop(columns=['temp','atemp'],axis=1,inplace=True)

    y_processed = bike_sharing_dataframe['cnt']
    X_processed = bike_sharing_dataframe.drop('cnt',axis=1)
    final_pipeline = Pipeline([
        ('scaling', StandardScaler()),
        ('reg', LinearRegression())
    ])

    final_pipeline.fit(X_processed, y_processed)
    print(list(X_processed.columns))

    # Salvataggio
    with open("final_model.pkl", "wb") as f:
        pickle.dump(final_pipeline, f)

