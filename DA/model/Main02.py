import pandas as pd
import csv

df = 'D:/장우영/LOCALSEARCH\DA\DA\data/AIS_Test.xlsx'

ais_data = pd.read_excel(df)
print(ais_data)

#            mmsi           ship_name  ship_type  ...    cog    sog             insert_time
# 0      440051540           D-01          0      ...   329.2   5.7 2023-05-11 10:10:58.000
# 1      440300780            NaN          0      ...   329.8   0.0 2023-05-11 10:10:58.000

