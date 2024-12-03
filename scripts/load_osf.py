import requests
from pathlib import Path

synergy_replication = ("synergy_replication.csv", "https://osf.io/yzqf8/download/")
comprehensive_search = ("comprehensive_search.csv", "https://osf.io/4x39f/download/")
inclusion_criteria_top1000 = ("inclusion_criteria_top1000.csv", "https://osf.io/r8wq3/download/")
included_records = ("included_records.xlsx", "https://osf.io/ejg9r/download/")
included_records_active_learning = ("included_records_active_learning.csv", "https://osf.io/36rhe/download/")
snowballing = ("snowballing.csv", "https://osf.io/7c4nf/download/")

data_subsets = [synergy_replication, comprehensive_search, inclusion_criteria_top1000, included_records, included_records_active_learning, snowballing]

def download_data(data_subsets):
    for data_subset in data_subsets:
        filename, url = data_subset
        response = requests.get(url)
        with open(Path("data", filename), "wb") as file:
            file.write(response.content)

def main():
    download_data(data_subsets)
    

if __name__ == "__main__":
    main()