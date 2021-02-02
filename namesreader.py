import csv
import pandas as pd

with open('prductsNamesMarques.csv','r') as readfile :
    rd = csv.reader(readfile,delimiter =',')
    for row in rd:
        for r in row:
            print(r)


#df = pd.read_excel("STOCK.xlsx", engine='openpyxl')
#for index, row in df.iterrows():
#    print(row[0],row[1])





