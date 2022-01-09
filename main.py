import concurrent.futures
import env
import requests
import dbUtil
from datetime import date,timedelta,datetime
import os
import sys


##Shared across threads so no problem also even if ovewritting is done always correct there will be a valid value 
groupMap = {}
typeMap = {}
schemeSet = set()


##Fetches all urls and date formats
def getAllUrls(complete):
    end_date_obj   = date.today()-timedelta(days=1)
    end_date_obj1   = date.today()-timedelta(days=1)
    end_date_obj = datetime.combine(end_date_obj, datetime.min.time())
    end_date_obj1 = datetime.combine(end_date_obj1, datetime.min.time())
    startDate = env.startDate       
    start_date_obj = datetime.strptime(env.startDate, env.dbDateFormat)
    if not complete:
        start_date_obj = end_date_obj1
    urls = []
    while start_date_obj <= end_date_obj:
        urls.append([env.urlFormat+start_date_obj.strftime(env.amfiDateFormat),start_date_obj.strftime(env.dbDateFormat)])
        start_date_obj = start_date_obj+timedelta(days=1)
    print(urls)
    return urls


###Insert into map so that if we encounter this group again no need to find id again
def getGroupId(group,cursor):
    if group not in groupMap:
        groupMap[group] = dbUtil.getGroupId(group,cursor)
    return groupMap[group]


###Insert into set so that if we encounter this scheme again no need to reinsert
def insertScheme(scheme,schemeId,cursor):
    if schemeId not in schemeSet:
        dbUtil.insertScheme(scheme,schemeId,cursor)
        schemeSet.add(schemeId)

###Insert into map so that if we encounter this type again no need to find id again
def getTypeId(typeName,cursor):
    if typeName not in typeMap:
        typeMap[typeName] = dbUtil.getTypeId(typeName,cursor)
    return typeMap[typeName]


def preProcessandInsert(text,dateStr):
    lines = text.split('\n');
    try:
        tempLine = lines[0].replace('\r','')
        assert env.header==tempLine
    except AssertionError as msg:
        env.logger.error("Header Not macthing for #$#%s",dateStr)
        return
    except Exception as e:
        env.logger.error("Exception while Checking Header #$#%s",dateStr)
        return
    count = 0
    groupId = 0
    typeId = 0
    insertData = []
    ##Both not thread safe so better open and close inside thread
    conn = dbUtil.getconnection()
    cursor = conn.cursor()
    for i in range(1,len(lines)):
        try:
            line = lines[i].replace('\r','')
            #print(line)
            if len(line)==0 or line.isspace():
                count+=1
                continue
            else:
                if count==1:
                    #maybe Group or Type(check i limits)
                    if lines[i+1].isspace():
                        typeId = getTypeId(line,cursor)
                    else:
                        ##Group
                        groupId = getGroupId(line,cursor)
                    count = 0
                    continue
                elif count==2:
                    ##Definetly Group
                    groupId = getGroupId(line,cursor)
                    count = 0
                    continue
                else:
                    fundData = line.split(';')
                    insertScheme(fundData[1],fundData[0],cursor)
                    fundData.pop(1)
                    # fundData[1] = fundId
                    fundData[0]=int(fundData[0])
                    for k in range(3,6):
                        ##Here this if we replace commas and if then can be case to float then valid this removes cases like ('','-','N.A.','NA' and any future ones)
                        ##Default 0.00 which implies invalid under the assumption that nav can't be 0 in practical cases
                        try:
                            fundData[k]=float(fundData[k].replace(',',''))
                        except:
                            fundData[k]=0.0000
                    fundData[-1] = datetime.strptime(dateStr, env.dbDateFormat).date()
                    fundData.append(groupId)
                    fundData.append(typeId)
                    insertData.append(tuple(fundData))
                    count = 0
        except Exception as ee:
            print("Error While Iterating File #$#%s,%s",dateStr,lines[i])
            cursor.close()
            conn.close()
            return
    dbUtil.insertIntoDb(insertData,cursor)
    print(dateStr)
    env.logger.info("loading data Done for #$#%s",dateStr)
    cursor.close()
    conn.close()
        

def load_url(url):
    ans = requests.get(url[0])
    return ans.text,url[1]


def complete(urlist):
    with concurrent.futures.ThreadPoolExecutor(max_workers=env.CONNECTIONS) as executor:
        future_to_url = (executor.submit(load_url,url) for url in urlist)
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data,dateStr = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                preProcessandInsert(data,dateStr)

if __name__ == '__main__':
    print(sys.argv)
    try:
        assert len(sys.argv)==2
    except AssertionError as msg:
        print("use argument 0 for full data load or 1 for T-1 day")
        sys.exit(0)
    if int(sys.argv[1])==0:
        complete(getAllUrls(True))
    else:
        complete(getAllUrls(False))

