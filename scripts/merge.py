import pandas as pd
import glob
from typing import List
import csv
import requests
import time
import chardet
from tqdm import tqdm

#load subsets into dataframes
def load_data() -> List[pd.DataFrame]:
    data_subsets = glob.glob("data/*.csv") + glob.glob("data/*.xlsx")
    return [(enrich_data(data_subset), data_subset.split(".")[0]) for data_subset in data_subsets]

def fetch_openalex_data(doi):
    """Fetch title and abstract from OpenAlex using DOI."""
    base_url = "https://api.openalex.org/works/https://doi.org/"
    url = f"{base_url}{doi}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Title not found")
            abstract_index = data.get("abstract_inverted_index", {})
            
            # Convert OpenAlex abstract format to readable string
            if abstract_index:
                abstract = " ".join(sorted(abstract_index.keys(), key=lambda k: min(abstract_index[k])))
            else:
                abstract = "Abstract not found"
            
            return title, abstract
        else:
            return "Title not found", "Abstract not found"
    except requests.RequestException:
        return "Title not found", "Abstract not found"


def enrich_data(data_subset: str) -> pd.DataFrame:
    with open(data_subset, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']

    if data_subset.endswith(".xlsx"):
        df = pd.read_excel(data_subset)
    else:
        df = pd.read_csv(data_subset, encoding=encoding)
    df.columns = df.columns.str.lower()
    if not all(col in df.columns for col in ['title', 'abstract', 'doi']):
        titles, abstracts = [], []
        for doi in tqdm(df['doi'], desc="Fetching OpenAlex Data", unit="DOIs"):
            title, abstract = fetch_openalex_data(doi)
            titles.append(title)
            abstracts.append(abstract)
        
        df['title'] = titles
        df['abstract'] = abstracts
        df.to_csv(data_subset, index=False)
        return df
    else:
        return df


def merge_data(data_subsets: List[tuple]) -> pd.DataFrame:
    seen_rows = {}
    mid_counter = 1
    
    for df, name in data_subsets:
        print(f"Processing {name}")
        
        key_columns = [col for col in ['title', 'abstract', 'doi'] if col in df.columns]
        df = df.copy()
        
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
    
    final_df = pd.DataFrame(seen_rows.values())

    first_columns = ['MID', 'doi', 'title', 'abstract']

    source_columns = [col for col in final_df.columns if 'Source' in col]

    remaining_columns = [col for col in final_df.columns if col not in first_columns + source_columns]

    new_order = first_columns + source_columns + remaining_columns
    return final_df[new_order]
    

def main():
    sets = load_data()
    merged = merge_data(sets)
    merged.to_csv("output/merged.csv", index=False)
    

if __name__ == "__main__":
    main()