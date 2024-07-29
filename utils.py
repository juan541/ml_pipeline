from prefect import task
from dotenv import load_dotenv
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from skops.io import dump
from snowflake.connector import connect
import os
import pandas as pd


load_dotenv()

@task
def snowflake_connection():
    """
    Establishes a connection to Snowflake and returns the connection object.
    """
    try:
        # Create a connection object
        print("connecting to snowflake...")
        conn = connect(
            user=os.getenv("SN_USERNAME"),
            password=os.getenv("SN_PASSWORD"),
            account=os.getenv("SN_ACCOUNT"),
            warehouse=os.getenv("SN_WAREHOUSE"),
            database=os.getenv("SN_DB"),
            schema=os.getenv("SN_SCHEMA"),
            role=os.getenv("SN_ROLE")
        )
        print("Connection to Snowflake established successfully")
        return conn
    
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
        raise e

@task
def extract_sn_data(conn):
    """
    Runs a query to fetch all data from ML_IRIS_FLOWER table and returns it as a Pandas DataFrame.

    Parameters
    ----------
    connection : snowflake connection

    Returns
    -------
    df
        resulting dataframe
    """
    query = "SELECT * FROM ML_IRIS_FLOWER;"
    try:
        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query)
        # Fetch the results into a Pandas DataFrame
        df = cursor.fetch_pandas_all()

        # Rename columns to lowercase
        df.columns = [col.lower() for col in df.columns]

        print("Data fetched successfully")
        return df
    except Exception as e:
        print(f"Failed to run query: {e}")
        raise e
    
@task
def extract_data():
    iris = load_iris()
    iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    return iris_df
@task
def cleaning(df: pd.DataFrame):
    """_summary_

    Parameters
    ----------
    df : pd.DataFrame
        dataframe to be cleaned

    Returns
    -------
    pd.DataFrame
        cleaned dataframe
    """
    try:
        # Handling missing values
        print("cleaning data...")
        if df.isnull().values.any():
            df = df.dropna()  # Drop rows with missing values
        
        # Removing duplicates
        df = df.drop_duplicates()
        
        # Ensuring correct data types for features
        for col in df.columns[:-1]:  # Assuming the last column is the target
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Ensuring the target column is categorical
        df['species'] = df['species'].astype('category')

        return df
    except Exception as e:
        print(f"Failed to clean data: {e}")
        raise e
@task
def preprocessing(df: pd.DataFrame):
    """_summary_

    Parameters
    ----------
    df : pd.DataFrame

    dataframe to preprocess

    Returns
    -------
    df
        dataframe ready for training
    """
    try:
        # Scales the feature values using StandardScaler.
        print("standardize data...")
        scaler = StandardScaler()
        df[df.columns[:-1]] = scaler.fit_transform(df[df.columns[:-1]])

        # Encodes the target variable (species) to numeric values.
        print("encoding labels...")
        le = LabelEncoder()
        df['species'] = le.fit_transform(df['species'])

        # Split the data into training and test sets
        # Split the data into features and target
        X = df[df.columns[:-1]]  # Features
        y = df['species']        # Target
        print("splitting data...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        

        return X_train, X_test, y_train, y_test
    except Exception as e:
            print(f"Failed to preprocess data: {e}")
            raise e
@task
def training(X_train, y_train):
    try:
        # Define the parameter grid to tune the hyperparameters
        param_grid = {
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        dtree_reg = DecisionTreeRegressor(random_state=42) # Initialize a decision tree regressor
        grid_search = GridSearchCV(estimator=dtree_reg, param_grid=param_grid, 
                                cv=5, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)
        model = grid_search.best_estimator_ 

        return model
    except Exception as e:
        print(f"Failed totrain model: {e}")
        raise e
@task
def evaluate_model(y_test, prediction: pd.DataFrame):
    try:
        accuracy = accuracy_score(y_test, prediction)
        f1 = f1_score(y_test, prediction, average="macro")

        print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))  
    except Exception as e:
        print(f"Failed to run evaluate: {e}")
        raise e

@task
def get_prediction(X_test, model: DecisionTreeRegressor):
    try:
        prediction = model.predict(X_test).astype(int)
        return prediction
    except Exception as e:
        print(f"Failed run inference: {e}")
        raise e

@task
def save_model(model: DecisionTreeRegressor):
    try:
        dump(model, "models/iris_model.skops")
    except Exception as e:
        print(f"Failed save model: {e}")
        raise e