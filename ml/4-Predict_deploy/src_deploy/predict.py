import pandas as pd
import json
import joblib
import warnings



class Predict:
    def __init__(self, data, encoder, scaler, model):
        #Supress warning "has feature names, but StandardScaler was fitted without feature names"
        #Since it doesnt affect the calculation
        
        file_enc = encoder
        file_scaler = scaler
        file_model = model
        
        warnings.filterwarnings("ignore")

        categorical = ["district","state_construction"]

        X = pd.DataFrame(data, index=[0])
  


        # Encodes new data with saved encoding from train set        
        loaded_enc = joblib.load(file_enc)

        enctransform = loaded_enc.transform(X[categorical])
        X = pd.concat([X, enctransform], axis = 1).drop(categorical, axis = 1)



        # Scales new data with saved scaler from train set
        loaded_scaler = joblib.load(file_scaler)
        X = loaded_scaler.transform(X)


        # Loads and use model to predict new price
        loaded_model = joblib.load(file_model)     
    
        self.result = loaded_model.predict(X)[0]
        

