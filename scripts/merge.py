import pandas as pd
import glob

#load subsets into dataframes
def load_data():
    data_subsets = glob.glob("data/.csv") + glob.glob("data/.xlsx")
    return [pd.read_csv(data_subset) if data_subset.endswith(".csv") else pd.read_excel(data_subset) for data_subset in data_subsets]
