#!/usr/bin/env python3

import requests
import pandas as pd
import json


def main():
    # resp=requests.get("http://www.celestrak.com/NORAD/elements/active.txt")
    # # print(resp)
    # #get data from the norad and write it to active.txt
    # with open("active.txt", "w") as f:
    #     for line in resp.text:
    #         f.write(line)

    #write the names of the satellite to celest.txt
    count=0
    with open("celest.txt","w") as celesfile:
        with open("active.txt","r") as f:
            for line in f.readlines():
                if count%3==0:
                    celesfile.write(line)
                count+=1
    # print(count)

    #create a dictionary of name:revsdata celest{}
    celest={}
    cnt=0
    with open("celest.txt","r") as celesfile:
        for line in celesfile.readlines():
            celest[line.strip()]=float(readRevsData(cnt))
            cnt+=1

    #use the celest{} to create pandas dataframe
    dataDF=pd.DataFrame(list(celest.items()),columns=['col1','col2'])
    dataSorted=dataDF.sort_values(by=['col2'])
    #print top ten satellite that take the most revs per day
    print(f"\n\n Top ten satellites that make the most revolutions around Earth:")
    print(dataSorted.tail(10))

#reads the revdata for given satellite position
def readRevsData(i):
    with open("active.txt","r") as f:
        txtlines=f.readlines()
        revsdata=txtlines[(i+2)+(i*2)].split(" ")
        revsdata2=list(filter(('').__ne__,revsdata))
        return revsdata2[-2]

if __name__=="__main__":
    main()