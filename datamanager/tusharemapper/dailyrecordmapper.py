from pandas import DataFrame,Series
from datamanager.database import db_session,DailyRecord
from datamanager.datareader import dailyrecordreader
import datetime

def write_dailyrecord(df):
    if not isinstance(df,DataFrame):
        raise TypeError('required type is DataFrame,but through in %'% type(df))

    insert_queue=[]
    for index,row in df.iterrows():
        code=row['code']
        date=row['date']
        exitstocks= dailyrecordreader.get_dailyrecords(code,date,date)
        if  exitstocks is not None and len(exitstocks)>0:
            continue
        stock=row_to_stock(row)
        if  stock is not None:
            insert_queue.append(stock)

    if  len(insert_queue)>0:
        db_session.add_all(insert_queue)

    try:
        db_session.commit()
        db_session.close()
    except Exception as ex:
        print('sqlalchemy execution occur exception,args:%s' % ex.args)

def row_to_stock(row):
    if type(row) != Series:
        print('row type is not Series')
        return None

    new_stock = DailyRecord(row['code'])
    for columnName in row.index:
        if str.lower(columnName) =='date':
            row_value=str(row[columnName])
            if len(row_value)==10:
                setattr(new_stock, columnName, datetime.datetime.strptime(row_value, '%Y-%m-%d').date())
                continue
        setattr(new_stock,columnName,row[columnName])
    return new_stock
