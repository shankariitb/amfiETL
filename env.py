import os
import loggerConfig

CONNECTIONS=10
startDate='2006-04-01'
cur_dir = os.getcwd()
log_dir = cur_dir+'/logs/'
logger = loggerConfig.get_my_logger('amfi',log_dir)
dbDateFormat = '%Y-%m-%d'
amfiDateFormat = '%d-%b-%Y'
urlFormat="https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt="
header="Scheme Code;Scheme Name;ISIN Div Payout/ISIN Growth;ISIN Div Reinvestment;Net Asset Value;Repurchase Price;Sale Price;Date"
HOST = '172.23.13.36'
USER = 'mirchi'
PASS = 'appcmsmirchi'
DB = 'music_logs'
insertQuery="""insert into nav_records (scheme_id,isin_div_payout_or_growth,isin_div_reinvestment,nav,repurchase_price,sale_price,record_date,group_id,type_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """

schemeGetQuery = """select id,scheme_id,name from scheme_table where scheme_id = (%s) """
schemeInsertQuery = """insert into scheme_table (scheme_id,name) values  (%s ,%s) """
schemeUpsertQuery = """insert into scheme_table (scheme_id,name) values (%s,%s) on DUPLICATE KEY update scheme_id = values(scheme_id)"""


groupGetQuery = """select id,name from group_table where name = (%s) """
groupInsertQuery = """insert into group_table (name) values (%s) """


typeGetQuery = """select id,name from type_table where name = (%s) """
typeInsertQuery = """insert into type_table (name) values (%s) """

##Assuming for now Name Not changing
# updateschemeNameQuery = """update scheme_table set name = '%s' where id = %s """
