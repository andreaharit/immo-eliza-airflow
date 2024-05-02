import glob
import os

list_csv = glob.glob('../0-Resources/clean_*.csv') # * means all if need specific format then *.csv
latest_clean = max(list_csv, key=os.path.getctime)

list_model = glob.glob('../0-Resources/model_*.pkl') # * means all if need specific format then *.csv
latest_model = max(list_model, key=os.path.getctime)

encoder = '../0-Resources/encoder.pkl'
scaler = '../0-Resources/scaler.pkl'
