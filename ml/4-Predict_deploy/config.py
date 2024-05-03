import glob
import os

# Gets latest files from the Resources, to be used in deploym
list_csv = glob.glob('../0-Resources/clean_*.csv') 
latest_clean = max(list_csv, key=os.path.getctime)

list_model = glob.glob('../0-Resources/model_*.pkl') 
latest_model = max(list_model, key=os.path.getctime)

encoder = '../0-Resources/encoder.pkl'
scaler = '../0-Resources/scaler.pkl'
