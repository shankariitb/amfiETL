import mysql.connector
import env


"""get connection with autocommit true. Note we are only inserting records at the end when we are sure that
entires days data is valid and schemeanem,typename,groupname we are only inserting if not present so autocommit true
wont cause any issues . No duplicate record insertion.
"""
def getconnection():
    try:
        conn = mysql.connector.connect(host = env.HOST,user = env.USER,password = env.PASS ,database = env.DB,autocommit = True)
    except Exception as ee:
        env.logger.error("Error While connecting to Mysql Server #$#",ee)
    else:
        return conn

##Insert scheme if not present
def insertScheme(schemeName,schemeId,cursor):
    curQuery = env.schemeUpsertQuery
    cursor.execute(curQuery,(schemeId,schemeName))


##insert if not present and getid
def getGroupId(groupName,cursor):
    curQuery = env.groupGetQuery
    cursor.execute(curQuery,(groupName,))
    data = cursor.fetchall()
    if len(data)==0:
        curQuery = env.groupInsertQuery
        cursor.execute(curQuery,(groupName,))
        return cursor.lastrowid
    return int(data[0][0])

##insert if not present and getid
def getTypeId(typeName,cursor):
    curQuery = env.typeGetQuery
    cursor.execute(curQuery,(typeName,))
    data = cursor.fetchall()
    if len(data)==0:
        curQuery = env.typeInsertQuery
        cursor.execute(curQuery,(typeName,))
        return cursor.lastrowid
    return int(data[0][0])

##insert records 
def insertIntoDb(records,cursor):
    curQuery = env.insertQuery
    cursor.executemany(curQuery,tuple(records))
