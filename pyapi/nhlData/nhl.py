#!/urs/bin/env python3

import requests
import pandas as pd
import matplotlib.pyplot as plt

def main():
    resp=requests.get("https://statsapi.web.nhl.com/api/v1/teams").json()

    for one in resp['teams']:
        print(f"Team Name: {one['name']}, \t\t Stadium Name: {one['venue']['name']}")

    nhldf=pd.DataFrame(resp['teams'])
    print(nhldf.head())

    # nhlLocation=nhldf.groupby("locationName").agg('count')
    # print(nhlLocation)
    nhldivDf=pd.DataFrame(nhldf['division'])
    print(nhldivDf.head())
    print(type(nhldivDf))
    

if __name__=="__main__":
    main()