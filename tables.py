import os
import sys
import glob
import csv

class Table:
	def __init__(self, csvfilename, metadata):
		self.name = metadata[0]
		self.numOfColumns = len(metadata) - 1
		self.labelsOfColumns = metadata[1:]
		self.rows = []
		self.cols = []
		self.readRowsAndCols(csvfilename, self.numOfColumns)

	def readRowsAndCols(self, csvfilename, numOfColumns):
		with open(csvfilename, 'r') as csvfile:
			contents = csv.reader(csvfile, delimiter=',')
			for c in contents:
				self.rows.append(c)
				for index, temp in enumerate(c):
					if len(self.cols) <= index:
						self.cols.append([])
					self.cols[index].append(temp)

def getPathToDir():
	print "Please enter the path to the directory in which the metafile and the csvfiles exist, Q or q to quit"
	dirpath = raw_input(">")
	if dirpath == "Q" or dirpath == "q":
		sys.exit()
	#elif not os.path.isdir(dirpath):
		print "Invalid path"
		return getPathToDir()
	else:
		dirpath = '/root/Desktop/Assignment1'
		return dirpath

def getCSVFiles(path):
	files = []
	os.chdir(path)
	for file in glob.glob('*.csv'):
		files.append(file)
	files.sort()
	return files

def readMetaFile(path):
	tables = []
	attributes = []
	try:
		with open(path+'/metadata.txt','r') as metafile:
			metaFileContent = metafile.read().splitlines()
			for line in metaFileContent:
				if line == "<begin_table>":
					continue
				elif line == "<end_table>":
					tables.append(attributes)
					attributes = []
				else:
					attributes.append(line)
		tables.sort()
		return tables
	except:
		print "Couldn't read metafile"
		return False

def printSchema(database):
	print "\nThe schema is\n"
	for i in range(len(database)):
		nameOfTable = database[i].name
		labelsOfCols = database[i].labelsOfColumns
		print nameOfTable
		for j in labelsOfCols:
			print j,
		print "\n"

def createDatabase():
	while 1:
		dirpath = getPathToDir()
		csvfiles = getCSVFiles(dirpath)
		tables = readMetaFile(dirpath)
		if not csvfiles or not tables:
			print "No csv files found or no metafile found, enter correct dir again"
		elif len(csvfiles) != len(tables):
			print "Number of tables in metafile.txt not same as number of csvfiles"
		else:
			break

	# print csvfiles
	# print tables
	database = []
	for i in range(len(tables)):
		if csvfiles[i][:len(csvfiles[i]) - 4] != tables[i][0]:
			print "Sort the metadata file according to Table Names and then try or inspect the table names and csv file names"
			sys.exit()
		database.append(Table(csvfiles[i], tables[i]))
		# print database[i].__dict__
		# print

	printSchema(database)

	return database

def main():
	database = createDatabase()
	for i in range(len(database)):
		print database[i].__dict__

if __name__ == '__main__':
	main()