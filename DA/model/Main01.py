import pandas as pd
import numpy as np

excel_file = 'D:/장우영/LOCALSEARCH\DA\DA\data/05_09해양 기상청 데이터.xls'

df = pd.read_excel(excel_file)
#   print(df.shape)

# 데이터 확인 

print(df.head(2))

#   지방청            표지                일시         풍향(˚)  유향(˚)    기온(℃)    풍속(m/s)   유속(kn)  기압(hPa)  습도(%)
#   부산청  부산항유도등부표(랜비)  2023-05-09 23:50     313       NaN        16.5     4.11       0.0        1012     62