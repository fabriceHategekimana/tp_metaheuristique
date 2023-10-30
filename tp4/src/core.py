import numpy as np
import pandas as pd
from functools import reduce
import random


def myfilter(f, tab):
    return np.array(list(filter(f, tab)))


def mymap(f, tab):
    return np.array(list(map(f, tab)))


def list_to_dataframe(mylist, name):
    return pd.DataFrame({name: mylist})


def string_to_list(string):
    return mymap(lambda x: str(x), string) 


def get_max(df, column):
    maxid = df[column].idxmax()
    return df.iloc[maxid]


def get_min(df, column):
    minid = df[column].idxmin()
    return df.iloc[minid]
