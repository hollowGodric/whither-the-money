from expenseTracker import *

while (True):
	i = input("What do you want to do?\n")
	args = i.split()
	if (args[0] in commands):
		commands[args[0]](args[1:])
	elif i == 'stop':
		break
	else:
		print("You may use the following commands: ")
		for com in commands.keys():
			print ("[%s] " % com, end="")
		print("")
