import tables
import parser
import itertools
import copy
from terminaltables import AsciiTable

def preProcess(action, database, listofrows = []):
	listofarrs = []
	for i in action:
		temparr = []
		temptable = i[0]
		tempcolumn = i[1]
		if len(i) == 3:
			if i[2] == 'MAX' or i[2] == 'max':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								tempmax = -1111111111
								index = -1
								if listofrows:
									tabflag = 0
									for z in range(len(listofrows)):
										if listofrows[z][0] == temptable:
											tabflag = 1
											templistofrowscol = listofrows[z][1]
											for l in range(len(database[j].cols[k])):
												if int(database[j].cols[k][l]) > tempmax and l in templistofrowscol:
													tempmax = int(database[j].cols[k][l])
													index = l
											if tempmax != -1111111111:
												temparr.append([str(tempmax),0])
									if tabflag == 0:
										for l in range(len(database[j].cols[k])):
											if int(database[j].cols[k][l]) > tempmax:
												tempmax = int(database[j].cols[k][l])
												index = l
										if tempmax != -1111111111:
											temparr.append([str(tempmax),0])	
								else:
									for l in range(len(database[j].cols[k])):
										if int(database[j].cols[k][l]) > tempmax:
											tempmax = int(database[j].cols[k][l])
											index = l
									if tempmax != -1111111111:
										temparr.append([str(tempmax),0])
			elif i[2] == 'MIN' or i[2] == 'min':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								tempmin = 1111111110
								index = -1
								if listofrows:
									tabflag = 0
									for z in range(len(listofrows)):
										if listofrows[z][0] == temptable:
											tabflag = 1
											templistofrowscol = listofrows[z][1]
											for l in range(len(database[j].cols[k])):
												if int(database[j].cols[k][l]) < tempmin and l in templistofrowscol:
													tempmin = int(database[j].cols[k][l])
													index = l
											if tempmin != 1111111110:
												temparr.append([str(tempmin),0])
									if tabflag == 0:
										for l in range(len(database[j].cols[k])):
											if int(database[j].cols[k][l]) < tempmin:
												tempmin = int(database[j].cols[k][l])
												index = l
										if tempmin != 1111111110:
											temparr.append([str(tempmin),0])	
								else:
									for l in range(len(database[j].cols[k])):
										if int(database[j].cols[k][l]) < tempmin:
											tempmin = int(database[j].cols[k][l])
											index = l
									if tempmin != 1111111110:
										temparr.append([str(tempmin),0])
			elif i[2] == 'AVG' or i[2] == 'avg':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								sum = 0
								if listofrows:
									tabflag = 0
									for z in range(len(listofrows)):
										if listofrows[z][0] == temptable:
											tabflag = 1
											templistofrowscol = listofrows[z][1]
											noofentries = 0
											for l in range(len(database[j].cols[k])):
												if l in templistofrowscol:
													sum += int(database[j].cols[k][l])
													noofentries += 1
											temparr.append([str(float(float(sum)/noofentries)),0])
									if tabflag == 0:
										for l in database[j].cols[k]:
											sum += int(l)
										temparr.append([str(float(float(sum)/len(database[j].cols[k]))),0])	
								else:
									for l in database[j].cols[k]:
										sum += int(l)
									temparr.append([str(float(float(sum)/len(database[j].cols[k]))),0])
			elif i[2] == 'SUM' or i[2] == 'sum':
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								sum = 0
								if listofrows:
									tabflag = 0
									for z in range(len(listofrows)):
										if listofrows[z][0] == temptable:
											tabflag = 1
											templistofrowscol = listofrows[z][1]
											for l in range(len(database[j].cols[k])):
												if l in templistofrowscol:
													sum += int(database[j].cols[k][l])
											temparr.append([str(sum),0])
									if tabflag == 0:
										for l in database[j].cols[k]:
											sum += int(l)
										temparr.append([str(sum),0])	
								else:
									for l in database[j].cols[k]:
										sum += int(l)
									temparr.append([str(sum),0])
			else:#DISTINCT
				for j in range(len(database)):
					if temptable == database[j].name:
						for k in range(len(database[j].labelsOfColumns)):
							if database[j].labelsOfColumns[k] == tempcolumn:
								used = []
								newtemparr = [[x,database[j].cols[k].index(x)] for x in database[j].cols[k] if x not in used and (used.append(x) or True)]
								temparr = []
								if listofrows:
									tabflag = 0
									for z in range(len(listofrows)):
										if temptable == listofrows[z][0]:
											tabflag = 1
											templistofrowscol = listofrows[z][1]
											for y in range(len(newtemparr)):
												if newtemparr[y][1] in templistofrowscol:
													temparr.append([newtemparr[y][0], newtemparr[y][1]])
									if tabflag == 0:
										temparr = newtemparr
								else:
									temparr = newtemparr
			i.pop()
		else:
			for j in range(len(database)):
				if temptable == database[j].name:
					for k in range(len(database[j].labelsOfColumns)):
						if database[j].labelsOfColumns[k] == tempcolumn:
							if listofrows:
								tabflag = 0
								for z in range(len(listofrows)):
									if temptable == listofrows[z][0]:
										tabflag = 1
										templistofrowscol = listofrows[z][1]
										for l in range(len(database[j].cols[k])):
											if l in templistofrowscol:
												temparr.append([database[j].cols[k][l],l])
								if tabflag == 0:
									for l in range(len(database[j].cols[k])):
										temparr.append([database[j].cols[k][l],l])	
							else:
								for l in range(len(database[j].cols[k])):
									temparr.append([database[j].cols[k][l],l])
		listofarrs.append(temparr)

	return action, listofarrs

