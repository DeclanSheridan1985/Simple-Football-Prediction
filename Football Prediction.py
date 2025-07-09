import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#English Data - read in the 14 datasets from Football data website
epl_2021 = pd.read_csv("http://www.football-data.co.uk/mmz4281/2120/E0.csv")
epl_1920 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1920/E0.csv")
epl_1819 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1819/E0.csv")
epl_1718 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1718/E0.csv")
epl_1617 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1617/E0.csv")
epl_1516 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1516/E0.csv")
epl_1415 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1415/E0.csv")
epl_1314 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1314/E0.csv")
epl_1213 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1213/E0.csv")
epl_1112 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1112/E0.csv")
epl_1011 = pd.read_csv("http://www.football-data.co.uk/mmz4281/1011/E0.csv")
epl_0910 = pd.read_csv("http://www.football-data.co.uk/mmz4281/0910/E0.csv")
epl_0809 = pd.read_csv("http://www.football-data.co.uk/mmz4281/0809/E0.csv")
epl_0708 = pd.read_csv("http://www.football-data.co.uk/mmz4281/0708/E0.csv")
epl_0607 = pd.read_csv("http://www.football-data.co.uk/mmz4281/0607/E0.csv")
epl_0506 = pd.read_csv("http://www.football-data.co.uk/mmz4281/0506/E0.csv")


#concatanate function allows it to be added together even when different columns
english=pd.concat([epl_0506,epl_0607,epl_0708,epl_0809,epl_0910,epl_1011,
           epl_1112,epl_1213,epl_1314,epl_1415,epl_1516,
           epl_1617,epl_1718, epl_1819,epl_1920,epl_2021]
, axis=0, ignore_index=True)

english.to_csv('Football Data.csv')