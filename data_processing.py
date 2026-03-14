import pandas as pd

def load_data():

    df = pd.read_csv("DataCoSupplyChainDataset.csv", encoding="latin1")

    # clean column names
    df.columns = df.columns.str.replace(" ", "_")

    return df