def solveWithoutWhere(action, database, listofrows = []):
	action, listofarrs = preProcess(action, database, listofrows)
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

def furtherSolve(listofrows, wherelist, val, database, andor):
	cond = []
	if wherelist[val][0][0] == wherelist[val][1][0] or len(wherelist[val][1]) == 1:
		temp = []
		if wherelist[val][0][0] == wherelist[val][1][0]:
			temptable = wherelist[val][0][0]
			tempcol1 = wherelist[val][0][1]
			tempcol2 = wherelist[val][1][1]
			
			templistofrowstable = []
			for z in listofrows:
				if z[0] == temptable:
					templistofrowstable = z[1]

			for i in range(len(database)):
				if temptable == database[i].name:
					j = (database[i].labelsOfColumns).index(tempcol1)
					k = (database[i].labelsOfColumns).index(tempcol2)
					for l in range(len(database[i].cols[j])):
						if database[i].cols[j][l] == database[i].cols[k][l] and l in templistofrowstable:
							temp.append(l)
			for z in listofrows:
				if z[0] == temptable:
					if andor and andor[0] == 'and':
						z[1] = list(set(temp) & set(z[1]))
						z[1].sort()
					else:
						z[1] = list(set(temp) | set(z[1]))
						z[1].sort()
		else:
			temptable = wherelist[val][0][0]
			tempcol = wherelist[val][0][1]

			templistofrowstable = []
			for z in listofrows:
				if z[0] == temptable:
					templistofrowstable = z[1]

			for i in range(len(database)):
				if temptable == database[i].name:
					j = (database[i].labelsOfColumns).index(tempcol)
					for l in range(len(database[i].cols[j])):
						if database[i].cols[j][l] == wherelist[val][1][0] and l in templistofrowstable:
							temp.append(l)
			for z in listofrows:
				if z[0] == temptable:
					if andor and andor[0] == 'and':
						z[1] = list(set(temp) & set(z[1]))
						z[1].sort()
					else:
						z[1] = list(set(temp) | set(z[1]))
						z[1].sort()
	else:
		temp1 = []
		temp2 = []
		temptable1 = wherelist[val][0][0]
		temptable2 = wherelist[val][1][0]
		tempcol1 = wherelist[val][0][1]
		tempcol2 = wherelist[val][1][1]

		templistofrowstable1 = []
		templistofrowstable2 = []
		for z in listofrows:
			if z[0] == temptable1:
				templistofrowstable1 = z[1]
			if z[0] == temptable2:
				templistofrowstable2 = z[1]

		for i in range(len(database)):
			for j in range(len(database)):
				if database[i].name == temptable1 and database[j].name == temptable2:
					k = (database[i].labelsOfColumns).index(tempcol1)
					l = (database[j].labelsOfColumns).index(tempcol2)
					for m in range(len(database[i].cols[k])):
						for n in range(len(database[j].cols[l])):
							if database[i].cols[k][m]  == database[j].cols[l][n] and m in templistofrowstable1 and n in templistofrowstable2:
								temp1.append(m)
								temp2.append(n)
		for z in listofrows:
			if z[0] == temptable1:
				if andor and andor[0] == 'and':
					z[1] = list(set(temp1) & set(z[1]))
					z[1].sort()
				else:
					z[1] = list(set(temp1) | set(z[1]))
					z[1].sort()
			if z[0] == temptable2:
				if andor and andor[0] == 'and':
					z[1] = list(set(temp2) & set(z[1]))
					z[1].sort()
				else:
					z[1] = list(set(temp2) | set(z[1]))
					z[1].sort()
					
	return listofrows

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

	listofrows = furtherSolve(listofrows, wherelist, 0, database, andor)

	if len(wherelist) == 2:
		listofrows = furtherSolve(listofrows, wherelist, 1, database, andor)

	return listofrows

def findIndex(lists, key):
	for r in range(len(lists)):
		if lists[r]  == key:
			return r

def appendCrossProduct(crossproduct, finaltable, level, templists):
	if level == 1:
		for i in finaltable[len(finaltable) - level]:
			for j in i:
				templists.append(j)
			crossproduct.append(copy.deepcopy(templists))
			for j in i:
				templists.pop()
		return crossproduct, templists

	for i in finaltable[len(finaltable) - level]:
		for j in i:
			templists.append(j)
		crossproduct, templists = appendCrossProduct(crossproduct, finaltable, level - 1, templists)
		for j in i:
			templists.pop()
	return crossproduct, templists


def finalizeRows(action, listofarrs, listofrows, database, tempaction):
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
	
	for i in range(len(finalrows)):
		finalrows[i][1] = list(finalrows[i][1])
		finalrows[i][1].sort()

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

	crossproduct = []
	header = []
	for i in range(len(tempaction)):
		if len(tempaction[i]) == 3:
			tempheader = tempaction[i][2] + '(' + tempaction[i][0] + '.' + tempaction[i][1] + ')'
			header.append(tempheader)
		else:
			header.append(tempaction[i][0] + '.' + tempaction[i][1])
	crossproduct.append(header)

	crossproduct, templists = appendCrossProduct(crossproduct, finaltable, len(finaltable), [])

	table = []
	if len(crossproduct) != 1:
		table = AsciiTable(crossproduct)
		print table.table
	else:
		print
	return table

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
				tempaction = copy.deepcopy(action)
				if not action and not wherelist:
					continue
				if not wherelist:
					action, listofarrs = solveWithoutWhere(action, database)
				elif wherelist:
					listofrows = solveWhere(wherelist, andor, database)
					action, listofarrs = solveWithoutWhere(action, database, listofrows)
				finalizeRows(action, listofarrs, listofrows, database, tempaction)
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