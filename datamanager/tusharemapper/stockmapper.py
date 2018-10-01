import datetime
import pandas as pd
import tushare as tu
from pandas.core.series import Series
from project.database import db_session, Stock


def sync_stock():
    # df = tu.get_stock_basics()
    df = pd.read_csv('/home/vagrant/data/tmp/get_stock_basics_df.csv',converters={'code':lambda x:str(x)})  # TODO:临时数据读取
    df=df[0:2]# TODO:临时数据截断
    insert_queue = []
    update_queue = []

    for index, row in df.iterrows():
        insert_or_update(row, insert_queue, update_queue)

    if len(insert_queue):
        db_session.add_all(insert_queue)
        print('insert total:%s record  ' % len(insert_queue))
    if len(update_queue):
        db_session.bulk_save_objects(update_queue)
        print('update total %s record  ' % len(update_queue))

    try:
        db_session.commit()
        db_session.close()
    except Exception as ex:
        print('sqlalchemy execution occur exception,args:%s' % ex.args)
    else:
        pass


def insert_or_update(row, insert_queue, update_queue):
    all_matched = None
    try:
        all_matched = db_session.query(Stock).filter(Stock.code == row['code']).all()
    except Exception as e:
        str(e)
    else:
        pass

    stock = None

    if len(all_matched) > 0:
        stock = all_matched[0]

    if stock is None:
        stock = row_to_stock(row)
        stock.update_time = datetime.datetime.now()
        stock.update_remark = '新增'
        insert_queue.append(stock)
    else:
        update_msg = ''
        result_stock  = update_stock(row, stock, update_msg)
        if  result_stock is not None:
            stock.update_remark = update_msg
            stock.update_time = datetime.datetime.now()
            update_queue.append(stock)


def row_to_stock(row):
    if type(row) != Series:
        print('row type is not Series')
        return None

    new_stock = Stock(row['code'])
    for columnName in row.index:
        setattr(new_stock, columnName, row[columnName])
    return new_stock


def update_stock(row, stock, update_msg):
    if type(row) != Series or stock is None:
        return None
    has_change=False
    for columnName in row.index:
        if hasattr(stock, columnName):
            value = getattr(stock, columnName)
            if value != row[columnName]:
                setattr(stock, columnName, row[columnName])
                update_msg += '%s:%s->%s,' % (columnName, value, row[columnName])
                has_change=True
    if  has_change:
        return stock
    else:
        return None


if __name__ == '__main__':
    sync_stock()
