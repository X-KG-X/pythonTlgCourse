#!/usr/bin/env python3

import requests
import yaml

LOOKUPAPI="http://ip-api.com/json/"
def main():
##    ip=str(input("Enter ipv4:"))

    #get data from external yaml life
    with open('ips.yaml') as f:
        ipList=yaml.load(f,Loader=yaml.FullLoader)

    for ip in ipList['IpList']:
        r= requests.get(LOOKUPAPI+ip)
        ipJson=r.json()
        print(f"IPv4 {ip} is located in {ipJson['city']}, {ipJson['region']}\n")


if __name__=="__main__":
    main()
