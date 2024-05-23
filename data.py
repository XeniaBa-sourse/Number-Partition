import csv
import pandas as pd
from Partitions import Partition


def find_delimiter(path):
    sniffer = csv.Sniffer()
    with open(path) as fp:
        delimiter = sniffer.sniff(fp.read(5000)).delimiter
    return delimiter

#data = pd.read_csv('data.csv', delimiter=find_delimiter('data.csv'),low_memory=False)

def my_data(num1, num2=None):
    part = Partition()
    if num2:
        data = pd.DataFrame()
        for i in range(int(num1),int(num2)+1):
            partitions = part.partitions(i)
            d = part.create_table(partitions)
            data = pd.concat([data, d])
    else:
        partitions = part.partitions(int(num1))
        data = part.create_table(partitions)
    return data

