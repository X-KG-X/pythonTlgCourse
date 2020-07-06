#!/usr/bin/python3

import requests

# define the URL we want to use
POSTURL = "http://validate.jsontest.com/"
DATEURL = "http://date.jsontest.com/"
IPURL="http://ip.jsontest.com"

def main():
    respDate=requests.get(DATEURL).json()
    print(f"TimeStamp: {respDate['date']} {respDate['time']}")

    respIP=requests.get(IPURL).json()
    print(f"Current IP: {respIP['ip']}")

    with open("servers.txt") as f:
        svrs=f.readlines()
    
    jsontotest={}
    jsontotest["time"]=respDate["time"]
    jsontotest["ip"]=respIP["ip"]
    jsontotest["svrs"]=svrs
    print(jsontotest)

    mydata={}
    mydata["json"]=str(jsontotest)

    respValidate=requests.post(POSTURL,data=mydata).json()

    print(f"JSON Validity: {respValidate['validate']}")



if __name__ == "__main__":
    main()
