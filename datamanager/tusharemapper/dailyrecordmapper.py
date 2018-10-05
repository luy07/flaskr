import pandas as pd

def sync_dailyrecord():
    df=pd.read_csv('/home/vagrant/data/tmp/rdgf_daily.csv',
                     converters={'code': lambda x: str(x), 'esp': lambda y: round(float(y), 3)},
                     index_col=0)  # TODO:临时数据读取
    df=df[0:100]