#!/usr/bin/env python3

import requests

import yaml


API="https://jservice.io/api/random?count=3"
def main():
    qa=getQs()
    #print("check")
    playerPoint=0
    player={}
    playerName=input("Your name: ")
    for one in qa:
        print(qa[one][1])
        print(qa[one][0]+"\n")
        ans=input(one+": ")
        if ans.lower()==qa[one][0].lower():
            print("Correct!\n")
            if qa[one][1] is not None:
                 playerPoint+=qa[one][1]
        else:
            print("Loser!!\n")
        player[playerName]=playerPoint
    print(player)


    with open(r'score_file.yaml', 'a') as yamlfile:
        yaml.dump(player, yamlfile)

    
def getQs():
    qa={}
    resp=requests.get(API)
    for one in resp.json():
        qa[one['question']]=[one['answer'],one['value']]
    #print(str(qa))
    #print(len(qa))
    return qa


if __name__=="__main__":
    main()
