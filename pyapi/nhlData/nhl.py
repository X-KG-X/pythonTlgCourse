#!/urs/bin/env python3

import requests
import pandas as pd
import matplotlib.pyplot as plt

def main():
    #get data
    resp=requests.get("https://statsapi.web.nhl.com/api/v1/teams").json()

    #Division list dict
    divDict=[]
    #print response data
    for one in resp['teams']:
        print(f"Team Name: {one['name']}, \t\t Stadium Name: {one['venue']['name']}")
        divDict.append(one['division'])
    #create pandas dataframe
    nhldf=pd.DataFrame(resp['teams'])
    print(nhldf.head())

    #create df for list of Division dictDict
    nhldivDf=pd.DataFrame(divDict)
    print(nhldivDf.head())
    #groupby division id
    divGrp=nhldivDf.groupby('id').agg({'id':['count']})
    print()
    print(divGrp)
    #plot the groupby division id
    divGrp.plot(kind="barh")
    plt.show()
    
if __name__=="__main__":
    main()