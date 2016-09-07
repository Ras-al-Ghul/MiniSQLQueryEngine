import tables
import parser

def preProcess(action, database):
	listofarrs = []
	for i in action:
		temparr = []
		temptable = i[0]
		tempcolumn = i[1]
		if len(i) == 3:
			if i[2] == 'MAX':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								tempmax = -1111111111
								index = -1
								for l in range(len(database[j].cols[k])):
									if int(database[j].cols[k][l]) > tempmax:
										tempmax = int(database[j].cols[k][l])
										index = l
								temparr.append([str(tempmax),index])
			elif i[2] == 'MIN':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								tempmin = 1111111110
								index = -1
								for l in range(len(database[j].cols[k])):
									if int(database[j].cols[k][l]) < tempmin:
										tempmin = int(database[j].cols[k][l])
										index = l
								temparr.append([str(tempmin),index])
			elif i[2] == 'AVG':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								sum = 0
								for l in database[j].cols[k]:
									sum += int(l)
								temparr.append([str(float(float(sum)/len(database[j].cols[k]))),-1])
			elif i[2] == 'SUM':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								sum = 0
								for l in database[j].cols[k]:
									sum += int(l)
								temparr.append([str(sum),-1])
			else:#DISTINCT
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								used = []
								temparr = [[x,database[j].cols[k].index(x)] for x in database[j].cols[k] if x not in used and (used.append(x) or True)]
			i.pop()
		else:
			for j in range(len(database)):
				if temptable == database[j].name:
					for k in range(len(database[j].labelsOfColumns)):
						if database[j].labelsOfColumns[k] == tempcolumn:
							for l in range(len(database[j].cols[k])):
								temparr.append([database[j].cols[k][l],l])
		listofarrs.append(temparr)

	return action, listofarrs

def solveWithoutWhere(action, database):
	action, listofarrs = preProcess(action, database)
	print action, listofarrs
	return action, listofarrs

def subSolveWhere(wherelist, val, database):
	cond = []
	if wherelist[val][0][0] == wherelist[val][1][0] or len(wherelist[val][1]) == 1:
		temp = []
		if wherelist[val][0][0] == wherelist[val][1][0]:
			temptable = wherelist[val][0][0]
			tempcol1 = wherelist[val][0][1]
			tempcol2 = wherelist[val][1][1]
			for i in range(len(database)):
				if temptable == database[i].name:
					j = (database[i].labelsOfColumns).index(tempcol1)
					k = (database[i].labelsOfColumns).index(tempcol2)
					for l in range(len(database[i].cols[j])):
						if database[i].cols[j][l] == database[i].cols[k][l]:
							temp.append(l)
		else:
			temptable = wherelist[val][0][0]
			tempcol = wherelist[val][0][1]
			for i in range(len(database)):
				if temptable == database[i].name:
					j = (database[i].labelsOfColumns).index(tempcol)
					for l in range(len(database[i].cols[j])):
						if database[i].cols[j][l] == wherelist[val][1][0]:
							temp.append(l)
		cond.append([wherelist[val][0][0], temp])
	else:
		temp1 = []
		temp2 = []
		temptable1 = wherelist[val][0][0]
		temptable2 = wherelist[val][1][0]
		tempcol1 = wherelist[val][0][1]
		tempcol2 = wherelist[val][1][1]
		for i in range(len(database)):
			for j in range(len(database)):
				if database[i].name == temptable1 and database[j].name == temptable2:
					k = (database[i].labelsOfColumns).index(tempcol1)
					l = (database[j].labelsOfColumns).index(tempcol2)
					for m in range(len(database[i].cols[k])):
						for n in range(len(database[j].cols[l])):
							if database[i].cols[k][m]  == database[j].cols[l][n]:
								temp1.append(m)
								temp2.append(n)
		cond.append([temptable1, temp1])
		cond.append([temptable2, temp2])
	return cond

def solveWhere(wherelist, andor, database):
	listofrows = []
	firstcond = []
	secondcond = []
	for i in range(len(wherelist)):
		for j in range(len(wherelist[i])):
			if j == 0 and len(wherelist[i][j]) == 1:
				print "Integer to be on RHS"
				return []
	firstcond = subSolveWhere(wherelist, 0, database)
	if len(wherelist) == 2:
		secondcond = subSolveWhere(wherelist, 1, database)

	print firstcond, secondcond

def startLoop(database):
	while 1:
		listofarrs = []
		inputStr = raw_input(">")
		if inputStr == 'q' or inputStr == 'Q':
			break
		else:
			try:
				columns, tables, where, action, wherelist, andor = parser.parseString(inputStr, database)
				print action
				print wherelist, andor
				if not action and not wherelist:
					continue
				if not wherelist:
					action, listofarrs = solveWithoutWhere(action, database)
				elif wherelist:
					action, listofarrs = solveWithoutWhere(action, database)
					solveWhere(wherelist, andor, database)
				#print columns, tables, where
			except Exception, e:
				print e
				continue
		print

def main():
	database = tables.createDatabase()
	if not database:
		print "Error occured while populating database. Try again"
		sys.exit()
	print "Enter your query, q to quit" 
	startLoop(database)

if __name__ == '__main__':
	main()