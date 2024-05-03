from sklearn.metrics import r2_score, root_mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import pandas as pd



class metrics:
    """Child class used in each model for calculating metrics (R2, RMSE, MAE) as its attributes.
    Takes y train, y test, y predicted from train set and y predicted from test set."""
    def __init__(self, y_train, y_pred_train, y_test, y_pred) -> None:        
        # R2
        self.r2_train = round(r2_score(y_train, y_pred_train),5)
        self.r2_test = round(r2_score(y_test, y_pred),5)
        #RMSE
        self.rmse_train = round(root_mean_squared_error(y_train, y_pred_train),2)
        self.rmse_test = round(root_mean_squared_error(y_test, y_pred),2)

        #MAE (mean absolute error) 
        self.mae_train = round(mean_absolute_error(y_train, y_pred_train),2)
        self.mae_test = round(mean_absolute_error(y_test, y_pred),2)



class Random_forest_reg (metrics):
    def __init__(self, X_train, X_test, y_train, y_test) -> None:
        """Random forest regression: model training, model predicting and metrics.
        Number of trees and samples per leaves are set inside the class (70 trees, 2 samples per leave)."""
        self.name = "Random Forest Regression"
        # Parameters for model, those where tested before with loops to find an optimized range
        trees = 70
        samples = 2

        # Regression
        random_forest_regressor = RandomForestRegressor(n_estimators = trees, min_samples_leaf= samples)
        random_forest_regressor.fit(X_train,y_train)

        # Make predictions
        y_pred= random_forest_regressor.predict(X_test)
        y_pred_train= random_forest_regressor.predict(X_train)

        # Stores metrics as attributes
        super().__init__(y_train, y_pred_train, y_test, y_pred)
        
        # Stores model for exporting later
        self.model = random_forest_regressor
        # Model metrics
        self.metrics = { 
            "model": self.name ,
            "r2_train": self.r2_train, 
            "r2_test" : self.r2_test, 
            "rmse_train": self.rmse_train, 
            "rmse_test": self.rmse_test, 
            "mae_train": self.mae_train, 
            "mae_test": self.mae_test
        }







