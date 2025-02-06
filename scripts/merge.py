import pandas as pd
import glob
from typing import List
import csv

#load subsets into dataframes
def load_data() -> List[pd.DataFrame]:
    data_subsets = glob.glob("data/*.csv") + glob.glob("data/*.xlsx")
    return [(pd.read_csv(data_subset, encoding="latin1", sep=None, engine="python", quoting=csv.QUOTE_NONE, on_bad_lines="skip"), data_subset.split(".")[0]) if data_subset.endswith(".csv") else pd.read_excel(data_subset) for data_subset in data_subsets]


#merge subsets
def merge_data(data_subsets: List[tuple]) -> pd.DataFrame:
    seen_rows = {}
    mid_counter = 1
    
    for df, name in data_subsets:
        print(f"Processing {name}")
        
        key_columns = [col for col in ['title', 'abstract', 'doi'] if col in df.columns]
        df = df.copy()
        
        if not key_columns:
            continue
            # raise ValueError("At least one of 'title', 'abstract', or 'doi' must be present in each DataFrame.")
        
        df['Source_' + name] = 1
        
        for _, row in df.iterrows():
            row_key = tuple(row[col] for col in key_columns)
            
            if row_key not in seen_rows:
                row_dict = row.to_dict()
                row_dict['MID'] = f'M{mid_counter}'
                mid_counter += 1
                seen_rows[row_key] = row_dict
            else:
                seen_rows[row_key]['Source_' + name] = 1
    
    final_df = pd.DataFrame(seen_rows.values()).fillna(0)
    
    return final_df


def main():
    sets = load_data()
    merged = merge_data(sets)
    merged.to_csv("data/merged.csv", index=False)
    

if __name__ == "__main__":
    main()