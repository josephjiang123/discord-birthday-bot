import csv
from datetime import datetime
import random

def getTodaysBirthdays() -> dict:
    today = datetime.now()
    with open('birthdays.csv', newline='') as csvfile:
        birthdays = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        todays_birthdays = dict()
        for row in birthdays:
            if monthToNum(row['Birth_Month']) == today.month and int(row['Birthdate']) == today.date:
                todays_birthdays[row['Discord']] = row['First_name']
        if isItNinisBirthday() == True:
            todays_birthdays['niranjan'] = "Niranjan 'Nini'"
        return todays_birthdays
            

def isItNinisBirthday() -> bool:
    return random.randint(1, 20) == 1

def isItTheirBirthday(guy:str) -> bool:
    today = datetime.now()
    if guy == "niranjan":
        return True
    with open('birthdays.csv', newline='') as csvfile:
        birthdays = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in birthdays:
            if row['Discord'] == guy:
                if monthToNum(row['Birth_Month']) == today.month and int(row['Birthdate']) == today.date:
                    return True
                else:
                    return False
    return False
    
def monthToNum(month:str):
    return {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9, 
            'October': 10,
            'November': 11,
            'December': 12
    }[month]

print(getTodaysBirthdays())