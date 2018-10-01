from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from . import config

engine = create_engine(config.DATABASE_URI, convert_unicode=True, **config.DATABASE_CONNECT_OPTIONS)

Model = declarative_base(name='Model')

# Model.query = db_session.query_property()
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def init_db():
    Model.metadata.drop_all(bind=engine)
    Model.metadata.create_all(bind=engine)


class TradeModel:
    """
    主要交易字段
    """
    price = Column(Float)  # 最新价
    volume = Column(Integer)  # 成交量
    change = Column(Float)  # 涨跌值，真实小数（非百分比）
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    turnover_rate = Column(Float)  # 换手率
    relative_ratio = Column(Float)  # 量比


class Stock(Model):
    __tablename__ = 'stocks'
    code = Column(String(50), primary_key=True)
    name = Column(String(50))
    intro = Column(String(500))
    tag = Column(String(500))  # 板块标签，逗号分隔
    industry = Column(String(50))  # 所属行业
    area = Column(String(50))  # 地区

    timeToMarket = Column(DateTime)  # 上市日期
    update_time = Column(DateTime)
    update_remark = Column(String(500))  # 更新备注
    risk_warnning = Column(String(500))  # 风险提示
    # 重要指标
    pe = Column(Float)  # 市盈率
    pb = Column(Float)  # 市净率
    # 总值
    capitalization = Column(Float)  # 市值
    outstanding = Column(Float)  # 流通股本(亿)
    totals = Column(Float)  # 总股本(亿)
    holders = Column(Integer)  # 股东人数
    totalAssets = Column(Float(10,5))  # 总资产(万)
    liquidAssets = Column(Float(10,5))  # 流动资产
    fixedAssets = Column(Float(10,5))  # 固定资产
    reserved = Column(Float(10,5))  # 公积金
    undp = Column(Float(10,5))  # 未分利润
    # 每股
    reservedPerShare = Column(Float(10,5))  # 每股公积金
    esp = Column(Float(10,5))  # 每股收益
    bvps = Column(Float(10,5))  # 每股净资
    pb = Column(Float(10,5))  # 市净率
    perundp = Column(Float(10,5))  # 每股未分配
    # 利润&增长
    gpr = Column(Float)  # 毛利率(%)
    npr = Column(Float)  # 净利润率(%)
    rev = Column(Float)  # 收入同比(%)
    profit = Column(Float)  # 利润同比(%)

    def __init__(self, code):
        if len(str(code))<6:
            raise Exception(self,('Stock init fail,invalid code:%s,type:%s'% (code,type(code))))
        self.code = code


class DailyRecord(Model, TradeModel):
    id = Column(Integer, primary_key=True)
    __tablename__ = 'dailyrecords'
    code = Column(String(10))
    date = Column(Date)


class MinutelyRecord(Model, TradeModel):
    __tablename__ = 'minutelyrecords'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date = Column(Date)
    hour = Column(Integer)
    minute = Column(Integer)
    # price = Column(Float)  # 当前价
    # volume = Column(Integer)  # 成交量
    # turnover_rate = Column(Float)  # 换手率
    # relative_ratio = Column(Float)  # 量比


class Discovery(Model):
    __tablename__ = 'discovery'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date_time = Column(DateTime)
    type = Column(Integer)
    days = Column(Integer)
    gold_score = Column(Float)  # 黄金分数
    description = Column(String(100))


class UpdateLog(Model):
    __tablename__ = 'updatelogs'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date = Column(Date)
