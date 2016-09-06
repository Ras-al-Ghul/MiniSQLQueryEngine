import tables
import parser

def startLoop(database):
	while 1:
		inputStr = raw_input(">")
		if inputStr == 'q' or inputStr == 'Q':
			break
		else:
			try:
				columns, tables, where = parser.parseString(inputStr, database)
				print columns, tables, where
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