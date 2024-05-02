import click
import logging
import pandas as pd
import joblib
from sklearn.model_selection import KFold, cross_validate

from src_train.preprocessing import Process_for_model, Process_all_dataset
from src_train.models import Random_forest_reg
from src_train.cleaning import clean



# run with:
# python3 random_forest.py --path_raw=..\0-Resources\raw.csv --path_clean=..\0-Resources\clean.csv --path_encoder=..\0-Resources\encoder.pkl --path_scaler=..\0-Resources\scaler.pkl --path_model=..\0-Resources\model.pkl 

@click.command()
@click.option("--path_raw", help="Path to the raw CSV")
@click.option("--path_clean", help="Path to save the clean CSV")
@click.option("--path_encoder", help="Path to save the model encoder")
@click.option("--path_scaler", help="Path to save the model scaler")
@click.option("--path_model", help="Path to save the model")
def make_model(path_raw, path_clean, path_encoder,path_scaler,path_model):

    categorical = ["district","state_construction"]
    logging.info("Cleaning the raw data...")
    clean(infile = path_raw, outfile = path_clean)

    logging.info("Reading clean data for model...")
    file = path_clean
    df = pd.read_csv(file)

    # Shuffle DF because its ordered per price, and this breaks cross validation
    df = df.sample(frac=1).reset_index(drop=True)

    logging.info("Preprocessing data...")
    # Split in feature/target and training set/test set
    X = df.drop(columns=["price"])
    y = df['price']     
    
    prepro_split = Process_for_model(X = X, y = y, categorical= categorical, )

    X_train = prepro_split.X_train 
    X_test = prepro_split.X_test
    y_train = prepro_split.y_train
    y_test = prepro_split.y_test
    columns_onehot =prepro_split.columns_onehot

    
    prepro_split.export_encoder(path_encoder=path_encoder)
    prepro_split.export_scaler(path_scaler=path_scaler)

    prepro_all = Process_all_dataset(X = X, y = y, categorical= categorical)
    y = prepro_all.y
    X = prepro_all.X


    logging.info("Training the model...")
    rd_forest = Random_forest_reg(X_train= X_train, X_test= X_test, y_train= y_train, y_test= y_test)
    forest_metrics = rd_forest.metrics  
    logging.info("Printing results...")

    columns = ["model", "r2_train", "r2_test", "rmse_train", "rmse_test", "mae_train", "mae_test"]
    data = forest_metrics
    
    
    print(f"Data mean {round(pd.Series(y).mean(),2)}")
    print(f"Data variance {round(pd.Series(y).var())}")
    print(f"Data std {round(pd.Series(y).std(),2)}")
    
    df_metrics = pd.DataFrame([data], columns = columns)  

    print(df_metrics)

    # Doing a cross validation  
      
    scores = ('r2', 'neg_root_mean_squared_error', 'neg_mean_absolute_error')
    cross_validation = cross_validate(rd_forest.model, X, y, scoring= scores, cv=5)
    print (f"Cross validation, mean R2: {round(abs(cross_validation['test_r2'].mean()),2)}")
    print (f"Cross validation, mean RMSE: {round(abs(cross_validation['test_neg_root_mean_squared_error'].mean()),2)}")
    print (f"Cross validation, mean MAE: {round(abs(cross_validation['test_neg_mean_absolute_error'].mean()),2)}")

    logging.info("Exporting model...")
    joblib.dump(rd_forest.model, path_model)
    

if __name__ == '__main__':
    make_model()
