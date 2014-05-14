try:
   import _pickle as pickle
except:
   import pickle
import pprint
import datetime
import re
from decimal import *
from prettytable import PrettyTable

getcontext().prec = 7
moneyPattern = re.compile('[\d]+(\.[\d]{1,2})?')



def newExpenditure(args):
	expenDate = acquireDate()
	expenLocale = input('Where did you spend the money? ')
	expenAmount = input('Now type the amount spent: ')
	while moneyPattern.match(expenAmount) == None:
		expenAmount = input('Try again: ')
		
	itemList = [];
	if yesAnswer(input('Do you want to make an itemized list? ')):
		print('Type "done" when finished')
		runningTotal = Decimal(0)
		while True:
			itemName = input('Enter a name for the item: ')
			if itemName == 'done':
				break
			itemCost = input('Now the cost: ')
			while moneyPattern.match(itemCost) == None or itemCost == 'done':
				itemCost = input('Try again: ')
			if itemCost == 'done':
				break
			itemList.append({'name': itemName, 'cost': itemCost})
			runningTotal += Decimal(itemCost)
			if Decimal(runningTotal) == Decimal(expenAmount):
				break
			
	saveData = loadPickle()
	try:
		saveData[expenDate]
	except KeyError:
		saveData[expenDate] = []
				   
	saveData[expenDate].append({'place': expenLocale, 'amount': expenAmount, 'items': itemList})
	savePickle(saveData)


def acquireDate():
	loop = False
	while loop != True:
		expenDate = datetime.date.today()
		if yesAnswer(input('Was this today? ')):
			pass
		elif yesAnswer(input('Was it this month? ')):
			expenDate = expenDate.replace(day = int(input('Which day was it? ')))
		elif yesAnswer(input('Was it this year, at least?! ')):
			expenDate = expenDate.replace(
				month = int(input('Okay, whew. Which number month? ')),
				day = int(input('And which day was it? '))
			)
		else:
			expenDate = datetime.date(
				int(input('Alright then, which year was it? (It had better not be in the future; you\'ll break my program!) ')),
				int(input('Number month? ')),
				int(input('And which day was it? '))
			)
		loop = yesAnswer(input('So the date was %s? ' % expenDate.ctime()))
	return expenDate

def yesAnswer(answer):
	if answer == 'y' or answer == 'yes' or answer == 'mm':
		return True
	elif answer == 'quit':
		quit()
	else:
		return False


def savePickle(data):
	#open file for editing
	pickl = open('data.pkl', 'wb');
	
	#write object to file
	pickle.dump(data, pickl)
	
	# close at the end
	pickl.close()

def loadPickle():
	#open file for editing
	pickl = open('data.pkl', 'rb');
	
	#load object from file
	unpickledObj = pickle.load(pickl)
	
	# close at the end
	pickl.close()
	
	return unpickledObj 

	

def loadData(args):
	data = loadPickle()
	table = PrettyTable()
	table.add_column('name', (), align='l')
	table.add_column('cost', (), align='r')
	table.add_column('date', (), align='r')
	table.add_column('place', (), align='l')
	total = 0
	itemCosts = 0
	for date in data:
		for x in data[date]:
			total += Decimal(x['amount'])
			for item in x['items']:
				table.add_row((item['name'], item['cost'], date, x['place']))
				itemCosts += Decimal(item['cost'])
	print(table)
	print('Total expenditures entered:', total, 'EUR')
	print('Unaccounted for: ', total - itemCosts, 'EUR')


commands = {
	'quit': quit,
	'new': newExpenditure,
	'load': loadData
}
