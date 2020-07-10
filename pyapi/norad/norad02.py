#!/usr/bin/env python3
import requests
import pandas as pd
import json


def main():
    resp=requests.get("http://www.celestrak.com/NORAD/elements/active.txt")
    # print(resp)
    #get data from the norad and write it to active.txt
    with open("active.txt", "w") as f:
        for line in resp.text:
            f.write(line)

    #create a dictionary of name:revsdata celest{}
    celest={}
    cnt=0
    with open("active.txt","r") as celesfile:
        txtlines=celesfile.readlines()
        for line in txtlines:
            if cnt%3==0:
                revsdata=txtlines[(cnt+2)].split(" ")
                revsdata2=list(filter(('').__ne__,revsdata))
                celest[line.strip()]=float(revsdata2[-2])
            cnt+=1

    #use the celest{} to create pandas dataframe
    dataDF=pd.DataFrame(list(celest.items()),columns=['col1','col2'])
    dataSorted=dataDF.sort_values(by=['col2'])
    #print top ten satellite that take the most revs per day
    print(f"\n\n Top ten satellites that make the most revolutions around Earth per day:")
    print(dataSorted.tail(10))

    print(f"\n\n Top ten satellites that make the least revolutions around Earth per day:")
    print(dataSorted.head(10))

if __name__=="__main__":
    main()