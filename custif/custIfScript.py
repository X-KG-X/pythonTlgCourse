#!/usr/bin/env python3

def main():
    score=int(input("Enter your score, [0,100]?"))
    
    msg="Your letter grade is: "

    if score>100 or score<0:
        print("Invalid entry, please enter valid score [0,100]")
    elif score>=90:
        print(msg+"A")
    elif score>=80:
        print(msg+"B")
    elif score>=70:
        print(msg+"C")
    elif score>=60:
        print(msg+"D")
    else:
        print(msg+"F")

if __name__=="__main__":
    main()
