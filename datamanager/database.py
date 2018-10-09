from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date,DECIMAL,Boolean
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from datamanager import config

def get_connection():
    if config.TEST is True:
        return create_engine(config.TEST_DATABASE_URI, convert_unicode=True, **config.TEST_DATABASE_CONNECT_OPTIONS)

    return create_engine(config.DATABASE_URI, convert_unicode=True,**config.DATABASE_CONNECT_OPTIONS)

engine=get_connection()
db_session=scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base(name='Model')

def create_all():
    Base.metadata.create_all(engine)

def drop_all():
    db_session.session_factory.close_all()
    Base.metadata.drop_all(engine)

class TradeModel:
    """
    主要交易字段
    """
    volume = Column(Integer)  # 成交量
    price_change = Column(DECIMAL(10,2))  # 涨跌值
    p_change= Column(DECIMAL(10,2))  # 涨跌率，真实小数（非百分比）
    open = Column(DECIMAL(10,2))
    close = Column(DECIMAL(10,2))
    high = Column(DECIMAL(10,2))
    low = Column(DECIMAL(10,2))
    turnover = Column(DECIMAL(10,2))  # 换手率
    relative_ratio = Column(DECIMAL(10,2))  # 量比


class Stock(Base):
    __tablename__ = 'stocks'
    code = Column(String(50), primary_key=True)
    name = Column(String(50))
    isdel=Column(Boolean,default=False)
    intro = Column(String(500))
    tag = Column(String(500))  # 板块标签，逗号分隔
    industry = Column(String(50))  # 所属行业
    area = Column(String(50))  # 地区

    timeToMarket = Column(Date)  # 上市日期
    update_time = Column(DateTime)
    update_remark = Column(String(500))  # 更新备注
    risk_warnning = Column(String(500))  # 风险提示
    # 重要指标
    pe = Column(DECIMAL(10,2))  # 市盈率
    pb = Column(DECIMAL(10,2))  # 市净率
    # 总值
    capitalization = Column(DECIMAL(10,2))  # 市值(亿)
    outstanding = Column(DECIMAL(10,2))  # 流通股本(亿)
    totals = Column(DECIMAL(10,2))  # 总股本(亿)
    holders = Column(Integer)  # 股东人数
    totalAssets = Column(DECIMAL(13,2))  # 总资产(万)
    liquidAssets = Column(DECIMAL(13,2))  # 流动资产(万)
    fixedAssets = Column(DECIMAL(13,2))  # 固定资产(万)
    reserved = Column(DECIMAL(13,2))  # 公积金(万)
    undp = Column(DECIMAL(13,2))  # 未分利润(万)
    # 每股
    reservedPerShare = Column(DECIMAL(10,3))  # 每股公积金
    esp = Column(DECIMAL(10,3))  # 每股收益
    bvps = Column(DECIMAL(10,3))  # 每股净资
    perundp = Column(DECIMAL(10,3))  # 每股未分配
    # 利润&增长
    gpr = Column(DECIMAL(10,2))  # 毛利率(%)
    npr = Column(DECIMAL(10,2))  # 净利润率(%)
    rev = Column(DECIMAL(10,2))  # 收入同比(%)
    profit = Column(DECIMAL(10,2))  # 利润同比(%)

    def __init__(self, code):
        if len(str(code))<6:
            raise Exception(self,('Stock init fail,invalid code:%s,type:%s'% (code,type(code))))
        self.code = code


class DailyRecord(Base, TradeModel):
    id = Column(Integer, primary_key=True)
    __tablename__ = 'dailyrecords'
    code = Column(String(10))
    date = Column(Date)
    ma5=Column(DECIMAL(10,2))
    ma10=Column(DECIMAL(10,2))
    ma20=Column(DECIMAL(10,2))
    v_ma5=Column(DECIMAL(10,2))
    v_ma10=Column(DECIMAL(10,2))
    v_ma20=Column(DECIMAL(10,2))
    def __init__(self,code):
        self.code=code


class MinutelyRecord(Base, TradeModel):
    __tablename__ = 'minutelyrecords'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date = Column(Date)
    hour = Column(Integer)
    minute = Column(Integer)
    price = Column(DECIMAL(10,2))  # 最新价
    # price = Column(DECIMAL(10,2))  # 当前价
    # volume = Column(Integer)  # 成交量
    # turnover_rate = Column(DECIMAL(10,2))  # 换手率
    # relative_ratio = Column(DECIMAL(10,2))  # 量比


class Discovery(Base):
    __tablename__ = 'discovery'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date_time = Column(DateTime)
    type = Column(Integer)
    days = Column(Integer)
    gold_score = Column(DECIMAL(10,2))  # 黄金分数
    description = Column(String(100))


class UpdateLog(Base):
    __tablename__ = 'updatelogs'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    date = Column(Date)
