import pandas as pd
import os

DATA_PATH = "data/scores.xlsx"

def save_result(row):
    df = pd.read_excel(DATA_PATH) if os.path.exists(DATA_PATH) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(DATA_PATH, index=False)
