# Author: Zak Malimar

import csv
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.\
from_json_keyfile_name(r'D:\programming\python\csvChecker\credentials.json', scope)

client = gspread.authorize(credentials)
sheet = client.open('users').sheet1

current_users = []  # users that are in both files
current_users_email = [] # their emails to validate
terminated_users = [] # user in initial but not manifest
new_users = [] # user in manifest but not initial
new_users_email = []
revised_users = [] # array of users aren't terminated

def removeDuplicateUserInfo(x):
        return list(dict.fromkeys(x))

def csvInit():
    with open(r'D:\programming\python\csvChecker\initial.csv') as initial, open(r'D:\programming\python\csvChecker\manifest.csv') as manifest:
        initialTable = list(csv.DictReader(initial))
        manifestTable = list(csv.DictReader(manifest))
        
        for initialReader in initialTable:
             for manifestReader in manifestTable:  
                if initialReader['Email'].lower() == manifestReader['Email'].lower():
                    current_users.append(manifestReader['FirstName'] + "," + manifestReader['SurName'] + "," + manifestReader['Email'] + "," + initialReader['Facility']) 
                    current_users_email.append(manifestReader['Email']) 
                    break
    csvCheckForTerm()
        # users that are in both files

def csvCheckForTerm():
    with open(r'D:\programming\python\csvChecker\initial.csv') as initial:
        initialTable = list(csv.DictReader(initial))

    for initialCheck in initialTable:
        if initialCheck['Email'] not in current_users_email:
            terminated_users.append(initialCheck['Email'])
    
    for secondCheck in initialTable:
        if secondCheck['Email'] not in terminated_users:
            revised_users.append(secondCheck['FirstName'] + "," + secondCheck['SurName'] + "," + secondCheck['Email'] + "," + secondCheck['Facility'])

    # print(revised_users)
    print("----------- TERMINATED ----------------------")
    print(terminated_users)
    csvCheckForNew()
    
def csvCheckForNew():
    with open(r'D:\programming\python\csvChecker\manifest.csv') as manifest:
        manifestTable = list(csv.DictReader(manifest))
        for manifestCheck in manifestTable: 
            if manifestCheck['Email'] not in current_users_email:
                if manifestCheck['Email'] not in terminated_users:
                    new_users.append(manifestCheck['FirstName'] + "," + manifestCheck['SurName'] + "," + manifestCheck['Email'])
                    new_users_email.append(manifestCheck['Email'])
    print("----------- NEW ----------------------")
    print(new_users_email)
    csvRewritten()

def csvRewritten():
    with open(r'D:\programming\python\csvChecker\new_user.csv','w', newline="") as reconstruction: # takes the new users and prepare it to be sent to Google Spreadsheets
        rewriter = csv.writer(reconstruction, delimiter="\n", skipinitialspace=True)
        reassembledUsers = removeDuplicateUserInfo(new_users)
        reassembledCurrentUsers = removeDuplicateUserInfo(revised_users)
        rewriter.writerow(['FirstName,SurName,Email,Facility'])
        rewriter.writerow(reassembledCurrentUsers) # old users
        rewriter.writerow(reassembledUsers) # new users
        # print("New Users Added to File")
        reconstruction.close()

with open(r'D:\programming\python\csvChecker\initial.csv',newline='') as i:
    j = csv.reader(i)
    initialData = [line for line in j]
    print('--------- //// program running //// ------------')
    csvInit()
        # csvCheckForTerm()

