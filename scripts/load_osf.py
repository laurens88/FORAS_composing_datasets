import requests
from pathlib import Path
from typing import List

synergy_replication: tuple = ("synergy_replication.csv", "https://osf.io/yzqf8/download/")
comprehensive_search: tuple = ("comprehensive_search.csv", "https://osf.io/4x39f/download/")
inclusion_criteria_top1000: tuple = ("inclusion_criteria_top1000.csv", "https://osf.io/r8wq3/download/")
included_records: tuple = ("included_records.xlsx", "https://osf.io/ejg9r/download/")
included_records_active_learning: tuple = ("included_records_active_learning.xlsx", "https://osf.io/36rhe/download/")
snowballing: tuple = ("snowballing.csv", "https://osf.io/7c4nf/download/")
dimensions: tuple = ("dimensions.xlsx", "https://osf.io/n8qae/download/")

data_subsets = [synergy_replication, comprehensive_search, inclusion_criteria_top1000, included_records, 
                included_records_active_learning, snowballing, dimensions]


def download_data(data_subsets: List[tuple]) -> None:
    for data_subset in data_subsets:
        filename, url = data_subset
        file_path = Path("data", filename)
        if not file_path.exists():
            response = requests.get(url)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(Path("data", filename), "wb") as file:
                file.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"{filename} already exists")


def main():
    download_data(data_subsets)
    

if __name__ == "__main__":
    main()