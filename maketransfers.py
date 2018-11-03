#!/usr/bin/python
import argparse
import sys
import os
import csv
import random
from reportlab.pdfgen import canvas
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--debitacc", required=True,
	help="Account to be Debited")
ap.add_argument("-d", "--dir", required=True,
	help="Directory containing csv")
ap.add_argument("-m", "--max", required=True,
	help="Max Amount")
ap.add_argument("-n", "--min", required=True,
	help="Min Amount")
args = vars(ap.parse_args())


DEBITACC = args['debitacc']
CSVDIR = args['dir']
max_amount = args['max']
min_amount = args['min']


def makeTransactions(transaction):
        bank_code = transaction[0]
        acc_number = transaction[1]
        acc_name = transaction[2]
        amount = transaction[3]
        narration = transaction[4]
        if debitAccount(DEBITACC):
	    debit_result = True
            credit_result = creditAccount(acc_number)
        else:
            debit_result = False
            credit_result = False
        c = canvas.Canvas(DEBITACC+".pdf")
        c.drawString(30,750, acc_number)
        c.drawString(180,750, amount)
        c.drawString(360,750, debit_result)
        c.drawString(540,750, credit_result)
        c.save()

        
def sendJsontoApi(resp):
    print(resp)
    return
   
def debitAccount(account):
    return random.choice([True, False])

def creditAccount(account):
    return random.choice([True, False])


if __name__=='__main__':
    try:
        os.chdir(CSVDIR)
    except OSError:     
        pass

    transactions_list = []

    for filename in os.listdir("."):
        if(filename.lower().endswith(('.csv'))):
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    #validate the information
                    elif(len(row[0]) == 3 and row[0].isdigit() and len(row[1]) == 10 and row[1].isdigit() and row[3].isdigit() and int(row[3]) < int(max_amount) and int(row[3]) > int(min_amount)):
                        bank_code = row[0]
                        acc_number = row[1]
                        acc_name = row[2]
                        amount = row[3]
                        narration = row[4]
                        single_transaction = [bank_code, acc_number, acc_name, amount, narration]
                        transactions_list.append(single_transaction)
                        line_count += 1
                    else:
                        line_count += 1
                print(f'Processed {line_count} lines.')
    pool = Pool()
    pool.map(makeTransactions, transaction_list)
    pool.close() 
    pool.join()
