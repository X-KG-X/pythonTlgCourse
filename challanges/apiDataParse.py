#!/usr/bin/env python3


'''issloc={
"message": "success",
"timestamp": 1593527850,
"iss_position": {
"longitude": "25.5639",
"latitude": "-48.1186"
}
}'''

import json
import requests
from geopy.geocoders import Nominatim

def main():
    r=requests.get("http://api.open-notify.org/iss-now.json")
    data=r.json()
    print(type(data))
    print("Current coordinates of the ISS is :"+ str(data["iss_position"]))

    geolocator = Nominatim(user_agent="kg")
    
    curLocation= data['iss_position']
    location =geolocator.reverse(f"{curLocation['latitude']}, {curLocation['longitude']}") 
    print(location.address)




if __name__=="__main__":
    main()
