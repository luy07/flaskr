import unittest
from datamanager import config
config.TEST=True
import pandas as pd
from datamanager import database
from datamanager.tusharemapper import dailyrecordmapper
from datamanager.datareader import dailyrecordreader

class DailylrecordMapperTest(unittest.TestCase):
    def setUp(self):
        database.drop_all()
        database.create_all()

    def tearDown(self):
        database.drop_all()

    def get_df(self):
        df = pd.read_csv('/home/vagrant/data/tmp/rdgf_daily.csv', converters={'code': lambda x: str(x)})
        # df = pd.read_csv('/home/vagrant/data/tmp/rdgf_daily.csv')
        return df

    def test_dailyrecord_async(self):
        df=self.get_df()
        sorted_df=df.set_index('code').sort_values(by=['date'],ascending=True)
        code=sorted_df.iloc[1].name
        begindate=sorted_df.iloc[0]['date']
        enddate=sorted_df.iloc[-1]['date']
        dailyrecords=dailyrecordreader.get_dailyrecords(code,begindate,enddate)
        self.assertEqual(len(dailyrecords), 0)
        dailyrecordmapper.write_dailyrecord(df)
        dailyrecords=dailyrecordreader.get_dailyrecords(code,begindate,enddate)
        assert  dailyrecords is not None
        self.assertEqual(len(dailyrecords),sorted_df.index.size)

