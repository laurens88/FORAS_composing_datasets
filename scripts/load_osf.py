import requests
from pathlib import Path

data1 = ("data1.csv", "https://osf.io/yzqf8/download/")
data2 = ("data2.csv", "https://osf.io/4x39f/download/")
data3a = ("data3a.csv", "https://osf.io/r8wq3/download/")
data3b = ("data3b.xlsx", "https://osf.io/ejg9r/download/")
data3c = ("data3c.csv", "https://osf.io/36rhe/download/")
data4 = ("data4.csv", "https://osf.io/7c4nf/download/")

data_subsets = [data1, data2, data3a, data3b, data3c, data4]

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