import tushare as tu
from datamanager.tusharemapper import stockmapper, dailyrecordmapper
from datamanager.datareader import stockreader


def sync_stocks():
    stocks_df = tu.get_stock_basics()
    result_count = stockmapper.sync_stock(stocks_df)
    print('股票列表已同步，新增%s，更新%s' % result_count)


def sync_dailyrecords(start_date, end_date):
    all_stocks = stockreader.get_all_stocks()
    # update_stocks = []
    for stock in all_stocks:
        stock_daily_df = tu.get_k_data(stock.code, start_date, end_date)
        dailyrecordmapper.write_dailyrecord(stock_daily_df)
        # sorted_df = stock_daily_df.set_index('date').sort_values(by=['date'], ascending=False)
        # newest_price = sorted_df.iloc[1]['close']
        # 更新股票市值
        # ori_value = stock.capitalization
        # stock.capitalization = newest_price * stock.totals
        # stock.update_remark = 'capitalization:%s->%s' % (ori_value, newest_price)
        # stock.update_time = datetime.datetime.now()
        # update_stocks.append(stock)

    # db_session.add_all(update_stocks)


if __name__ == '__main__':
    sync_stocks()
    sync_dailyrecords('2017-01-01','2018-10-09')
