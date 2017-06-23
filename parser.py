# Parses log.txt and outputs useful information

import operator
from tabulate import tabulate

LOGFILE = 'log.txt'
STR1 = "function"

# Parameter: A duplicate time (string)
# Returns an array of lines that contains the duplicate times
def duplicate(dup):
	dup_arr = []
	with open(LOGFILE) as f:
		for line in f.readlines():
			if dup in line:
				dup_arr.append(line)
	return dup_arr

with open(LOGFILE) as f:

	everything_arr = [] # A list of list, containing the entry time, function name, times-called, exit time
	func_names = []
	enter_times = []
	exit_times = []
	debug_times = []
	warning_times = []

	enter_dic = {}
	enter_dic_sorted = {} # a list containing a tuple consisting of the enter time and the function name

	exit_dic = {}
	exit_dic_sorted = {} # a list containing a tuple consisting of the exit time and the function name

	flag = '' # ie., enter, exits, debug, warning

	for line in f.readlines():
		
		########### ENTERS ###########

		if (line.find("enter")) > 0:
			flag = 'enters'
			dup = ''
			dup_func_names = [] # List of function names that have the same entry time
			enter_times.append(line[0:9])
			enter_dic[line[0:9]] = str(line[(line.find(STR1)):].strip(STR1).lstrip(' ').rstrip('\n').rstrip('\t').rstrip('()')) # ie., enter_dic[time] = function name
			enter_dic_sorted = map(list,sorted(enter_dic.items(), key=lambda value: value[0])) # Sorts the array by the time (the key) and returns a list of tuples
			for i in set(enter_times):
			  	if enter_times.count(i) > 1:
			  		dup = i
					for i in duplicate(i):
						dup_func_names.append(str(i[(i.find(STR1)):].strip(STR1).lstrip(' ').rstrip('\n').rstrip('\t').rstrip('()')))
					# print(exit_dic_sorted)
					arr = [x[1] for x in enter_dic_sorted]
					# print(arr)
					for i in dup_func_names:
						if not i in arr:
							enter_dic_sorted.append((dup,i))

		########### EXITS ###########

		elif (line.find("exits")) > 0:
			flag = 'exits'
			dup = ''
			dup_func_names = [] # List of function names that have the same exit time
			exit_times.append(line[0:9])
			exit_dic[str(line[0:9])] = str(line[(line.find(STR1)):].strip(STR1).lstrip(' ').rstrip('\n').rstrip('\t').rstrip('()'))
			exit_dic_sorted = map(list,sorted(exit_dic.items(), key=lambda value: value[0]))
			for i in set(exit_times):
			  	if exit_times.count(i) > 1:
			  		dup = i
					for i in duplicate(i):
						dup_func_names.append(str(i[(i.find(STR1)):].strip(STR1).lstrip(' ').rstrip('\n').rstrip('\t').rstrip('()')))
					# print(exit_dic_sorted)
					arr = [x[1] for x in exit_dic_sorted]
					# print(arr)
					for i in dup_func_names:
						if not i in arr:
							exit_dic_sorted.append([dup,i])

		########### DEBUG ###########

		elif (line.find("Debug")) > 0:
			flag = 'debug'
			debug_times.append(line[0:9])

		########### WARNING ###########

		elif (line.find("Warning")) > 0:
			flag = 'warning'
			warning_times.append(line[0:9])

	#print(enter_dic_sorted)
	#print("######")
	#print(exit_dic_sorted)
	#print("######")

	# Stores function names into array
	for i in enter_dic_sorted:
		func_names.append(i[1])

	# Creates a list of list that contains the function name along with the number of times called (not ordered)
	times_called = [[x,func_names.count(x)] for x in set(func_names)] 
	func_names = sorted(set(func_names), key = func_names.index) # Sorts the function names back into the order in which it was called
	func_times_called = [] # The finalized list of tuples containing the function name along with its number of times called
	
	for i in func_names:
		for j in times_called:
			if i == j[0]:
				func_times_called.append((i,j[1]))

	func_times_called = map(list, func_times_called) # Convert list of tuples to list of list for tabulate function
	# print(func_times_called)
	# print(func_names)
	# print("\n")
	# print(warning_times)
	for i in range(len(func_times_called)):
		if (func_times_called[i][0] == enter_dic_sorted[i][1]):
			if ((len(func_times_called[i])) == 2):
				enter_dic_sorted[i].append(1)
			else:
				enter_dic_sorted[i].append(func_times_called[i][1])

	# print(func_times_called[i])
	for i in enter_dic_sorted:
		if (len(i) == 2):
			i.append(1)
	# print(enter_dic_sorted)

	everything_arr = enter_dic_sorted # Assign all entries of enter_dic_sorted into everything_arr
	for i in range(len(exit_dic_sorted)): # If the function name of the element in everything_arr == the function name of the element in exit_dic_sort
		for j in exit_dic_sorted:         # then append the exit time to everything_arr
			if (everything_arr[i][1] == j[1]):
				everything_arr[i].append(j[0])


		#print(exit_dic_sorted[i][0])

	# If the length of the list in everything_arr is greater than 4 (ie., more than one exit time because the function was called more than once), 
	# then figure out which exit time is the correct one and remove the ones that are not correct
	for i in everything_arr:
 		if ((len(i)) > 4):
 			if((i[3] > i[0]) and (i[3] < i[4])):
 				i.append(i[3])
 				del i[3]
 				del i[3]
 			else:
 				i.append(i[4])
 				del i[3]
 				del i[3]

 	for i in everything_arr:
 		print(i)

	print(tabulate(func_times_called, headers=['Function','Times-called']))