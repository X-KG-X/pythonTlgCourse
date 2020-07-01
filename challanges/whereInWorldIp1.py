#!/usr/bin/env python3

import requests

LOOKUPAPI="http://ip-api.com/json/"
def main():
    ip=str(input("Enter ipv4:"))

    r= requests.get(LOOKUPAPI+ip)
    jData=r.json()
    print(f"Location of {ip} is {jData['city']}, {jData['region']} ")


if __name__=="__main__":
    main()
