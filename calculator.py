#!/usr/bin/env python3
# Filename: calculator
# copyright (c) Tomas Gil 2015
import datetime
import csv
import sqlite3


#Create database
conn = sqlite3.connect('mealvouchers.sqlite3')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Vacation_days')
cur.execute('CREATE TABLE Vacation_days (name TEXT, vacations INTEGER)')
#conn.close()

current_month = "May" #input("Select a month for calculation:")  # datetime.date.today().strftime("%B")
# current_month = datetime.date.strftime(month,"%m")
print("Now is: ", current_month)


def get_workdays():
    if current_month == "March":
        workdays = 20
    elif current_month == "April":
        workdays = 18
    elif current_month == "May":
        workdays = 19
    return workdays

#return working days
work_days = get_workdays()


class Employee:
    def __init__(self, name, vacation_start, vacation_end):
        self.name = name
        self.vacation_start = vacation_start
        self.vacation_end = vacation_end

    def count_vacation_days(self):
        start_date = datetime.datetime.strptime(self.vacation_start, "%d-%m-%Y")
        if start_date < datetime.datetime(2015, 5, 1):
            start_date = datetime.datetime(2015, 5, 1)
        end_date = datetime.datetime.strptime(self.vacation_end, "%d-%m-%Y")
        start_week_days = min(start_date.weekday(), 4) + 1
        end_week_days = min(end_date.weekday(), 4) + 1
        no_of_weeks = end_date.isocalendar()[1] - start_date.isocalendar()[1]
        working_days = (5 * no_of_weeks) + end_week_days - start_week_days
        if start_date.weekday() < 5:
            working_days += 1
        return working_days

    def __str__(self):
        return str(self.__dict__)

#import csv file return
def import_data():
    employees_list = []
    with open('listscv.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employees_list.append(row)
    return employees_list


def import_ees():
    ee_list = import_data()
    mealvoucher_output = []
    for c in ee_list:
        ee_dict = dict(c)
        ee = Employee(ee_dict['name'], ee_dict['vacation_start'], ee_dict['vacation_end'])
        mealvoucher_output.append(ee)
        #Employee.display(ee)
    return mealvoucher_output

def insert_into_db():
    db_list = import_ees()
    cur = conn.cursor()
    for q in range(len(db_list)):
        cur.execute('INSERT INTO Vacation_days(name, vacations) VALUES( ?, ? )', (db_list[q].name,db_list[q].count_vacation_days()))
        conn.commit()

def pivot():
    pivot_list = dict()
    conn = sqlite3.connect('mealvouchers.sqlite3')
    cur = conn.cursor()
    cur.execute("select name from Vacation_days")
    db_ee_list = ([i[0] for i in cur.fetchall()])
    for t in range(len(db_ee_list)):
        cur.execute('SELECT vacations FROM Vacation_days WHERE name = ?', (db_ee_list[t], ))
        q = ([int(i[0]) for i in cur.fetchall()])
        e = (db_ee_list[t], sum(q))
        pivot_list[db_ee_list[t]] = work_days - sum(q)
        #print (db_ee_list[t], "will get", (work_days - sum(q)),"mealvouchers for month of",current_month)
    return (pivot_list)

def main():
    insert_into_db()
    result = pivot()
    for r in result:
        print(r, "will get", result[r], "mealvouchers")



