import unittest
import pandas as pd
from datamanager import config
config.TEST=True
from datamanager.tusharemapper import stockmapper
from datamanager.datareader import stockreader
from datamanager import database

class StockMapper_TestCase(unittest.TestCase):

    def setUp(self):
        database.create_all()
        pass

    def tearDown(self):
        database.drop_all()
        pass

    def get_df(self):
        df = pd.read_csv('/home/vagrant/data/tmp/get_stock_basics_df.csv',converters={'code': lambda x: str(x), 'esp': lambda y: round(float(y), 3)})
        df = df.set_index('code')  # 数据截断，并指定code列为索引
        return df

    # @unittest.skip('ok')
    def test_stocksync_insert_fromcsv(self):
        stocks = stockreader.get_all_stocks()
        assert stocks is None or len(stocks) == 0

        stockmapper.sync_stock(self.get_df())

        stocks = stockreader.get_all_stocks()
        assert stocks is not None and len(stocks) > 0

    def test_stocksync_update(self):
        df = self.get_df()
        code = df.iloc[1].name

        stockmapper.sync_stock(df)
        stock = stockreader.get_stock(code)
        assert stock is not None

        ori_pe = df.loc[code, 'pe']
        df.loc[code, 'pe'] = 999  # 修改pe值

        stockmapper.sync_stock(df)
        stock = stockreader.get_stock(code)

        assert stock is not None
        self.assertEqual(stock.pe, 999)
        expected = 'pe:' + str(ori_pe) + '->' + '999.0'
        self.assertEqual(stock.update_remark, expected)


