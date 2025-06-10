import pandas as pd

def read_file():
    """
    Read the starting 200 rows of excel file and store into dataframe using pandas
    """
    df = pd.read_excel("src/hassan/Amazon_Trading.xlsx").head(200)
    shared_memory = {"data": df}
    return shared_memory

print(read_file())

read_file()
