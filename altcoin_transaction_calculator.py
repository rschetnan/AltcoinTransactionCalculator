import json
from csv import reader
import sys

#Grab the prices in the json file and load them up in a dictionary
fh = open('prices.json')
js = json.load(fh)

#Create a transactions dictionary
transactions = dict()

#Grab the transactions file, parse it and load the data
fh = open('transactions.csv')

csv_reader = reader(fh)
header = next(csv_reader)
# Check file as empty
if header != None:
    # Iterate over each row after the header in the csv
    for row in csv_reader:
        # Grab the transaction ID from the record
        transaction_id = row[0]
        #Create a transaction records dictionary
        transaction_details = {}
        #Add dictionary entries
        transaction_details['Txhash'] = row[0]
        transaction_details['UnixTimestamp'] = row[1]
        date_and_time = row[2].split()
        transaction_details['Date'] = date_and_time[0]
        transaction_details['Time'] = date_and_time[1]
        transaction_details['From'] = row[3]
        transaction_details['To'] = row[4]
        float_val = 0.0
        try:
            float_val = float(row[5].replace(",", ""))
        except:
            float_val = 0
        transaction_details['Value'] = float_val
        transaction_details['ContractAddress'] = row[6].lower()
        transaction_details['TokenName'] = row[7]
        transaction_details['TokenSymbol'] = row[8]

        # Create an empty list of records dictionaries to return if the transaction doesn't yet exist
        records_list = []

        #Get the list of transaction records dictionaries from the transactions dictionary
        transaction_records = transactions.get(transaction_id, records_list)

        #Add the record dictionary to the list
        transaction_records.append(transaction_details)

        #Add the list of transaction records dictionaryies to the transactions dictionary
        transactions[transaction_id] = transaction_records

tx_id = input("Provide the transaction ID:")

if len(tx_id) == 0: sys.exit()

if tx_id in transactions:
    tx_records = transactions[tx_id]
else:
    print('Transaction not found!')
    sys.exit()

tx_record_count = len(tx_records)

#Display a menu of records associated with the transaction
print('Transaction records:')
print()
for i in range(tx_record_count):
   print(i, ":", tx_records[i]['Value'], tx_records[i]['TokenName']) 

#Ask user to select a record
print()
tx_record_input = input('Select a record or Enter for 0: ')

try:
    record_index = int(tx_record_input)
except:
    record_index = 0

#Grab the selected transaction record
tx = tx_records[record_index]

tx_date = tx['Date']
contract_address = tx['ContractAddress']

#Display the contract address and give user the opportunity to change it
print('Contract address is', contract_address, 'for', tx['TokenName'])

contract_address_input = input("Provide a new contract address or Enter:")

if len(contract_address_input) > 0:
    contract_address = contract_address_input.lower()
    print('New contract address is', contract_address)

#look up the price in the prices dictionary and provide status messages
if contract_address in js:
    prices = js[contract_address]
else:
    print('No prices found for this token!')
    prices = {}

if tx_date in prices:
    price = float(prices[tx_date])
else:
    print('No price found for date of transaction!')
    price = 0.0

print('Token price:', price)

# Give the user an opportunity to change the price
price_input = input("Provide a new token price or Enter:")
if len(price_input) > 0:
    try:
        price = float(price_input)
    except:
        print('Price is not valid!')
        price = 0.0
    print('New price is', price)

token_amount = tx['Value']

#Show the token oamout and give the user a chance to update it
print('Token amount:', token_amount)
token_amount_input = input("Provide a new token amount or Enter:")
if len(token_amount_input) > 0:
    try:
        token_amount = float(token_amount_input)
    except:
        print('Token amount is not valid!')
        token_amount = 0.0
    print('New token amount is', token_amount)

#Calculate and display the transaction value
tx_value = price * token_amount
print('Transaction value is', tx_value)




