import datetime
import tushare as tu
from project.database import db_session,Stock

def syncStock():
    df=tu.get_stock_basics()
    df=df[0:50]
    insert_queue=[]
    update_queue=[]

    for index,row in df.iterrows():
        insertOrUpdate(index,row, insert_queue, update_queue)

    if len(insert_queue):
        db_session.add_all(insert_queue)
        print('insert success,count:%s'% len(insert_queue))

    db_session.commit()
    db_session.close()

def insertOrUpdate(code,row,insert_queue,update_queue):
    if not code:
        pass

    all_matched=None

    try:
        all_matched=db_session.query(Stock).filter(Stock.code==code).all()
    except Exception as e:
        str(e)
    else:
        pass

    stock=None

    if len(all_matched)>0:
        stock=all_matched[0]

    if  stock is None:
        stock=Stock()
        stock.code=code
        stock.name=row['name']
        stock.area=row['area']
        stock.update_time=datetime.datetime.now()
        stock.update_remark='新增'
        insert_queue.append(stock)
    else:
        stock.industry=row['industry']
        stock.update_time=datetime.datetime.now()

if __name__=='__main__':
    syncStock()




