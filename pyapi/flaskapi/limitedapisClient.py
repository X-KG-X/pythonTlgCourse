#!/usr/bin/env python3

import requests

def main():
    for i in range(201):
        resp=requests.get("http://0.0.0.0:2224/fast")
        print(resp)

if __name__=="__main__":
    main()