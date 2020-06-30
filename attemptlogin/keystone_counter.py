#!/usr/bin/python3
# parse keystone.common.wsgi and return number of failed login attempts
loginfail = 0 # counter for fails
allFail = 0  # all auth fail messages
# open the file for reading
keystone_file = open("/home/student/mycode/attemptlogin/keystone.common.wsgi","r")
# turn the file into a list of lines in memory
keystone_file_lines=keystone_file.readlines()
# loop over the list of lines
print("Ip address of failed logins are as follows: ")
for line in keystone_file_lines:
    # if this 'fail pattern' appears in the line...
    if "- - - - -] Authorization failed" in line:
        loginfail += 1 # this is the same as loginfail = loginfail + 1
        print(line.split(" ")[-1])
    if "-] Authorization failed" in line:
        allFail += 1

print("The number of failed log in attempts is", loginfail)
print("The number of successful logins is", (allFail-loginfail) )
keystone_file.close() # close the open file


