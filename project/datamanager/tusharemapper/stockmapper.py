import tushare as tu
from project import database


def syncstock():
    df=tu.get_stock_basics()
    for 