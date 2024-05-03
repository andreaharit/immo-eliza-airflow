import click
import pandas as pd
import joblib
from sklearn.model_selection import KFold, cross_validate

from src_train.preprocessing import Process_for_model, Process_all_dataset
from src_train.models import Random_forest_reg
from src_train.cleaning import clean
from datetime import datetime
import json


@click.command()
@click.option("--path_raw", help="Path to the raw CSV")
@click.option("--path_clean", help="Path to save the clean CSV")
@click.option("--path_encoder", help="Path to save the model encoder")
@click.option("--path_scaler", help="Path to save the model scaler")
@click.option("--path_model", help="Path to save the model")
@click.option("--path_metrics", help="Path to the json file to print metrics")
def make_model(path_raw, path_clean, path_encoder,path_scaler,path_model, path_metrics):

    # States which metrics are categorical for the model traning/one-hot encoding
    categorical = ["district","state_construction"]

    print("Cleaning the raw data...")
    clean(infile = path_raw, outfile = path_clean)

    print("Reading cleaned data for model...")
    file = path_clean
    df = pd.read_csv(file)

    # Shuffle DF because its ordered per price, and this breaks cross validation
    df = df.sample(frac=1).reset_index(drop=True)

    print("Preprocessing data...")
    # Split in feature/target and training set/test set
    X = df.drop(columns=["price"])
    y = df['price']     
    
    prepro_split = Process_for_model(X = X, y = y, categorical= categorical, )

    X_train = prepro_split.X_train 
    X_test = prepro_split.X_test
    y_train = prepro_split.y_train
    y_test = prepro_split.y_test
    columns_onehot =prepro_split.columns_onehot

    # Export scaler and encoder picke files
    prepro_split.export_encoder(path_encoder=path_encoder)
    prepro_split.export_scaler(path_scaler=path_scaler)

    # Preprocess full data, for cross validation
    prepro_all = Process_all_dataset(X = X, y = y, categorical= categorical)
    y = prepro_all.y
    X = prepro_all.X

    print("Training the model...")
    rd_forest = Random_forest_reg(X_train= X_train, X_test= X_test, y_train= y_train, y_test= y_test)

    print("Exporting model...")
    joblib.dump(rd_forest.model, path_model)

    print("Writing metric results into file...")


    today = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")   

    # Data metrics
    data_metrics = {
        "number_rows" : X.shape[0],
        "data_mean" : round(pd.Series(y).mean(),2),
        "data_variance" : round(pd.Series(y).var()),
        "data_std" : round(pd.Series(y).std(),2)
    }
    # Cross validation metrics
    scores = ('r2', 'neg_root_mean_squared_error', 'neg_mean_absolute_error')
    cross_validation = cross_validate(rd_forest.model, X, y, scoring= scores, cv=5)
    
    cross_metrics = {    
    "mean_r2" : round(abs(cross_validation['test_r2'].mean()),2),
    "mean_RMSE" : round(abs(cross_validation['test_neg_root_mean_squared_error'].mean()),2),
    "mean_MAE" : round(abs(cross_validation['test_neg_mean_absolute_error'].mean()),2)
    }

    # Model metrics
    model_metrics = rd_forest.metrics

    # Dumps metrics into a jsonfile   
    information = {today: {"data": data_metrics, "model":model_metrics, "cross validation": cross_metrics}}


    with open(path_metrics , "a") as file:
        file.write(json.dumps(information, indent=4))


if __name__ == '__main__':
    make_model()
