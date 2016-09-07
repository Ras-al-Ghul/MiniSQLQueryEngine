import tables
import parser
import itertools

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
								temparr.append([str(float(float(sum)/len(database[j].cols[k]))),0])
			elif i[2] == 'SUM':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								sum = 0
								for l in database[j].cols[k]:
									sum += int(l)
								temparr.append([str(sum),0])
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
	#print action, listofarrs
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

	if andor:
		for i in range(len(firstcond)):
			for j in range(len(secondcond)):
				if firstcond[i][0] == secondcond[j][0]:
					firstset = set(firstcond[i][1])
					secondset = set(secondcond[j][1])
					temp = {}
					if andor[0] == 'and':
						temp = firstset & secondset
					else:
						temp = firstset | secondset
					templist = (list(temp))
					templist.sort()
					listofrows.append([firstcond[i][0], templist])

	for i in range(len(firstcond)):
		flag = 0
		for j in range(len(listofrows)):
			if firstcond[i][0] == listofrows[j][0]:
				flag = 1
				break
		if flag == 0:
			listofrows.append(firstcond[i])

	for i in range(len(secondcond)):
		flag = 0
		for j in range(len(listofrows)):
			if secondcond[i][0] == listofrows[j][0]:
				flag = 1
				break
		if flag == 0:
			listofrows.append(secondcond[i])

	#print firstcond, secondcond
	#print listofrows
	return listofrows

def findIndex(lists, key):
	for r in range(len(lists)):
		if lists[r]  == key:
			return r

def finalizeRows(action, listofarrs, listofrows, database):
	#In listofarrs
	tempset = set()
	finalrows = []
	for i in range(len(action)):
		if action[i][0] not in tempset:
			tempset.add(action[i][0])
	finalrows = []
	for i in tempset:
		finalrows.append([i,set(range(0,1000))])

	finalrows.sort()

	for i in range(len(action)):
		curtable = action[i][0]
		curcolumn = action[i][1]
		collist = listofarrs[i] 
		tempset = set([x[1] for x in collist])
		for j in range(len(finalrows)):
			if finalrows[j][0] == curtable:
				finalrows[j][1] = finalrows[j][1] & tempset

	#In listofrows
	for i in range(len(listofrows)):
		curtable = listofrows[i][0]
		tempset = set(listofrows[i][1])
		for j in range(len(finalrows)):
			if finalrows[j][0] == curtable:
				finalrows[j][1] = finalrows[j][1] & tempset
	
	for i in range(len(finalrows)):
		finalrows[i][1] = list(finalrows[i][1])
		finalrows[i][1].sort()
	print finalrows

	finaltable = []
	for i in range(len(finalrows)):
		curcol = finalrows[i][1]
		finaltable.append([])
		for j in curcol:
			finaltable[i].append([])

	for i in range(len(finalrows)):
		curtable = finalrows[i][0]
		curlist = finalrows[i][1]
		for j in range(len(action)):
			if action[j][0] == curtable:
				templist = listofarrs[j]
				for k in range(len(templist)):
					if templist[k][1] in curlist:
						finaltable[i][findIndex(curlist, templist[k][1])].append(templist[k][0])
	print finaltable

	crossproduct = []
	header = []
	for i in range(len(action)):
		header.append(action[i][1])
	crossproduct.append(header)

	if len(finaltable) == 2:
		for i in range(len(finaltable[0])):
			for j in range(len(finaltable[1])):
				templists = []
				for ii in finaltable[0][i]:
					templists.append(ii)
				for ii in finaltable[1][j]:
					templists.append(ii)
				crossproduct.append(templists)
	else:
		for i in range(len(finaltable[0])):
			crossproduct.append(finaltable[0][i])

	for i in crossproduct:
		for j in i:
			print j,
		print
	return finaltable

def startLoop(database):
	while 1:
		listofarrs = []
		listofrows = []
		inputStr = raw_input(">")
		if inputStr == 'q' or inputStr == 'Q':
			break
		else:
			try:
				columns, tables, where, action, wherelist, andor = parser.parseString(inputStr, database)
				if not action and not wherelist:
					continue
				if not wherelist:
					action, listofarrs = solveWithoutWhere(action, database)
				elif wherelist:
					action, listofarrs = solveWithoutWhere(action, database)
					listofrows = solveWhere(wherelist, andor, database)
				print action, "\n", wherelist, "\n", andor, "\n"
				print listofarrs, "\n", listofrows, "\n"
				finalizeRows(action, listofarrs, listofrows, database)
				#finalaction(listofarrs, listofrows)
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