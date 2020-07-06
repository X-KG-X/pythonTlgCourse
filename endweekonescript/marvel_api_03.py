#!/usr/bin/env python3
import argparse
import time
import requests
import hashlib

## Define the API here
XAVIER = 'http://gateway.marvel.com/v1/public/characters'

## Calculate a hash to pass through to our MARVEL API call
## Marvel API wants md5 calc md5(ts+privateKey+publicKey)
def hashbuilder(timeywimey, pvkee, pubkee):
    return hashlib.md5((timeywimey+pvkee+pubkee).encode('utf-8')).hexdigest()

## Perform a call to MARVEL Character API
## http://gateway.marvel.com/v1/public/characters
## ?name=Spider-Man&ts=1&apikey=1234&hash=ffd275c5130566a2916217b101f26150
def marvelcharcall(stampystamp, hashyhash, pkeyz, lookmeup):
    r = requests.get(XAVIER+"?name="+lookmeup+"&ts="+stampystamp+"&apikey="+pkeyz+"&hash="+hashyhash)

    #print(XAVIER+"?name="+lookmeup+"&ts="+stampystamp+"&apikey="+pkeyz+"&hash="+hashyhash)
    return r.json()

    
def main():           
    
    ## harvest private key
    with open(args.dev) as mccoy:
        beast = mccoy.read().rstrip('\n')
    
    ## harvest public key
    with open(args.pub) as munroe:
        storm = munroe.read().rstrip('\n')
    
    ## create an integer from a float timestamp (for our RAND)
    nightcrawler = str(time.time()).rstrip('.')
    
    ## build hash with hashbuilder(timestamp, privatekey, publickey)
    cerebro = hashbuilder(nightcrawler, beast, storm)

    ## call the API with marvelcharcall(timestamp, hash, publickey, character)
    uncannyxmen1 = marvelcharcall(nightcrawler, cerebro, storm, args.char1)
    ## display results
    # comicsChar1=uncannyxmen1['data']['results'][0]['comics']['items']
    comicsChar1count=uncannyxmen1['data']['results'][0]['comics']['available']

    ## call the API with marvelcharcall(timestamp, hash, publickey, character)
    uncannyxmen2 = marvelcharcall(nightcrawler, cerebro, storm, args.char2)
    ## display results
    # comicsChar2=uncannyxmen1['data']['results'][0]['comics']['items']
    comicsChar2count=uncannyxmen2['data']['results'][0]['comics']['available']
    # Comparing the comic count of 2 charaters
    if(comicsChar1count>comicsChar2count):
      print(f"\n\n{args.char1}({comicsChar1count}) has more comic appearances then {args.char2}({comicsChar2count})\n")
    elif(comicsChar1count<comicsChar2count):
      print(f"\n\n{args.char2}({comicsChar2count}) has more comic appearances then {args.char1}({comicsChar1count})\n")
    else:
      print(f"\n\nSame number of comic appearances {comicsChar1count}\n")
    

    # character1 storie count
    storiesChar1count=uncannyxmen1['data']['results'][0]['stories']['available']
    # character1 storie count
    storiesChar2count=uncannyxmen2['data']['results'][0]['stories']['available']
    #Compare event appareances of the two charachers
    if(storiesChar1count>storiesChar2count):
      print(f"\n\n{args.char1}({storiesChar1count}) has more story appearances then {args.char2}({storiesChar2count})\n")
    elif(storiesChar1count<storiesChar2count):
      print(f"\n\n{args.char2}({storiesChar2count}) has more story appearances then {args.char1}({storiesChar1count})\n")
    else:
      print(f"\n\nSame number of story appearances {storiesChar1count}\n")


## Define arguments to collect
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', help='Provide the /path/to/file.priv \
      containing Marvel private developer key')
    parser.add_argument('--pub', help='Provide the /path/to/file.pub \
      containing Marvel public developer key')
    
    ## The line below is NEW! This allows us to pass the lookup character
    parser.add_argument('--char1', \
      help='Character 1 to search for within the Marvel universe for comparision')
    parser.add_argument('--char2', \
      help='Character 2 to search for within the Marvel universe for comparision')
    args = parser.parse_args()
    main()

