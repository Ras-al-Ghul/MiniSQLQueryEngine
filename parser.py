# simpleSQL.py
#
# simple demo of using the parsing library to do simple-minded SQL parsing
# could be extended to include where clauses etc.
#
# Copyright (c) 2003,2016, Paul McGuire
#
from pyparsing import Literal, CaselessLiteral, Word, delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword, upcaseTokens

# define SQL tokens
selectStmt = Forward()
SELECT = Keyword("select", caseless=True)
FROM = Keyword("from", caseless=True)
WHERE = Keyword("where", caseless=True)

ident          = Word( alphas + '*', alphanums + "_$()" ).setName("identifier")
columnName     = ( delimitedList( ident, ".", combine=True ) ).setName("column name")
columnNameList = Group( delimitedList( columnName ) )
tableName      = ( delimitedList( ident, ".", combine=True ) ).setName("table name")
tableNameList  = Group( delimitedList( tableName ) )

whereExpression = Forward()
and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)
in_ = Keyword("in", caseless=True)

E = CaselessLiteral("E")
binop = oneOf("= != < > >= <= eq ne lt le gt ge", caseless=True)
arithSign = Word("+-",exact=1)
realNum = Combine( Optional(arithSign) + ( Word( nums ) + "." + Optional( Word(nums) )  |
                                                         ( "." + Word(nums) ) ) + 
            Optional( E + Optional(arithSign) + Word(nums) ) )
intNum = Combine( Optional(arithSign) + Word( nums ) + 
            Optional( E + Optional("+") + Word(nums) ) )

columnRval = realNum | intNum | quotedString | columnName # need to add support for alg expressions
whereCondition = Group(
    ( columnName + binop + columnRval ) |
    ( columnName + in_ + "(" + delimitedList( columnRval ) + ")" ) |
    ( columnName + in_ + "(" + selectStmt + ")" ) |
    ( "(" + whereExpression + ")" )
    )
whereExpression << whereCondition + ZeroOrMore( ( and_ | or_ ) + whereExpression ) 

# define the grammar
selectStmt <<= (SELECT + (columnNameList)("columns") + 
                FROM + tableNameList( "tables" ) + 
                Optional(Group(WHERE + whereExpression), "")("where"))

simpleSQL = selectStmt

# define Oracle comment format, and ignore them
oracleSqlComment = "--" + restOfLine
simpleSQL.ignore( oracleSqlComment )

def linkColTable(columns, tables, database):
    for table in tables:
        flag = False
        for i in range(len(database)):
            if table == database[i].name:
                flag = True
        if not flag:
            print table, "doesn't exist"
            return []

    actionList = []
    for col in columns:
        if col.find('.') == -1 and col.find('(') == -1 and col.find('*') == -1:
            flag = -1
            for table in tables:
                for i in range(len(database)):
                    if table == database[i].name:
                        for colm in database[i].labelsOfColumns:
                            if col == colm:
                                flag += 1
                                if flag == 1:
                                    print "Ambiguity in resolving columns into tables, try again"
                                    return []
                                else:
                                    actionList.append([table, col])
            if flag == -1:
                print "Column", col , "doesn't exist, try again"
                return []
        elif col == '*':
            for table in tables:
                for i in range(len(database)):
                    if table == database[i].name:
                        for colm in database[i].labelsOfColumns:
                            actionList.append([table, colm])
        elif col.find('.') != -1 and col.find('(') == -1:
            ind = col.find('.')
            tempt = col[:ind]
            tempcol = col[ind + 1:]
            tabflag = -1
            for table in tables:
                if tempt == table:
                    tabflag = 1
                    for i in range(len(database)):
                        if table == database[i].name:
                            flag = -1
                            for colm in database[i].labelsOfColumns:
                                if tempcol == colm:
                                    flag = 1
                                    actionList.append([table, tempcol])
                                    break
                            if flag == -1:
                                print "Column", tempcol , "doesn't exist, try again"
                                return []
            if tabflag == -1:
                print tempt, "not specified"
                return []
        elif col.find('(') != -1:
            ind = col.find('(')
            keyword = col[:ind]
            if col.find('.') == -1:
                tempcol = col[ind + 1:col.find(')')]
                flag = -1
                for table in tables:
                    for i in range(len(database)):
                        if table == database[i].name:
                            for colm in database[i].labelsOfColumns:
                                if tempcol == colm:
                                    flag += 1
                                    if flag == 1:
                                        print "Ambiguity in resolving columns into tables, try again"
                                        return []
                                    actionList.append([table, tempcol, keyword])
                                    break
                if flag == -1:
                    print "Column", tempcol , "doesn't exist, try again"
                    return []
            else:
                tempt = col[ind + 1:col.find('.')]
                tempcol = col[col.find('.') + 1:col.find(')')]
                tabflag = -1
                for table in tables:
                    if tempt == table:
                        tabflag = 1
                        for i in range(len(database)):
                            if table == database[i].name:
                                flag = -1
                                for colm in database[i].labelsOfColumns:
                                    if tempcol == colm:
                                        flag = 1
                                        actionList.append([table, tempcol, keyword])
                                        break
                                if flag == -1:
                                    print "Column", tempcol , "doesn't exist, try again"
                                    return []
                if tabflag == -1:
                    print tempt, "not specified"
                    return []
        else:
            print "Try Again"
            return []
    return actionList

def linkWhereTable(where, tables, database):
    whereList = []
    andor = []
    for i in range(len(where[0])):
        if i == 0:
            continue
        elif i == 2:
            andor.append(where[0][i])
        else:
            temp = []
            temparr = where[0][i]
            for j in range(len(temparr)):
                if j == 1:
                    continue
                elif temparr[j].find('.') == -1:
                    if temparr[j].isdigit() or temparr[j][:1] == '-':
                        temp.append([temparr[j]])
                    else:
                        tempcol = temparr[j]
                        flag = -1
                        for table in tables:
                            for l in range(len(database)):
                                if table == database[l].name:
                                    for k in database[l].labelsOfColumns:
                                        if k == tempcol:
                                            flag += 1
                                            if flag == 1:
                                                print "Ambiguity in resolving columns"
                                                return [], andor
                                            temp.append([table, tempcol])
                        if flag == -1:
                            print tempcol, "not found"
                            return [], andor
                elif temparr[j].find('.') != -1:
                    temptable = temparr[j][:temparr[j].find('.')]
                    tempcol = temparr[j][temparr[j].find('.') + 1:]
                    tabflag = -1
                    for table in tables:
                        if temptable == table:
                            tabflag = 1
                            for l in range(len(database)):
                                if temptable == database[l].name:
                                    flag = -1
                                    for k in database[l].labelsOfColumns:
                                        if k == tempcol:
                                            flag = 1
                                            temp.append([temptable, tempcol])
                                            break
                                    if flag == -1:
                                        print tempcol, "not found"
                                        return [], andor
                    if tabflag == -1:
                        print temptable, "doesn't exist in provided table list"
                        return [], andor
                if j == 2:
                    whereList.append(temp)
    return whereList, andor

def parseString(rawString, database):
    sqlstmt = simpleSQL.parseString(rawString)
    actionList = linkColTable(sqlstmt.columns, sqlstmt.tables, database)
    whereList, andor = linkWhereTable(sqlstmt.where, sqlstmt.tables, database)
    return sqlstmt.columns, sqlstmt.tables, sqlstmt.where, actionList, whereList, andor

if __name__ == "__main__":
    sqlstmt = simpleSQL.parseString("select distinct(table1.B) from table1, table2;")
    print sqlstmt.columns, sqlstmt.tables, sqlstmt.where
