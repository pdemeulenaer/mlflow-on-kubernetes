# Importing in necessary libraries
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import ElasticNet
import mlflow
import mlflow.sklearn



# PROJECT SETUP
# ------------------------------------------------------------------------------
# Setting the MLflow tracking server
mlflow.set_tracking_uri('http://mlflow-server.local')


# Setting the requried environment variables
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://mlflow-minio.local/'
os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123'

# Loading data from a CSV file
df_wine = pd.read_csv('train.csv')

# Separating the target class ('quality') from remainder of the training data
X = df_wine.drop(columns = 'quality')
y = df_wine[['quality']]

# Splitting the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, random_state = 42)
