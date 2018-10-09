import datetime, math
from decimal import Decimal
from pandas.core.series import Series
from datamanager.database import db_session, Stock


def sync_stock(df):
    insert_queue = []
    update_queue = []
    num = 1
    for index, row in df.iterrows():
        insert_or_update(row, insert_queue, update_queue)
        if num % 100 == 0:
            print('completed the %sth' % num)
        num += 1

    if len(insert_queue):
        batch_len = 100
        for x in range(math.ceil(len(insert_queue) / batch_len)):
            start = x * batch_len
            end = (x + 1) * batch_len
            db_session.add_all(insert_queue[start:end])
            try:
                db_session.commit()
                print('committed from %s to %s' % (start, end))
            except Exception as ex:
                print('commit occur exception,args:%s' % ex.args)
        print('insert total:%s record  ' % len(insert_queue))

    if len(update_queue):
        db_session.bulk_save_objects(update_queue)
        db_session.commit()
        print('update total %s record  ' % len(update_queue))

    if len(insert_queue) == 0 and len(update_queue) == 0:
        print('not any record need insert or update')
        return 0, 0

    try:
        # print('begin commit to database.')
        db_session.close()
        print('session has closed.')
    except Exception as ex:
        print('sqlalchemy execution occur exception,args:%s' % ex.args)
        return -1, -1

    return len(insert_queue), len(update_queue)


def insert_or_update(row, insert_queue, update_queue):
    all_matched = None
    try:
        all_matched = db_session.query(Stock).filter(Stock.code == row.name and Stock.isdel == False).all()
    except Exception as ex:
        print('sqlalchemy query occur exception,args:%s' % ex.args)

    stock = None
    if all_matched is None:
        return
    elif len(all_matched) == 1:
        stock = all_matched[0]

    if stock is None:
        stock = row_to_stock(row)
        stock.update_time = datetime.datetime.now()
        stock.update_remark = '新增'
        insert_queue.append(stock)
    else:
        has_changed = update_stock(row, stock)
        if has_changed:
            update_queue.append(stock)


def row_to_stock(row):
    if type(row) != Series:
        print('row type is not Series')
        return None

    code = row.name

    if type(code) == int and len(str(code)) < 6:
        code = '000000'[0:6 - len(str(code))] + str(code)

    new_stock = Stock(code)
    for columnName in row.index:
        if str.lower(columnName) == 'timetomarket':
            setattr(new_stock, columnName,get_correct_date(row[columnName]))
            continue
        setattr(new_stock, columnName, row[columnName])
    return new_stock

def get_correct_date(date_value):
    date_str = str(date_value)
    if len(date_str) == 8:
        return  datetime.datetime.strptime(date_str, '%Y%m%d').date()
    elif len(date_str) == 1:
        return  datetime.datetime.strptime('1970-01-01', '%Y-%m-%d').date()

def update_stock(achieved_row, exist_stock):
    if type(achieved_row) != Series or exist_stock is None:
        return None
    has_change = False
    update_remark = ''
    for columnName in achieved_row.index:
        if hasattr(exist_stock, columnName):
            ori_value = getattr(exist_stock, columnName)
            new_value = achieved_row[columnName]

            if type(ori_value) == Decimal:
                ori_value = float(ori_value)

            if type(ori_value) == datetime.date and type(new_value) == int:
                new_value =  get_correct_date(new_value)

            if ori_value != new_value:
                setattr(exist_stock, columnName, achieved_row[columnName])
                update_remark += '%s:%s->%s,' % (columnName, ori_value, achieved_row[columnName])
                setattr(exist_stock, 'update_remark', update_remark.rstrip(','))
                setattr(exist_stock, 'update_time', datetime.datetime.now())
                has_change = True
    return has_change
